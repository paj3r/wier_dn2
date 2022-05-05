import contextvars
import copy
import os
import re
import bs4
import Levenshtein
from bs4 import BeautifulSoup

def partial_alignment(tree1, tree2):

    if isinstance(tree1, bs4.NavigableString) or isinstance(tree2, bs4.NavigableString):
        if isinstance(tree1, bs4.NavigableString) and isinstance(tree2, bs4.NavigableString):
            return bs4.NavigableString("#PGDATA")
        else:
            return bs4.NavigableString("#RANDOM")

    # check parents
    if tree1.name == tree2.name:
        tree1.contents = list(filter(lambda item: item != " ", tree1.contents))
        tree2.contents = list(filter(lambda item: item != " ", tree2.contents))

        # check children

        c1 = ""
        for x in tree1.children:
            if x.name:
                c1 += x.name

        c2 = ""
        for x in tree2.children:
            if x.name:
                c2 += x.name

        if len(list(tree1.children)) == len(list(tree2.children)) and c1 == c2:

            for i, (tree1_sub, tree2_sub) in enumerate(zip(tree1.children, tree2.children)):

                if tree1_sub == tree2_sub:
                    # children are the same, skip
                    continue

                # otherwise, make new p. aligned tree
                subtree = partial_alignment(tree1_sub, tree2_sub)

                tree1.contents[i].replace_with(copy.copy(subtree))

            extract_unique(tree1)
            return tree1

        # children not same, must match
        else:
            extract_unique(tree1)
            extract_unique(tree2)

            short_tree = ""
            long_tree = ""

            if(len(list(tree1.children)) <= len(list(tree2.children))):
                short_tree = copy.copy(tree1)
                long_tree = copy.copy(tree2)
            else:
                short_tree = copy.copy(tree2)
                long_tree = copy.copy(tree1)

            new_tree = copy.copy(short_tree)
            new_tree.clear()

            i = 0
            j = 0

            short_len = len(short_tree.contents)
            long_len = len(long_tree.contents)

            if short_len == 0:
                new_tree = long_tree
                return new_tree

            while i < short_len:
                match = False
                elem = short_tree.contents[i]
                while j < long_len:

                    elem2 = long_tree.contents[j]

                    if isinstance(elem, bs4.NavigableString) or isinstance(elem2, bs4.NavigableString):

                        new_elem = partial_alignment(elem, elem2)
                        new_tree.contents.append(copy.copy(new_elem))

                        short_tree.contents[i].extract()
                        long_tree.contents[j].extract()

                        short_len = len(short_tree.contents)
                        long_len = len(long_tree.contents)

                        if i < short_len:
                            elem = short_tree.contents[i]
                        else:
                            break

                        match = True

                    elif elem.has_attr("class") and elem2.has_attr("class") and similar(elem['class'], elem2['class']):

                        new_elem = partial_alignment(elem, elem2)
                        new_tree.contents.append(copy.copy(new_elem))

                        short_tree.contents[i].extract()
                        long_tree.contents[j].extract()

                        short_len = len(short_tree.contents)
                        long_len = len(long_tree.contents)

                        if i < short_len:
                            elem = short_tree.contents[i]
                        else:
                            break

                        match = True

                    elif elem.has_attr('id') and elem2.has_attr('id') and elem['id'] == elem2['id']:

                        new_elem = partial_alignment(elem, elem2)
                        new_tree.contents.append(copy.copy(new_elem))

                        short_tree.contents[i].extract()
                        long_tree.contents[j].extract()

                        short_len = len(short_tree.contents)
                        long_len = len(long_tree.contents)

                        if i < short_len:
                            elem = short_tree.contents[i]
                        else:
                            break

                        match = True

                    elif elem.name == elem2.name and Levenshtein.distance(str(clear_nav(copy.copy(elem))), str(clear_nav(copy.copy(elem2)))) < int(0.2 * max(len(str(elem)), len(str(elem2)))) and tree_height(elem, 0) == tree_height(elem2, 0):

                        new_el = partial_alignment(elem, elem2)
                        new_tree.contents.append(copy.copy(new_el))

                        short_tree.contents[i].extract()
                        long_tree.contents[j].extract()

                        short_len = len(short_tree.contents)
                        long_len = len(long_tree.contents)

                        if i < short_len:
                            el = short_tree.contents[i]
                        else:
                            break

                        match = True

                    else:
                        j += 1

                if not match and i < short_len:
                    copied = copy.copy(short_tree.contents[i])
                    new_tree.append(copied)
                    short_tree.contents[i].extract()
                    short_len = len(short_tree.contents)

            short_tree.extract()

            if len(long_tree.contents) != 0:
                while len(long_tree.contents) > 0:
                    new_tree.append(long_tree.contents[0].extract())

            return new_tree

    return tree1

def extract_unique(t : BeautifulSoup):

    """
    tree.contents = list(filter(lambda x: x != " ", tree.contents))

    i = 0

    while i < len(tree.contents):
        j = i + 1
        while j < len(tree.contents):

            no_nav1 = str(clear_nav(copy.copy(tree.contents[i])))
            no_nav2 = str(clear_nav(copy.copy(tree.contents[j])))
            max_len = max(len(str(tree.contents[i])), len(str(tree.contents[j])))


            if isinstance(tree.contents[i], bs4.NavigableString) or isinstance(tree.contents[i], bs4.NavigableString):
                j += 1
            elif Levenshtein.distance(no_nav1, no_nav2,) / max_len < 0.2 and tree_height(tree.contents[i], 0) == tree_height(tree.contents[j], 0):

                temp = copy.copy(tree.contents[i])
                tree.contents[i] = copy.copy(partial_alignment(tree.contents[i], tree.contents[j]))

                # tag as repeat
                tree.contents[i]["r"] = "t"
                tree.contents[j].extract()
            else:
                j += 1
        i += 1
    """

    t.contents = list(filter(lambda x: x != " ", t.contents))

    i = 0

    while i < len(t.contents):
        j = i + 1
        while j < len(t.contents):

            if isinstance(t.contents[i], bs4.NavigableString) or isinstance(t.contents[j], bs4.NavigableString):
                j += 1
            elif Levenshtein.distance(str(clear_nav(copy.copy(t.contents[i]))),
                                      str(clear_nav(copy.copy(t.contents[j])))) / max(len(str(t.contents[i])),
                                                                                             len(str(t.contents[
                                                                                                         j]))) < 0.2 and \
                    tree_height(t.contents[j], 0) == tree_height(t.contents[i], 0):

                _temp = copy.copy(t.contents[i])
                t.contents[i].replace_with(copy.copy(partial_alignment(t.contents[i], t.contents[j])))
                # add repeat tag
                t.contents[i]["r"] = "t"
                t.contents[j].extract()
            else:
                j += 1
        i += 1

def similar(param, param1):

    for x in param:
        if x in ['mobile-show-only']:
            continue
        if x in param1:
            return True
    return False

def tree_height(tree: BeautifulSoup, curr_h):

    # already on last layer, size -> 0
    if isinstance(tree, bs4.NavigableString):
        return curr_h

    # no contents -> size 0
    if not tree.contents:
        return curr_h

    max_h = -1
    for child_el in tree.contents:
        ch = tree_height(child_el, curr_h + 1)

        if ch > max_h:
            max_h = ch

    return max_h

def strip_whitespace(html_string):

    new_string = ""
    for line in html_string.split(os.linesep):
        new_string += line

    return new_string

def clear_nav(tree : BeautifulSoup):

    count = 0
    l = len(tree.contents)

    if not isinstance(tree, bs4.NavigableString) and 'href' in tree.attrs:
        tree.attrs["href"] = ""
    if not isinstance(tree, bs4.NavigableString) and 'title' in tree.attrs:
        tree.attrs["title"] = ""


    while(count < l):

        child_el = tree.contents[count]

        if isinstance(child_el, bs4.NavigableString):
            tree.contents[count].extract()
            l = len(tree.contents)
        else:
            tree.contents[count] = clear_nav(child_el)
            count += 1

    return tree

def clear_tags(tree : BeautifulSoup) -> BeautifulSoup:

    new_tree = tree.find("body")

    # remove script tags
    for match in new_tree('script'):
        match.decompose()

    # remove style tags
    for match in new_tree('style'):
        match.decompose()

    # remove noscript tags
    for match in new_tree('noscript'):
        match.decompose()

    # remove iframe tags
    for match in new_tree('iframe'):
        match.decompose()

    # remove comments
    for match in new_tree.findAll(text=lambda text: isinstance(text, bs4.Comment)):
        match.extract()

    return new_tree

def remove_trash(abs_tree : BeautifulSoup):

    if isinstance(abs_tree, bs4.NavigableString):
        if str(abs_tree) in ["#PGDATA", "#RANDOM"]:
            return True
        else:
            return False

    if len(abs_tree.contents) == 0:
        return False

    i = 0
    l = len(abs_tree.contents)
    important = False

    if 'href' in abs_tree.attrs:
        abs_tree.attrs['href'] = "*"
    if 'title' in abs_tree.attrs:
        abs_tree.attrs['title'] = "*"
    if 'data-gps-track' in abs_tree.attrs:
        abs_tree.attrs['data-gps-track'] = "*"

    while i < l:

        child_el = abs_tree.contents[i]

        if not remove_trash(child_el):
            try:
                abs_tree.contents[i] = bs4.NavigableString("#RANDOM")
            except:
                pass
        else:
            important = True

        i += 1

    return important

def extract(raw_p1, raw_p2):


    #preprocess_regex
    pages = [str(raw_p1), str(raw_p2)]

    stripped = [strip_whitespace(page) for page in pages]

    page_trees = [BeautifulSoup(html, 'html.parser') for html in stripped]

    # clear some tags and comments
    page_trees = [clear_tags(tree) for tree in page_trees]

    # perform partial alignment
    abs_tree = partial_alignment(page_trees[0], page_trees[1])

    remove_trash(abs_tree)

    items = abs_tree.findAll(lambda elem: elem.has_attr('r'))

    for item in items:
        item.wrap(BeautifulSoup("", "html.parser").new_tag("repeat"))

    abstract_str = re.sub(r"(#RANDOM)+", r"#RANDOM", str(abs_tree))
    abstract_str = re.sub(r"(#PGDATA)+", r"#PGDATA", str(abstract_str))
    abstract_str = re.sub(r'r="t"', r'', str(abstract_str))
    abstract_str = re.sub(r'(#PGDATA#RANDOM)+', r'#PGDATA', str(abstract_str))
    abstract_str = re.sub(r'(#RANDOM#PGDATA)+', r'#PGDATA', str(abstract_str))
    abstract_str = re.sub(r'#PGDATA', r'#P', str(abstract_str))
    abstract_str = re.sub(r'#RANDOM', r'#R', str(abstract_str))

    return str(abstract_str)
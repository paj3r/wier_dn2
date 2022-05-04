from lxml import etree
from io import StringIO
import html
def xpath(format, htmlraw):
    if format == "bolha":
        return xpathbolha(StringIO(htmlraw))
    if format == "overstock":
        return xpathoverstock(StringIO(htmlraw))
    if format == "rtv":
        return xpathrtv(StringIO(htmlraw))

def xpathbolha(data):
    #print(data.read())
    parser = etree.HTMLParser()
    tree = etree.parse(data, parser)
    searchtopic = tree.xpath('//h1[contains(@class, "ContentHeader-title")]/text()')[0].strip()
    #print(searchtopic)
    subt_hrefs = tree.xpath('//a[contains(@class, "CategoryListing-topCategoryLink")]/@href')
    #print(subt_hrefs)
    subts = tree.xpath('//a[contains(@class, "CategoryListing-topCategoryLink")]/text()')
    #print(subts)
    subt_counts = tree.xpath('//span[contains(@class, "CategoryListing-entitiesCount")]/text()')
    #print(subt_counts)
    ad_count = tree.xpath('//strong[contains(@class, "entities-count")]/text()')
    #print(ad_count)
    ad_pics = tree.xpath('//img[contains(@class, "img") and '
                         'contains(@class, "entity-thumbnail-img") and contains(@class, "is-loaded")]/@src')
    #print(ad_pics)
    ad_hrefs = tree.xpath('//li[contains(@class, "EntityList-item--Regular") or contains(@class, "EntityList-item--VauVau")]'
                          '//a[contains(@class, "link") and @name]/@href')
    #print(ad_hrefs)
    ad_names = tree.xpath('//h3/a[contains(@class, "link") and @name]/text()')
    #print(ad_names)
    ad_locations = tree.xpath('//div[contains(@class, "entity-description-main")]/text()')
    ad_locations = [i.strip() for i in ad_locations]
    ad_locations = [i for i in ad_locations if i]
    #print(ad_locations)
    ad_posted = tree.xpath('//time[contains(@class, "date--full")]/text()')
    #print(len(ad_posted)-len(ad_hrefs))
    ad_price = tree.xpath('//strong[contains(@class, "price") and contains(@class, "price--hrk")]/text()')
    ad_price = [i.strip() for i in ad_price]
    ad_price = [i for i in ad_price if i]
    #print(len(ad_price)-len(ad_posted))
    subs = {}
    for i in range(len(subts)):
        subs[subts[i]] = {
            "hrefs": subt_hrefs[i],
            "count": subt_counts[i]
        }
    ads = {}
    for i in range(len(ad_price)):
        ads[ad_names[i]] = {
            "Location": ad_locations[i],
            "Posted": ad_posted[i],
            "Image_href": ad_pics[i] if i < len(ad_pics) else "No href",
            "Price": ad_price[i],
            "Href": ad_hrefs[i]
        }

    t_out = {
        "Search_topic": searchtopic,
        "Subtopics": subs,
        "Ads": {
            "Total_count": ad_count,
            "Ads": ads
        }
    }
    output = t_out
    return output

def xpathoverstock(data):
    parser = etree.HTMLParser()
    tree = etree.parse(data, parser)
    titles = tree.xpath('(//tr[@bgcolor="#ffffff"]|//tr[@bgcolor="#dddddd"])/td[@valign="top"]/a/b/text()')
    #print(titles)
    descriptions = tree.xpath('(//tr[@bgcolor="#ffffff"]|//tr[@bgcolor="#dddddd"])/td[@valign="top"]/table//td[@valign="top"]//span[@class="normal"]/text()')
    descriptions = [i.strip() for i in descriptions]
    #print(len(descriptions)-len(titles))
    listprices = tree.xpath('//td[@align="left" and @nowrap="nowrap"]/s/text()')
    #print(len(descriptions)-len(listprices))
    prices = tree.xpath('//td[@align="left" and @nowrap="nowrap"]/span[@class="bigred"]/b/text()')
    #print(len(prices)-len(listprices))
    temp = tree.xpath('//td[@align="left" and @nowrap="nowrap"]/span[@class="littleorange"]/text()')
    saving = []
    perc = []
    for i in range(len(temp)):
        t = temp[i].split(" ")
        saving.append(t[0])
        perc.append(t[1])
    ads = {}
    for i in range(len(perc)):
        ads[i] = {
            "Title": titles[i],
            "Content": descriptions[i],
            "ListPrice": listprices[i],
            "Price": prices[i],
            "Saving": saving[i],
            "SavingPercent": perc[i]
        }
    return ads

def xpathrtv(data):
    parser = etree.HTMLParser()
    tree = etree.parse(data, parser)
    author = tree.xpath('//div[@class="author-name"]/text()')[0]
    #print(author)
    published = tree.xpath('//div[@class="publish-meta"]/text()')[0].strip()
    #print(published)
    title = tree.xpath('//h1/text()')[0]
    #print(title)
    subtitle = tree.xpath('//div[@class="subtitle"]/text()')[0]
    #print(subtitle)
    lead = tree.xpath('//p[@class="lead"]/text()')[0]
    #print(lead)
    cont = tree.xpath('//article[@class="article"]/p/text()')
    cont_out = ""
    for tex in cont:
        cont_out += tex
    #print(cont_out)
    output = {
        "Author": author,
        "PublishedTime": published,
        "Title": title,
        "SubTitle": subtitle,
        "Lead": lead,
        "Content": cont_out
    }
    return output
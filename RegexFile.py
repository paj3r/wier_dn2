import sys
import re
import os
import codecs
import json


def maketitle(match_obj):
    return match_obj.group(0).title()

def regex(format, html):
    if format == "bolha":
        return regexbolha(html)
    if format == "overstock":
        return regexoverstock(html)
    if format == "rtv":
        return regexrtv(html)



def regexbolha(html):
    #print(html)
    searchtopic = re.search("(?<=<h1 class=\"ContentHeader-title\">)[\s\S]*(?=</h1>)", html, flags=re.DOTALL).group(0).strip()
    #print(searchtopic)
    #subt1_href = re.search("(?<=<a class=\"CategoryListing-topCategoryLink\" href=\")[\s\S]*?(?=\">)", html).group()
    #print(subt1_href)
    #subt1 = re.search("(?<=<a class=\"CategoryListing-topCategoryLink\" href=\""+subt1_href+"\">)[\s\S]*?(?=</a>)", html).group()
    #print(subt1)
    #subt1_count = re.search("(?<=<span class=\"CategoryListing-entitiesCount\">)[\s\S]*?(?=</span>)", html).group()
    #print(subt1_count)
    subt_hrefs = re.findall("(?<=<a class=\"CategoryListing-topCategoryLink\" href=\")[\s\S]*?(?=\">)", html)
    subts = []
    for url in subt_hrefs:
        subts.append(re.search("(?<=<a class=\"CategoryListing-topCategoryLink\" href=\""+url+"\">)[\s\S]*?(?=</a>)", html).group())
    #print(subts)
    subt_counts = re.findall("(?<=<span class=\"CategoryListing-entitiesCount\">)[\s\S]*?(?=</span>)",
                      html)
    #print(subt_counts)
    ad_count = re.search("(?<=<strong class=\"entities-count\">)[\s\S]*?(?=</strong>)", html).group()
    #print(ad_count)
    ad_pics = re.findall("(?<=<img class=\"img entity-thumbnail-img is-loaded\" src=\")[\s\S]*?(?=\")", html)
    #print(ad_pics)
    ad_hrefs = re.findall("(?<=\" class=\"link\" href=\")[\s\S]*?(?=\")", html)
    ad_hrefs = ad_hrefs[:len(ad_hrefs)-6]
    ad_names = []
    for url in ad_hrefs:
        ad_names.append(re.search("(?<= class=\"link\" href=\""+url+"\">)[\s\S]*?(?=</a>)", html).group())
    #print(ad_names)
    #print(ad_hrefs)
    ad_locations = re.findall("(?<=<span class=\"entity-description-itemCaption\">Lokacija: </span>)[\s\S]*?(?=<br>)", html)
    #print(ad_locations)
    ad_posted = re.findall("(?<=pubdate=\"pubdate\">)[\s\S]*?(?=</time>)", html)
    #print(ad_posted)
    ad_price = re.findall("(?<=<strong class=\"price price--hrk\">)[\s\S]*?(?=&nbsp;)", html)
    for i in range(len(ad_price)):
        ad_price[i] = ad_price[i].strip()
    #print(ad_price)
    subs={}
    for i in range(len(subts)):
        subs[subts[i]]={
            "hrefs":subt_hrefs[i],
            "count":subt_counts[i]
        }
    ads={}
    for i in range(len(ad_price)):
        ads[ad_names[i]]={
            "Location":ad_locations[i],
            "Posted":ad_posted[i],
            "Image_href":ad_pics[i] if i<len(ad_pics) else "No href",
            "Price":ad_price[i],
            "Href":ad_hrefs[i]
        }

    t_out={
        "Search_topic": searchtopic,
        "Subtopics": subs,
        "Ads":{
            "Total_count": ad_count,
            "Ads":ads
        }
    }
    output = t_out
    return output

def regexoverstock(html):
    hrefs = re.findall("(?<=<td valign=\"top\" align=\"center\"> \n<table><tbody><tr><td><a href=\")[\s\S]*?(?=\")",html)
    #print(img_hrefs)
    titles = []
    for url in hrefs:
        url_t = str(url).replace("?", "\?")
        titles.append(re.search("(?<="+url_t+"\"><b>)[\s\S]*?(?=</b>)", html).group(0))
    descriptions = re.findall('(?<=</tbody></table> \n</td><td valign="top"><span class="normal">)[\s\S]*?(?=<br>)', html)
    listprices = re.findall('(?<=<b>List Price:</b></td><td align="left" nowrap="nowrap"><s>)[\s\S]*?(?=</s)', html)
    #print(len(listprices))
    prices = re.findall('(?<=</td></tr> \n<tr><td align="right" nowrap="nowrap"><b>Price:</b></td><td align="left" nowrap="nowrap"><span class="bigred"><b>)[\s\S]*?(?=</b)', html)
    #print(len(prices))
    temp = re.findall('(?<=<b>You Save:</b></td><td align="left" nowrap="nowrap"><span class="littleorange">)[\s\S]*?(?=</span>)', html)
    saving = []
    perc = []
    for i in range(len(temp)):
        t = temp[i].split(" ")
        saving.append(t[0])
        perc.append(t[1])
    ads = {}
    for i in range(len(perc)):
        ads[i] = {
           "Title":titles[i],
           "Content":descriptions[i],
           "ListPrice":listprices[i],
           "Price":prices[i],
           "Saving":saving[i],
           "SavingPercent":perc[i]
        }
    return ads

def regexrtv(html):
    author = re.search('(?<=<div class="author-name">)[\s\S]*?(?=</div>)', html).group()
    #print(author)
    published = re.search('(?<=<div class="publish-meta">\n)[\s\S]*?(?=<br>)', html).group().strip()
    #print(published)
    title = re.search('(?<=<h1>)[\s\S]*?(?=</h1>)', html).group().strip()
    #print(title)
    subtitle = re.search('(?<=<div class="subtitle">)[\s\S]*?(?=</div>)', html).group().strip()
    #print(subtitle)
    lead = re.search('(?<=<p class="lead">)[\s\S]*?(?=</p>)', html).group().strip()
    #print(lead)
    cont = re.findall('(?<=<p class="Body">)[\s\S]*?(?=</p>)',html)
    cont_out = ""
    for tex in cont:
        cont_out+=tex
    #print(cont_out)
    output = {
        "Author":author,
        "PublishedTime":published,
        "Title":title,
        "SubTitle":subtitle,
        "Lead":lead,
        "Content":cont_out
    }
    return output


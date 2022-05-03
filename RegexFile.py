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
    print(html)
    img_hrefs = re.findall('''
        (?<=<tr bgcolor="#ffffff"> 
<td valign="top" align="center"> 
<table><tbody><tr><td><a href=")[\s\S]*?(=?")
    ''',html)
    print(img_hrefs)

def regexrtv(html):
    return 1
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

def xpathoverstock(html):
    return 1
def xpathrtv(html):
    return 1
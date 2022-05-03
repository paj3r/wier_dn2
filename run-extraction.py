import sys
import re
import os
import codecs
def maketitle(match_obj):
    return match_obj.group(0).title()

def regex(format, html):
    if format == "bolha":
        regexbolha(html)



def regexbolha(html):
    #print(html)
    searchtopic = re.search("(?<=<h1 class=\"ContentHeader-title\">)[\s\S]*(?=</h1>)", html, flags=re.DOTALL).group(0).strip()
    print(searchtopic)
    subt1_href = re.search("(?<=<a class=\"CategoryListing-topCategoryLink\" href=\")[\s\S]*?(?=\">)", html).group()
    print(subt1_href)
    subt1 = re.search("(?<=<a class=\"CategoryListing-topCategoryLink\" href=\""+subt1_href+"\">)[\s\S]*?(?=</a>)", html).group()
    print(subt1)


method = sys.argv[1]
#print(method)
folders = os.listdir("webpages")
bolha = codecs.open("./webpages/bolha.com/aparati.html", "r", "utf-8")
jewelry1 = codecs.open("webpages/overstock.com/jewelry01.html", "r", "utf-8")
jewelry2 = codecs.open("webpages/overstock.com/jewelry02.html", "r", "utf-8")
audi = codecs.open("webpages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", "r", "utf-8")
volvo = codecs.open("webpages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html", "r", "utf-8")
doncic = codecs.open("webpages/siol.net/Razočaranje za fantastičnega Dončića, ki je dosegel nov zgodovinski mejnik - siol.net.html", "r", "utf-8")

pr = re.search("(?<=<a>).*(?=</a>)", "<body> <a>Hello world</a> </body>")
print(pr.group(0))
if method == "A":
    regex("bolha", bolha.read())
    regex("overstock", jewelry1)
    regex("overstock", jewelry2)
    regex("rtvslo", audi)
    regex("rtvslo", volvo)
    regex("siol", doncic)

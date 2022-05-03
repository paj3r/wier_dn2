import sys
import re
import os
import codecs
import json
import RegexFile as r



method = sys.argv[1]
#print(method)
folders = os.listdir("webpages")
bolha = codecs.open("./webpages/bolha.com/aparati.html", "r", "utf-8")
jewelry1 = codecs.open("webpages/overstock.com/jewelry01.html", "r", "ISO-8859-1")
jewelry2 = codecs.open("webpages/overstock.com/jewelry02.html", "r", "ISO-8859-1")
audi = codecs.open("webpages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", "r", "utf-8")
volvo = codecs.open("webpages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html", "r", "utf-8")
bolha2 = codecs.open("webpages/bolha.com/avdio.html", "r", "utf-8")

#print(pr.group(0))
if method == "A":
    bol = r.regex("bolha", bolha.read())
    bol2 = r.regex("bolha", bolha2.read())
    ove = r.regex("overstock", jewelry1.read())
    ove2 = r.regex("overstock", jewelry2.read())
    rtv = r.regex("rtv", audi.read())
    rtv2 = r.regex("rtv", volvo.read())
    ou = {
        "bolha.com": {
            "0": bol,
            "1": bol2
        },
        "overstock.com":{
            "0": ove,
            "1": ove2
        },
        "rtvslo.si":{
            "0": rtv,
            "1": rtv2
        }
    }
    #print(ou)

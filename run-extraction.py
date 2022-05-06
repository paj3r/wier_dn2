import sys
import re
import os
import codecs
import json
import RegexFile as r
import xPathFile as x
import RoadRunner as rr



method = sys.argv[1]
#print(method)
folders = os.listdir("webpages")
bolha = codecs.open("./webpages/bolha.com/aparati.html", "r", "utf-8")
bolha2 = codecs.open("webpages/bolha.com/avdio.html", "r", "utf-8")
jewelry1 = codecs.open("webpages/overstock.com/jewelry01.html", "r", "ISO-8859-1")
jewelry2 = codecs.open("webpages/overstock.com/jewelry02.html", "r", "ISO-8859-1")
audi = codecs.open("webpages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", "r", "utf-8")
volvo = codecs.open("webpages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html", "r", "utf-8")

if os.path.isdir("results"):
    print("Results dir already exists")
    pass
else:
    os.mkdir("results")

def write_json(method):
    ou = {
        "bolha.com": {
            "0": bol,
            "1": bol2
        },
        "overstock.com": {
            "0": ove,
            "1": ove2
        },
        "rtvslo.si": {
            "0": rtv,
            "1": rtv2
        }
    }

    if method == "A":
        pass
    elif method == "B":
        pass

def make_txt(results):

    try:
        with open("results\\roadrunner\\overstock.txt", "w") as file:
            file.write(results[0])

        with open("results\\roadrunner\\rtvslo.txt", "w") as file:
            file.write(results[1])

        with open("results\\roadrunner\\bolha.txt", "w") as file:
            file.write(results[2])

    except FileNotFoundError:
        print("Results directory doesn't exist!")

    pass

#print(pr.group(0))
if method == "A":
    bol = r.regex("bolha", bolha.read())
    bol2 = r.regex("bolha", bolha2.read())
    ove = r.regex("overstock", jewelry1.read())
    ove2 = r.regex("overstock", jewelry2.read())
    rtv = r.regex("rtv", audi.read())
    rtv2 = r.regex("rtv", volvo.read())
    write_json()
elif method == "B":
    bol = x.xpath("bolha", bolha.read())
    bol2 = x.xpath("bolha", bolha2.read())
    ove = x.xpath("overstock", jewelry1.read())
    ove2 = x.xpath("overstock", jewelry2.read())
    rtv = x.xpath("rtv", audi.read())
    rtv2 = x.xpath("rtv", volvo.read())
    write_json()
elif method == "C":
    ove = rr.extract(jewelry1.read(), jewelry2.read())
    rtv = rr.extract(audi.read(),volvo.read())
    bol = rr.extract(bolha.read(),bolha2.read())
    make_txt([ove, rtv, bol])





import csv
import requests
from bs4 import BeautifulSoup
import math
import os.path
from os import path
import re
def readCsvFile():
    with open('URLs(without features).csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        readURLs = []
        kinds = []
        for row in readCSV:
            url = row[1]
            kind = row[2]
            readURLs.append(url)
            kinds.append(kind)
    csvfile.close()
    return readURLs,kinds
def createCsvFile(URLs):
    csv.register_dialect('myDialect',
    quoting=csv.QUOTE_ALL,
    skipinitialspace=True)
    with open('URLs(with features-before selection).csv', 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(["id","url","type","ip","https","spam","#.","#/","#numbers","sensitive_words","uppercase_letter","length","suspicious_character",
                         "prefix-suffix","tld","entropy","brands","www_misuse","has_www","extension_extraction"])
        for row in URLs:
            writer.writerow(row)
    f.close()
def getTLDList():
    r = requests.get("http://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    soup = BeautifulSoup(r.content)
    tldList = []
    d = soup.findAll(text=True)
    for line in d:
        for line2 in line.strip().split('\n'):
            if line2:
                tldList.append(line2)
    tldList = tldList[1:]
    return tldList
def is_ip(url):
    ip = False
    length = len(url)
    for i in range(length):
        count = 0
        j = i
        while(j<length and ((ord(url[j])>=48 and ord(url[j])<=57) or ord(url[j])==46)):
            if(ord(url[j])==46):             #Ascii of the dot
                count = count + 1
            j = j + 1
        if(count==3):
            ip = True
    if(ip == True):
        return 0
    else:
        return 1
def is_https(url):
    if(url[3] == 'p' and url[4] == 's'):
        return 1
    else:
        return 0
def is_spam(url):
    u = url[:4]
    if(u == "SPAM"):
        return 0
    else:
        return 1
def numberOfDots(url):
    if(url[8]=='w'):
        if(url[4]=='s'):
            i = 12
        else:
            i = 11
    else:
        if(url[4]=='s'):
            i = 8
        else:
            i = 7
    count = 0
    length = len(url)
    while(i<length):
        if(url[i]=='.'):
            count = count + 1
        i = i + 1
    if(count>1):
        return 0
    else:
        return 1
def numberOfSlashes(url):
    length = len(url)
    count = 0
    for i in range(length):
        if(url[i] == '/'):
            count = count + 1
    if(count>6):
        return 0
    else:
        return 1
def numberOfNumbers(url):
    length = len(url)
    count = 0
    for i in range(length):
        if(ord(url[i])>=48 and ord(url[i])<=57):
            count = count + 1
    if(count>6):
        return 0
    else:
        return 1
def existenceOfSensitiveWords(url):
    phishingWords = ["secure","account","login","signin","confirm","submit","verify","mail"]
    phishing = False
    for i in range(len(phishingWords)):
        if(phishingWords[i] in url.lower()):
            phishing = True
    if(phishing == True):
        return 0
    else:
        return 1
def existenceOfUpperCaseLetter(url):
    length = len(url)
    phishing = False
    for i in range(length):
        if(ord(url[i])>=65 and ord(url[i])<=90):
            phishing = True
    if(phishing == True):
        return 0
    else:
        return 1
def length(url):
    if(len(url) > 100):
        return 0
    else:
        return 1
def has_suspicious_char(url):
    if(url.find("@")!=-1 or url.find("&")!=-1 or url.count("//")>1 or url.find("!")!=-1 or url.find("?")!=-1 or url.find("=")!=-1 or url.find("#")!=-1 or url.find("$")!=-1 or url.find("_")!=-1 or url.find("*")!=-1 or url.find("+")!=-1 or url.find(" ")!=-1 or url.find("~")!=-1 or url.find(",")!=-1 or url.find("%")!=-1 or url.count(":")>1 or url.find("<")!=-1 or url.find(">")!=-1 or url.find("|")!=-1 or url.find("\\")!=-1):
        return 0
    else:
        return 1
def prefix_suffix(url):
    if(url.find("-") != -1):
        return 0
    else:
        return 1
def TLD_count(url,tldList):
    tld_Found = False
    slash_count = 0
    if(url.count('/') == 2):
        url = url + "/"
    i = 0
    stop = 0
    while(i<len(url) and stop==0):
        if(url[i] == '/'):
            slash_count = slash_count + 1
        if(slash_count==3):
            stop = 1
        i = i + 1
    u = url[i:]
    for tld in tldList:
        if(u.find("."+tld.lower()+".") != -1 or
           u.find("."+tld.lower()+"/") != -1 or
           u.find("."+tld.lower()+"&") != -1):
            tld_Found = True
    if(tld_Found == True):
        return 0
    else: 
        return 1 
def entropy(url):
    if not url:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(url.count(chr(x)))/len(url)
        if(p_x > 0):
            entropy += - p_x*math.log(p_x, 2)
    if(entropy>4.8):
        return 0
    else:
        return 1
def existenceOfBrands(url):
    brands = ["outlook","facebook","instagram","twitter","google","netflix","whatsapp","linkedin","ebay","amazon","apple","microsoft","adobe","yahoo","dropbox","icloud","paypal","onedrive","windows","office","iphone","firebase","steam","origin","epicgames","vodafone","bit.ly","bitly","starmak","tesla","elon","bankofamerica","finanzas","webhostapp","ziraat","usbank","wellsfargo","runescape","absabank","americanexpress","intesasanpaolo","allegro","deltaairlines","blockchain","itau","posteitaliane","orange","index","bancodebrasil","aol","mastercard","sulake"]
    phishing = False
    for i in range(len(brands)):
        if(brands[i] in url.lower()):
            phishing = True
    if(phishing == True):
        return 0
    else:
        return 1
def misuse_of_www(url):
    index = url.find("www")
    if((index!=-1 and index+3<len(url) and url[index+3]!='.') or (index!=-1 and index!=7 and index!=8) or url.count("www")>1):
        return 0
    else:
        return 1
def existence_of_www(url):
    if(url.find("www")==-1 or url.find("www")>8):
        return 0
    else:
        return 1
def extract_extension(url):
    file = open('extensions.txt', 'r')
    pattern = re.compile("[a-zA-Z0-9.]")
    for extension in file:
        i = (url.lower().strip()).find(extension.strip())
        while(i > -1):
            if ((i + len(extension) - 1) >= len(url)) or not pattern.match(url[i + len(extension) - 1]):
                file.close()
                return 0
            i = url.find(extension.strip(), i + 1)
    file.close()
    return 1
def results(url):
    feature = []
    legimate=0
    phishing=0
    for i in range(len(url)):
        result = is_https(url[i])
        feature.append(result)
        if(result==0 and i<107000):
            legimate=legimate+1
        elif(result==0 and i>=107000):
            phishing=phishing+1
    print(feature)
    l=legimate/107000
    p=phishing/107000
    print("Legimate:"+str(l))
    print("Phishing:"+str(p))
    print("phishing/legimate:"+str(p/l))



url,kind = readCsvFile()
ip = []
https = []
spam = []
number_of_dots = []
number_of_slashes = []
number_of_numbers = []
sensitive_words = []
upper_case_letter = []
length_ = []
suspicious_character = []
prefixSuffix = []
tld = []
entropy_ = []
brands = []
www_misuse = []
has_www = []
extension = []
tldList = getTLDList()
for i in range(len(url)):
    ip.append(is_ip(url[i]))
    https.append(is_https(url[i]))
    spam.append(is_spam(url[i]))
    number_of_dots.append(numberOfDots(url[i]))
    number_of_slashes.append(numberOfSlashes(url[i]))
    number_of_numbers.append(numberOfNumbers(url[i]))
    sensitive_words.append(existenceOfSensitiveWords(url[i]))
    upper_case_letter.append(existenceOfUpperCaseLetter(url[i]))
    length_.append(length(url[i]))
    suspicious_character.append(has_suspicious_char(url[i]))
    prefixSuffix.append(prefix_suffix(url[i]))
    tld.append(TLD_count(url[i],tldList))
    entropy_.append(entropy(url[i]))
    brands.append(existenceOfBrands(url[i]))
    www_misuse.append(misuse_of_www(url[i]))
    has_www.append(existence_of_www(url[i]))
    extension.append(extract_extension(url[i]))
URLs = []
for i in range(len(url)):
    row = []
    for j in range(20):
        if (j % 20 == 0):
            row.append(i + 1)
        elif (j % 20 == 1):
            row.append(url[i])
        elif (j % 20 == 2):
            row.append(kind[i])
        elif (j % 20 == 3):
            row.append(ip[i])            
        elif (j % 20 == 4):
            row.append(https[i])
        elif (j % 20 == 5):
            row.append(spam[i])
        elif (j % 20 == 6):
            row.append(number_of_dots[i])    
        elif (j % 20 == 7):
            row.append(number_of_slashes[i])
        elif (j % 20 == 8):
            row.append(number_of_numbers[i])
        elif (j % 20 == 9):
            row.append(sensitive_words[i])
        elif (j % 20 == 10):
            row.append(upper_case_letter[i])
        elif (j % 20 == 11):
            row.append(length_[i])  
        elif (j % 20 == 12):
            row.append(suspicious_character[i])
        elif (j % 20 == 13):
            row.append(prefixSuffix[i])
        elif (j % 20 == 14):
            row.append(tld[i])
        elif (j % 20 == 15):
            row.append(entropy_[i])
        elif (j % 20 == 16):
            row.append(brands[i])  
        elif (j % 20 == 17):
            row.append(www_misuse[i])
        elif (j % 20 == 18):
            row.append(has_www[i])
        elif (j % 20 == 19):
            row.append(extension[i])
    URLs.append(row)
createCsvFile(URLs)
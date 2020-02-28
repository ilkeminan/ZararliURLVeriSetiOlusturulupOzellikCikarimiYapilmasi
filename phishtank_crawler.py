import csv
import requests
from bs4 import BeautifulSoup
import os.path
from os import path
import time
def getPhishingIDs(numberOfPages):
    phish_id = []
    for i in range(numberOfPages):
        r = requests.get("https://www.phishtank.com/phish_search.php?page="+str(i)+"&valid=y&Search=Search")
        soup = BeautifulSoup(r.content)
        links = soup.find_all("a")
        for link in links:
            if("phish_id=" in link.get("href")):
                id = link.get("href")[link.get("href").find("phish_id=")+9:link.get("href").find("phish_id=")+16]
                phish_id.append(id)
    return phish_id
def getPhishingURLs(phish_id,readURLs,url_id):
    url = []
    for id in phish_id:
        r = requests.get("https://www.phishtank.com/phish_detail.php?phish_id="+id)
        soup = BeautifulSoup(r.content)
        links2 = soup.find_all("span")
        count = 0
        for link in links2:
            if(count == 2 and not "[email" in link.text):
                url.append(link.text)
            count = count + 1
    url = list(set(url) - set(readURLs))
    url = list(dict.fromkeys(url))  # removing duplicates
    phishingURLSize = len(url)
    URLs = []
    for i in range(phishingURLSize):
        row = []
        for j in range(3):
            if (j % 3 == 0):
                row.append(url_id + 1)
            elif (j % 3 == 1):
                row.append(url[i])
            elif (j % 3 == 2):
                row.append(0)
        URLs.append(row)
        url_id = url_id + 1
    return URLs
def createCsvFile(phishingURLs):
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    with open('phishing_URLs.csv', 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        for i in phishingURLs:
            writer.writerow(i)
    f.close()
def appendRowsToCsvFile(phishingURLs):
    with open('phishing_URLs.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        for row in phishingURLs:
            writer.writerow(row)
    csvFile.close()
def readCsvFile():
    with open('phishing_URLs.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        readURLs = []
        for row in readCSV:
            url = row[1]
            lastID = row[0]
            readURLs.append(url)
    csvfile.close()
    return readURLs,lastID


if(path.exists("phishing_URLs.csv")):
    numberOfPages = 100
    phishingIDs = getPhishingIDs(numberOfPages)
    index = 0
    while(index<numberOfPages*10):
        readURLs,lastID = readCsvFile()
        IDs = phishingIDs[index:index+10]
        phishingURLs = getPhishingURLs(IDs,readURLs,int(lastID))
        appendRowsToCsvFile(phishingURLs)
        time.sleep(5)
        index = index + 10
else:
    numberOfPages = 100
    phishingIDs = getPhishingIDs(numberOfPages)
    index = 0
    while(index<numberOfPages*10):
        IDs = phishingIDs[index:index+10]
        if(index==0):
            readURLs = []
            phishingURLs = getPhishingURLs(IDs,readURLs,0)
            createCsvFile(phishingURLs)
        else:
            readURLs,lastID = readCsvFile()
            phishingURLs = getPhishingURLs(IDs,readURLs,int(lastID))
            appendRowsToCsvFile(phishingURLs)
        time.sleep(5)
        index = index + 10
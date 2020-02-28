import csv
import requests
import os.path
from os import path
def readCsvFile():
    with open('dmoztools_URLs.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        readURLs = []
        for row in readCSV:
            url = row[1]
            lastID = row[0]
            readURLs.append(url)
    csvfile.close()
    return readURLs,lastID
def createCsvFile(URLs):
    csv.register_dialect('myDialect',
    quoting=csv.QUOTE_ALL,
    skipinitialspace=True)
    with open('benign_URLs.csv', 'w') as f:
        writer = csv.writer(f, dialect='myDialect')
        for row in URLs:
            writer.writerow(row)
    f.close()
def appendRowsToCsvFile(URLs):
    with open('benign_URLs.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        for row in URLs:
            writer.writerow(row)
    csvFile.close()

if(path.exists("dmoztools_URLs.csv")):
    count=0
    url,lastID = readCsvFile()
    url = url[0:55000]
    fixed_url = []
    for i in range(len(url)):
        try:
            r = requests.get(url[i])
            fixed_url.append(r.url)
            count=count+1
            print(str(count)+","+r.url)
        except:
            continue
    urlSize = len(fixed_url)
    URLs = []
    for i in range(urlSize):
        row = []
        for j in range(3):
            if (j % 3 == 0):
                row.append(i + 1)
            elif (j % 3 == 1):
                row.append(fixed_url[i])
            elif (j % 3 == 2):
                row.append(1)
        URLs.append(row)
    if(path.exists("benign_URLs.csv")):
        appendRowsToCsvFile(URLs)
    else:
        createCsvFile(URLs)
else:
    print("There is no file named 'dmoztools_URLs.csv'")
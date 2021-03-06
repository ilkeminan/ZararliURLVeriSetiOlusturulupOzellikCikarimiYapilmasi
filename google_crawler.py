#!pip install -q fake_useragent
import csv
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import urllib
import re
from os import path
def crawlFromGoogle(readURLs,id):
    queryWords = ["banks", "amazon", "yahoo finance", "stock market", "financas", "stock", "efinance", "finance", "loans", "google market", "stripe", "dwolla",
                  "apple pay", "payoneer", "2checkout", "square", "payza", "pay", "skrill", "venmo", "google wallet", "wepay", "cryptocurrencies", "cash", 
                  "e-wallets", "credit card", "paypal", "adyen", "paymill", "due", "fedex", "bitcoin", "mbill", "online store", "online business", "shopping",
                  "online payment" ,"zendesk", "docusign", "dropbox", "slack", "concur", "amazon web services", "salesforce", "sale", "discount", "raise", 
                  "e-commerce", "saas", "finance", "money"]
    url = []
    for i in queryWords:
        query = i
        query = urllib.parse.quote_plus(query) # Format into URL encoding
        number_result = 100
        ua = UserAgent()
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
        response = requests.get(google_url, {"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, "html.parser")
        result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})
        links = []
        titles = []
        descriptions = []
        for r in result_div:
            # Checks if each element is present, else, raise exception
            try:
                link = r.find('a', href = True)
                title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
                description = r.find('div', attrs={'class':'s3v9rd'}).get_text() 
                # Check to make sure everything is present before appending
                if link != '' and title != '' and description != '': 
                    links.append(link['href'])
                    titles.append(title)
                    descriptions.append(description)
            # Next loop if one element is not present
            except:
                continue
        to_remove = []
        clean_links = []
        for j, l in enumerate(links):
            clean = re.search('\/url\?q\=(.*)\&sa',l)
            # Anything that doesn't fit the above pattern will be removed
            if clean is None:
                to_remove.append(j)
                continue
            clean_links.append(clean.group(1))
        url = list(set(url + clean_links))
    url = list(set(url) - set(readURLs))
    url = list(dict.fromkeys(url))  # removing duplicates
    querySize = len(url)
    URLs = []
    for i in range(querySize):
        row = []
        for j in range(3):
            if (j % 3 == 0):
                row.append(id + 1)
            elif (j % 3 == 1):
                row.append(url[i])
            elif (j % 3 == 2):
                row.append(1)
        URLs.append(row)
        id = id + 1
    return URLs
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
def readCsvFile():
    with open('benign_URLs.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        readURLs = []
        for row in readCSV:
            url = row[1]
            lastID = row[0]
            readURLs.append(url)
    csvfile.close()
    return readURLs,lastID
  
  



if(path.exists("benign_URLs.csv")):
    readURLs,lastID = readCsvFile()
    URLs = crawlFromGoogle(readURLs,int(lastID))
    appendRowsToCsvFile(URLs)    
else:
    readURLs = []
    URLs = crawlFromGoogle(readURLs,0)
    createCsvFile(URLs)
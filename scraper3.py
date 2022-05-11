#Scrapes all pages and gets title, location, date, image#, and SN# and puts into a csv

from urllib.request import urlopen
from bs4 import BeautifulSoup
import math

url = "https://chroniclingamerica.loc.gov/search/pages/results/?date1=1835&rows=1000&searchType=basic&state=&date2=1950&proxtext=%28graded+school%29&y=14&x=24&dateFilterType=yearRange&page=1&sort=relevance"

request_page = urlopen(url)
page_html = request_page.read()
request_page.close()

soup = BeautifulSoup(page_html, 'html.parser')

numRows = 1000
temp =  soup.find('span', class_="results").text.split()
numResults = int(temp[len(temp)-1])
numPages = math.ceil(numResults/numRows) + 1

filename = "./run/data.csv"
f = open(filename, 'w', encoding="utf-8")

headers = "Title, SN Number, Location, Date, Image # \n"

f.write(headers)

for i in range(1, 2):
    print(i)
    url = url[:url.rfind("page")] + "page=" + str(i) + "&sort=relevance"
    request_page = urlopen(url)
    page_html = request_page.read()
    request_page.close()

    soup = BeautifulSoup(page_html, 'html.parser')
    for div in soup.find_all('div', class_="highlite"):
        #print(div)
        atag = div.find_all('a')[1]
        text = atag.text
        title = text[:text.find(".")]
            #print(title)
        location = text[text.find("(")+1:text.rfind(")")]
        text = text[text.rfind(")")+3:]
        #date = text[:text.find("Image")-2]
        date = text[:text.find(",")+6]
        print(date)
        image = text[text.find("Image") + 6:]
            
        text = atag['href']
        
        if text.find("sn") != -1:
            sn = text[text.find("sn"):text.find("sn") + 10]
        else:
            sn = "sn" + text[text.find("lccn")+5:text.find("lccn")+15]
        
        #print("\"" + title + "\", " + sn + ", \"" + location + "\", \"" + date + "\", " + image + "")
        f.write("\"" + title + "\"," + sn + ",\"" + location + "\",\"" + date + "\"," + image + "\n")

f.close()
#f2.close()
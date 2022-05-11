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

filename = "data.csv"
f = open(filename, 'w')

headers = "Title, SN Number, Location, Date, Image # \n"

f.write(headers)

#filename2 = "log.txt"
#f2 = open(filename2, 'w')
print(soup.find('strong'))
for i in range(1, numPages):
    print(i)
    url = url[:url.rfind("page")] + "page=" + str(i) + "&sort=relevance"
    request_page = urlopen(url)
    page_html = request_page.read()
    request_page.close()

    soup = BeautifulSoup(page_html, 'html.parser')
    for ultag in soup.find_all('ul', class_="results_list"):
            #print(ultag)
            for litag in ultag.find_all('li'):
                #print(litag)
                for atag in litag.find_all('a'):
                    text = atag.text
                    title = atag.find('strong').text
                    location = text[text.find("(")+1:text.rfind(")")]
                    text = text[text.rfind(")")+3:]
                    date = text[:text.find("Image")-2]
                    image = text[text.find("Image") + 6:]
                    
                    text = atag['href']
                    sn = text[text.find("sn"):text.find("sn") + 10]

                    #print("\"" + title + "\", " + sn + ", \"" + location + "\", \"" + date + "\", " + image + "")
                    f.write("\"" + title + "\"," + sn + ",\"" + location + "\",\"" + date + "\"," + image + "\n")
""" for i in range (1, 2):
#for i in range(1,numPages+1):
    print(i)
    #f2.write(str(i) + "\n")
    
    
    links = []

    for ultag in soup.find_all('ul', class_="results_list"):
        #print(ultag)
        for litag in ultag.find_all('li'):
            #print(litag)
            for atag in litag.find_all('a'):
                links.append(atag['href'])

    
    #print(links)
    #f2.write(str(links) + "\n")
    for link in links: 
        f.write(link[link.find("sn"):link.find("sn")+ 10] + "\n") """
    

f.close()
#f2.close()
#Scrapes all pages and puts each article's SN#s into a text file named SNs -- Obsolete, scraper 3 does same thing but more + better

from urllib.request import urlopen
from bs4 import BeautifulSoup
import math

url = "https://chroniclingamerica.loc.gov/search/pages/results/list/?date1=1835&rows=20&searchType=basic&state=&date2=1860&proxtext=%28graded+school%29&y=11&x=14&dateFilterType=yearRange&page=1&sort=relevance"

request_page = urlopen(url)
page_html = request_page.read()
request_page.close()

soup = BeautifulSoup(page_html, 'html.parser')

temp =  soup.find('span', class_="results").text.split()
numResults = int(temp[len(temp)-1])
numPages = math.ceil(numResults/20) + 1

filename = "SNs.txt"
filename2 = "log.txt"
f = open(filename, 'w')
#f2 = open(filename2, 'w')
#for i in range (1, 2):

for i in range(1,numPages):
    print(i)
    #f2.write(str(i) + "\n")
    url = url[:url.rfind("page")] + "page=" + str(i) + "&sort=relevance"
    request_page = urlopen(url)
    page_html = request_page.read()
    request_page.close()

    soup = BeautifulSoup(page_html, 'html.parser')
    
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
        f.write(link[link.find("sn"):link.find("sn")+ 10] + "\n")
    

f.close()
#f2.close()
print(numPages)
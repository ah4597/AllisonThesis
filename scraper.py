#Scrapes the first page's images and puts the text into files named after their SN#s

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://chroniclingamerica.loc.gov/search/pages/results/list/?date1=1835&rows=20&searchType=basic&state=&date2=1860&proxtext=%28graded+school%29&y=11&x=14&dateFilterType=yearRange&page=1&sort=relevance"

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
        

for link in links:
    last_paren = link.rfind("/") + 1
    link = link[:last_paren] + "ocr.txt"
    url = "https://chroniclingamerica.loc.gov" + link

    filename = "texts/" + link[link.find("sn"):link.find("sn")+ 10] + ".txt"

    f = open(filename, 'w', encoding="utf-8")

    request_page = urlopen(url)
    page_html = request_page.read()
    request_page.close()
    soup = str(BeautifulSoup(page_html, 'html.parser'))

    #print(soup)
    f.write(soup)

    f.close()
#print(list_items)

#Scrapes the first page's images and puts the text into files named after their SN#s

from urllib.request import urlopen
from bs4 import BeautifulSoup


url = "https://chroniclingamerica.loc.gov/lccn/sn86081096/1861-01-31/ed-1/seq-2/ocr.txt"

filename = "texts/" + url[url.find("sn"):url.find("sn")+ 10] + ".txt"

f = open(filename, 'w', encoding="utf-8")

request_page = urlopen(url)
page_html = request_page.read()
request_page.close()
soup = str(BeautifulSoup(page_html, 'html.parser'))

#print(soup)
f.write(soup)
f.close()

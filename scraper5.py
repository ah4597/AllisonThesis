#Scrapes all pages and gets title, location, date, image#, and SN# and puts into a csv
#Also gathers all the dates of each articles and counts them, and puts the counts into a csv
#Basically, combines scraper 3 and 4.

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict
import math
import time

#url = "https://chroniclingamerica.loc.gov/search/pages/results/?date1=1835&rows=1000&searchType=basic&state=&date2=1950&proxtext=%28graded+school%29&y=14&x=24&dateFilterType=yearRange&page=1&sort=relevance"
url = "https://chroniclingamerica.loc.gov/search/pages/results/list/?date1=1835&rows=2000&searchType=basic&state=&date2=1950&proxtext=house&y=0&x=0&dateFilterType=yearRange&page=1&sort=relevance"

request_page = urlopen(url)
page_html = request_page.read()
request_page.close()

soup = BeautifulSoup(page_html, 'html.parser')

numRows = 2000
temp =  soup.find('span', class_="results").text.split()
numResults = int(temp[len(temp)-1])
numPages = math.ceil(numResults/numRows) + 1


dates = {
}

filename = "./run/data.csv"
error_filename = "./run/error.txt"
f = open(filename, 'w', encoding="utf-8")
error_f = open(filename, 'w', encoding="utf-8")
headers = "Title, SN Number, Location, Date, Image # \n"
f.write(headers)
print("Running for total " + str(numPages-1) + " pages.")
for i in range(1, numPages):
    print("Running on page: " + str(i))
    url = url[:url.rfind("page")] + "page=" + str(i) + "&sort=relevance"
    
    success = False
    retries = 0
    while not success and retries <= 5:
        try:
            request_page = urlopen(url)
            page_html = request_page.read()
            request_page.close()
            soup = BeautifulSoup(page_html, 'html.parser')
            success = True
        except Exception as e:
            wait = retries * 30
            print(f'Error occured. Waiting {wait} secs and retrying.')
            time.sleep(wait)
            retries += 1

    if success:
        for div in soup.find_all('div', class_="highlite"):
            
            #Separate the info
            atag = div.find_all('a')[1]
            text = atag.text
            title = text[:text.find(".")]
                #print(title)
            location = text[text.find("(")+1:text.rfind(")")]
            text = text[text.rfind(")")+3:]
            date = text[:text.find(",")+6]

            #Separate the year, so we can count it
            year = date[len(date)-4:]
            if year in dates:
                dates[year] = dates[year] + 1
            else:
                dates[year] = 1

            image = text[text.find("Image") + 6:]    
            text = atag['href']
            
            if text.find("sn") != -1:
                sn = text[text.find("sn"):text.find("sn") + 10]
            else:
                sn = "sn" + text[text.find("lccn")+5:text.find("lccn")+15]
            
            #print("\"" + title + "\", " + sn + ", \"" + location + "\", \"" + date + "\", " + image + "")
            f.write("\"" + title + "\"," + sn + ",\"" + location + "\",\"" + date + "\"," + image + "\n")
    else:
        print(f'Error retreiving page {i}. Failed 5 times.')
        error_f.write(f'Error retreiving page {i}. Failed 5 times.\n')


f.close()

#Write out the dates and counts into a separate csv
filename2 = "./run/dates.csv"
f = open(filename2, 'w', encoding="utf-8")
headers2 = "Year, Count\n"
f.write(headers2)
dates = OrderedDict(sorted(dates.items(), key=lambda x: x[1], reverse=True))
#print(dates)
for year in dates:
    f.write(str(year) + "," + str(dates[year]) + "\n")

f.close()
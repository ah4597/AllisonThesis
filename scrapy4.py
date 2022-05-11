#Gets years and counts how many articles there are per year
from urllib.request import urlopen
from bs4 import BeautifulSoup
import math

#url = "https://chroniclingamerica.loc.gov/search/pages/results/?date1=1835&rows=20&searchType=basic&state=&date2=1950&proxtext=%28graded+school%29&y=14&x=24&dateFilterType=yearRange&page=1&sort=relevance"
#url = "https://chroniclingamerica.loc.gov/search/pages/results/?date1=1835&rows=20&searchType=basic&state=&date2=1860&proxtext=%28graded+school%29&y=7&x=17&dateFilterType=yearRange&page=1&sort=relevance"
#url = "https://chroniclingamerica.loc.gov/search/pages/results/?date1=1835&rows=500&searchType=basic&state=&date2=1860&proxtext=%28graded+school%29&y=7&x=17&dateFilterType=yearRange&page=1&sort=relevance"

url = "https://chroniclingamerica.loc.gov/search/pages/results/?date1=1835&rows=1000&searchType=basic&state=&date2=1950&proxtext=%28graded+school%29&y=14&x=24&dateFilterType=yearRange&page=1&sort=relevance"
request_page = urlopen(url)
page_html = request_page.read()
request_page.close()

soup = BeautifulSoup(page_html, 'html.parser')

temp =  soup.find('span', class_="results").text.split()
numResults = int(temp[len(temp)-1])
numPages = math.ceil(numResults/1000) + 1

filename = "./run/dates.csv"

f = open(filename, 'w')


#headers = "Title, SN Number, Location, Date, Image # \n"
headers = "Year, Count\n"

f.write(headers)


#dates dict

dates = {
}

#filename2 = "log.txt"
#f2 = open(filename2, 'w')
print(soup.find('strong'))
for i in range(1, numPages):
    #if(i%10 == 0):
    print(i)
    url = url[:url.rfind("page")] + "page=" + str(i) + "&sort=relevance"
    request_page = urlopen(url)
    page_html = request_page.read()
    request_page.close()
    soup = BeautifulSoup(page_html, 'html.parser')
    #print(soup.find('div', class_="highlite"))
    for div in soup.find_all('div', class_="highlite"):
        #print(div)
        for atag in div.find_all('a'):
            text = atag.text
            #print(text)
            year = text[text.rfind('Image')-6:text.rfind('Image')-2]
            #print(year)
            if(year in dates):
                dates[year] = dates[year] + 1
            else: 
                dates[year] = 1
            
    


    """ for tbody in soup.find_all('table', class_="search_results"):
            #print(tbody)
            for trtag in tbody.find_all('tr'):
                #print(litag)
                for tdtag in trtag.find_all('a'):
                    text = atag.text
                    title = atag.find('strong').text
                    location = text[text.find("(")+1:text.rfind(")")]
                    text = text[text.rfind(")")+3:]
                    date = text[:text.find("Image")-2]
                    year = date[date.rfind(",")+1:]
                    if(year in dates):
                        dates[year] = dates[year] + 1
                    else: 
                        dates[year] = 1
                    image = text[text.find("Image") + 6:]
                    
                    text = atag['href']
                    sn = text[text.find("sn"):text.find("sn") + 10]

                    #print("\"" + title + "\", " + sn + ", \"" + location + "\", \"" + date + "\", " + image + "")
                    print("\"" + title + "\"," + sn + ",\"" + location + "\",\"" + date + "\"," + image + "\n")
                    f.write("\"" + title + "\"," + sn + ",\"" + location + "\",\"" + date + "\"," + image + "\n") """


print(dates)
for year in dates:
    f.write(str(year) + "," + str(dates[year]) + "\n")
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
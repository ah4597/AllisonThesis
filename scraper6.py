#Scrapes by State and Decade, gather only the # of results for each

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import time
url = 'https://chroniclingamerica.loc.gov/search/pages/results/list/?date1=1835&rows=20&searchType=basic&state=Alabama&date2=1950&proxtext=house&y=21&x=23&dateFilterType=yearRange&page=1&sort=relevance'

f = open('./data.csv', 'w', encoding='utf-8')

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District+of+Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New+Hampshire', 'New+Jersey', 'New+Mexico', 'New+York', 'North+Carolina', 'North+Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode+Island', 'South+Carolina', 'South+Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West+Virginia', 'Wisconsin', 'Wyoming']
dates = [
    ['1830', '1839'],
    ['1840', '1849'],
    ['1850', '1859'],
    ['1860', '1869'],
    ['1870', '1879'],
    ['1880', '1889'],
    ['1890', '1899'],
    ['1900', '1909'],
    ['1910', '1919'],
    ['1920', '1929'],
    ['1930', '1939'],
    ['1940', '1949'],
    ['1950', '1959']
]

f.write('States,')
for date in dates:
    f.write(f'{date[0]}-{date[1]},')
f.write('\n')

for state in states:
    f.write(f'{state},')
    for date in dates:
        date1 = date[0]
        date2 = date[1]
        print(f'Running for {state}, {date1}-{date2}')
        url = f'https://chroniclingamerica.loc.gov/search/pages/results/list/?date1={date1}&rows=20&searchType=basic&state={state}&date2={date2}&proxtext=&y=20&x=14&dateFilterType=yearRange&page=1&sort=relevance'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        success = False
        retries = 0
        failure = False
        while not success and retries <= 5:
            try:
                request_page = urlopen(req)
                page_html = request_page.read()
                request_page.close()
                soup = BeautifulSoup(page_html, 'html.parser')
                success = True
            except Exception as e:
                if 'Retry-After' in e.headers:
                    wait = int(e.headers['Retry-After'])
                    success = False
                    print(f'Request limit reached.. Waiting {wait} seconds')
                    time.sleep(wait)
                else:
                    wait = retries * 30
                    print(f'Error occured. Waiting {wait} secs and retrying.')
                    print(e.headers['Retry-After'])
                    time.sleep(wait)
                    success = False
                    retries += 1
        
        if not success and retries > 5:
            failure = True

        soup = BeautifulSoup(page_html, 'html.parser')

        temp =  soup.find('span', class_="results")
        if temp:
            temp = temp.text.split()
            numResults = int(temp[len(temp)-1])
        elif failure:
            numResults = 'Error'
        else:
            numResults = 0

        f.write(f'{numResults},')   
    f.write('\n')
f.close()     

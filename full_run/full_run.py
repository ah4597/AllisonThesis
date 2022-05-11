#Scrape all pages in search
#Analyze word counts - sentiments based on positive and negative words
#Rates sentiment 0-2 (0 = negative, 1 = neutral, 2 = positive), and
#Puts individual counts of each word of each article in an overall spreadsheet to double check if desired.

#Essentially combines (beginning part of) scraper.py and analysis2.py to run without storing all of the articles' texts in memory.

#Scrapes the first page's images and puts the text into files named after their SN#s

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from collections import OrderedDict
import math

MAX_SINCE_SCHOOL = 200
#url = "https://chroniclingamerica.loc.gov/search/pages/results/list/?date1=1835&rows=1500&searchType=basic&state=&date2=1950&proxtext=%28graded+school%29&y=14&x=24&dateFilterType=yearRange&page=1&sort=relevance"
counter = input("What number is this? (If not running parallel, ignore and input nothing)\n> ")
if not counter:
    counter = str(0)
have_links = input("Do you have all the links/dates for the txts already?\n> ")
if have_links == "yes" or have_links == "y":
    have_links = True
    starting_article = input("Do you have a starting article number? Empty = start from beginning.\n> ")
    ending_article = input("Perform analysis up until what # article? (Empty = full (408,025)\n> ")
    if not starting_article:
        starting_article = 0
    else:
        starting_article = int(starting_article) - 1

    if not ending_article:
        ending_article = 408025
    else:
        ending_article = int(ending_article)
if not have_links:
    
    starting_article = 0
    url = input("Enter URL: (If empty, default will be used)\n> ")
    if not url:
        url = "https://chroniclingamerica.loc.gov/search/pages/results/list/?date1=1835&rows=1500&searchType=basic&state=&date2=1950&proxtext=%28graded+school%29&y=14&x=24&dateFilterType=yearRange&page=1&sort=relevance"
    rows = input("How many rows would you like (# of links per page)? Empty = default of link entered\n> ")
    startPage = input("Starting page? Empty = 1\n> ")
    #Make sure it's in list format (I think this will help loading times)
    if url.find("list") < 0:
        url = url[:url.find("results")+8] + "list/" + url[url.find("results")+8:]
    if rows:
        url = url[:url.find("rows")+5] + rows + url[url.find("&searchType"):]
    else:
        rows = url[url.find("rows")+5:url.find("&searchType")]
    if not startPage:
        startPage = 1
    request_page = urlopen(url)
    page_html = request_page.read()
    request_page.close()

    soup = BeautifulSoup(page_html, 'html.parser')
    temp =  soup.find('span', class_="results").text.split()
    numResults = int(temp[len(temp)-1])
    # + 1 because our for loop will start at 1
    numPages = math.ceil(numResults/int(rows)) + 1

    links = []

    #Get all the links on every page
    for i in range(int(startPage), numPages):
        links_current_page = []
        dates_current_page = []
        locs_current_page = []
        uid_current_page = []
        print("Getting links from page " + str(i) + " of " + str(numPages-1))
        url = url[:url.rfind("page")] + "page=" + str(i) + "&sort=relevance"
        request_page = urlopen(url)
        page_html = request_page.read()
        request_page.close()
        soup = BeautifulSoup(page_html, 'html.parser')
        #Get all the links on the current page
        for ultag in soup.find_all('ul', class_="results_list"):
            #print(ultag)
            for litag in ultag.find_all('li'):
                #print(litag)
                for atag in litag.find_all('a'):
                    links.append(atag['href'])
                    links_current_page.append(atag['href'])
                    text = atag.text
                    location = text[text.find("(")+1:text.rfind(")")]
                    date = atag['href'][17:27]
                    dates_current_page.append(date)
                    locs_current_page.append(location)
                    uid_current_page.append(atag['href'][1:27])

        links_txt = open("links.txt", 'a')
        dates_and_locs = open('dates_and_locs.csv', 'a', encoding='utf-8')
        for link in links_current_page:    
            links_txt.write(link + "\n")
        for i in range(0, len(dates_current_page)):
            dates_and_locs.write(locs_current_page[i] +  "," + dates_current_page[i] + "," + uid_current_page[i] + "\n")
        links_txt.close()
        dates_and_locs.close()
        

    print("Done getting links, dates, and locs got a total of: " + str(len(links)))

else:
    link_read = open("links.txt", 'r', encoding="utf-8")
    links = link_read.read().split("\n")
    link_read.close()

#positive_words = ["advancement", "advance", "accomplish", "accomplished", "incentive", "advantage", "best", "better", "quality"]
p_read = open("positive_words.txt", 'r', encoding="utf-8")
positive_words = p_read.read().split()
p_read.close()

#negative_words = ["danger", "dangerous", "evil", "evils", "overstrain", "overstrained"]
n_read = open("negative_words.txt", 'r', encoding="utf-8")
negative_words = n_read.read().split()
n_read.close()

#Create .csv file
analysis = open('analysis_' + str(counter) + '.csv', 'a', encoding="utf-8")
analysis_count = open('analysis_count_' + str(counter) + '.csv', 'a', encoding="utf-8")
error_log = open('error_log_' + str(counter) + '.txt', 'a', encoding="utf-8")



print("Starting analysis...")
#For each link, convert it to the ocr.txt link and perform analysis, and output the results into two files.
for i in range(int(starting_article), int(ending_article)):
#for link in links:
    print("Performing analysis on article " + str(i + 1) + " of " + str(ending_article))
    #Get the url for the individual article's ocr.txt link
    last_paren = links[i].rfind("/") + 1
    link = links[i][:last_paren] + "ocr.txt"
    url = "https://chroniclingamerica.loc.gov" + link
    uid = link[1:27]

    #Get the article's text
    try:
        request_page = urlopen(url)
    except HTTPError as e:
        error_log.write("Article #" + str(i + 1) + "; SN# - " + uid + " encountered error: " + str(e) + "\n")
        analysis.write(uid + ",ERROR\n")
        analysis_count.write(uid + "(ERROR)," + str(i + 1) +"\n___END CURRENT ARTICLE___\n\n")
        print(e)
    except URLError as e:
        error_log.write("Article #" + str(i + 1) + "; SN# - " + uid + " encountered error: " + str(e) + "\n")
        analysis.write(uid + ",ERROR\n")
        analysis_count.write(uid + "(ERROR)," + str(i + 1) +"\n___END CURRENT ARTICLE___\n\n")
        print(e)
    else:
        page_html = request_page.read()
        request_page.close()
        try: 
            soup = str(BeautifulSoup(page_html, 'html.parser'))
        except TypeError as e:
            error_log.write("Article #" + str(i + 1) + "; SN# - " + uid + " encountered error: " + str(e) +"\n")
            analysis.write(uid + ",ERROR")
            analysis_count.write(uid + "(ERROR)," + str(i + 1) +"\n___END CURRENT ARTICLE___\n\n")
            print(e)
        except UnboundLocalError as e:
            error_log.write("Article #" + str(i + 1) + "; SN# - " + uid + " encountered error: " + str(e) +"\n")
            analysis.write(uid + ",ERROR")
            analysis_count.write(uid + "(ERROR)," + str(i + 1) +"\n___END CURRENT ARTICLE___\n\n")
            print(e)
        else:
            #Perform analysis (from analysis2.py)
            positive_word_count = {}
            negative_word_count = {}
            #Buffer to track previous words before we find the first instance of "school". Max size should maybe be 200? 
            buffer = []
            words_since_school = 0
            first_school_found = False
            
            #with open(filepath, 'r', encoding="utf-8") as f:
            #Positivity rating (0 = negative, 1 = neutral 2 = positive)
            positivity_scale = 1

            #Get text, normalize into lowercase and split into array
            text = [word.lower() for word in soup.split()]

            #nsw = no safe words, if we're collecting all words, we don't want "safe words"
            #text_nsw = [word for word in text if not word in stop_words]

            #Collect only negative or positive words
            text_wanted_words = []
            positivity = 0
            negativity = 0
            for word in text:
                #Check if current word is school
                if word == "school":
                    words_since_school = 0
                    #If this is the first occurrence of "school", we need to look at the previous 200 words as well, held inside of 'buffer'
                    if not first_school_found:
                        first_school_found = True
                        #print("Performing on buffer:")
                        for buffer_word in buffer:
                            if buffer_word in positive_words:
                                #print("Positivity currently: " + str(positivity) + ", adding positive word " + buffer_word)
                                positivity = positivity + 1
                                text_wanted_words.append(buffer_word)
                                if buffer_word in positive_word_count:
                                    positive_word_count[buffer_word] = positive_word_count[buffer_word] + 1
                                else:
                                    positive_word_count[buffer_word] = 1
                                #print("Positivity is now: " + str(positivity))
                            elif buffer_word in negative_words:
                                #print("Positivity currently: " + str(positivity) + ", adding negative word " + buffer_word)
                                negativity += 1
                                text_wanted_words.append(buffer_word)
                                if buffer_word in negative_word_count:
                                    negative_word_count[buffer_word] = negative_word_count[buffer_word] + 1
                                else:
                                    negative_word_count[buffer_word] = 1
                                #print("Positivity is now: " + str(positivity))
                        buffer = []
                #If it hasn't been over 200 words since we've seen school, and the first school has been found (we don't want to add any words until we've seen first 'school')
                elif words_since_school <= MAX_SINCE_SCHOOL and first_school_found:
                    if word in positive_words:
                        #print("Positivity currently: " + str(positivity) + ", adding positive word " + word)
                        positivity = positivity + 1
                        text_wanted_words.append(word)
                        if word in positive_word_count:
                            positive_word_count[word] = positive_word_count[word] + 1
                        else:
                            positive_word_count[word] = 1
                        #print("Positivity is now: " + str(positivity))
                    elif word in negative_words:
                        #print("Positivity currently: " + str(positivity) + ", adding negative word " + word)
                        negativity += 1
                        text_wanted_words.append(word)
                        if word in negative_word_count:
                            negative_word_count[word] = negative_word_count[word] + 1
                        else:
                            negative_word_count[word] = 1
                        #print("Positivity is now: " + str(positivity))
                    words_since_school = words_since_school + 1
                    if words_since_school > MAX_SINCE_SCHOOL:
                        break
                elif not first_school_found:
                    if len(buffer) <= 200:
                        buffer.append(word)
                    else:
                        buffer.pop(0)
                        buffer.append(word)
                elif words_since_school > MAX_SINCE_SCHOOL:
                    break
            if positivity - negativity > 0:
                positivity_scale = 2
            elif positivity - negativity < 0:
                positivity_scale = 0

            #Using this to sort the word counts in decending order
            #OrderedDict(sorted(dates.items(), key=lambda x: x[1], reverse=True))

            #Write SN# of current article and positivity score into both files
            #Write positivity score, # of positives, # of negatives, positivity scale
            analysis_count.write(uid + " (" + str(positivity_scale) + "),"+ str(i + 1) + "\n")
            analysis.write(uid + "," + str(positivity_scale) + "," + str(positivity) + "," + str(negativity) + "," + str(positivity - negativity) +  "\n")

            #Sort and place positive words into analysis_count
            analysis_count.write("___Positive Words____\n")
            positive_word_count = OrderedDict(sorted(positive_word_count.items(), key=lambda x: x[1], reverse=True))
            for word in positive_word_count:
                analysis_count.write('\"' + str(word) + '\",' + str(positive_word_count[word]) + '\n')

            #Sort and place negative words into analysis_count
            analysis_count.write("___Negative Words____\n")
            negative_word_count = OrderedDict(sorted(negative_word_count.items(), key=lambda x: x[1], reverse=True))
            for word in negative_word_count:
                analysis_count.write('\"' + str(word) + '\",' + str(negative_word_count[word]) + '\n')
            analysis_count.write("___END CURRENT ARTICLE___\n\n")

error_log.close()
analysis.close()
analysis_count.close()
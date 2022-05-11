#Takes texts from .txt file and counts how many times each word appears into a .csv

import os
import collections
from collections import OrderedDict
#import nltk
#from nltk.corpus import stopwords

#import pandas as pd
#import matplotlib.pyplot as plt

#stop_words = set(stopwords.words('english'))

#positive_words = ["advancement", "advance", "accomplish", "accomplished", "incentive", "advantage", "best", "better", "quality"]
p_read = open("positive_words.txt", 'r')
positive_words = p_read.read().split()
p_read.close()

#negative_words = ["danger", "dangerous", "evil", "evils", "overstrain", "overstrained"]
n_read = open("negative_words.txt", 'r')
negative_words = n_read.read().split()
n_read.close()

totalfile = open("analysis/overall_analysis.csv", 'w', encoding="utf-8")
totalfile.write("File Name/Article ID, Positivity Rating\n")


for subdir, dirs, files in os.walk(r'F:\\ProgramStuff\\Projects\\AllisonThesis\\texts'):
    print("Running analysis on " + str(len(files)) + " files.")
    for filename in files:
        print("Running on file #" + str(files.index(filename) + 1) + ", file name: " + filename + ".")
        filepath = subdir + os.sep + filename

        positive_word_count = {}
        negative_word_count = {}
        #Buffer to track previous words before we find the first instance of "school". Max size should maybe be 200? 
        buffer = []
        words_since_school = 0
        first_school_found = False
        
        with open(filepath, 'r', encoding="utf-8") as f:
            #Positivity rating (0 = negative, 1 = neutral 2 = positive)
            positivity_scale = 1

            #Get text, normalize into lowercase and split into array
            text = f.read()
            text = [word.lower() for word in text.split()]

            #nsw = no safe words, if we're collecting all words, we don't want "safe words"
            #text_nsw = [word for word in text if not word in stop_words]

            #Collect only negative or positive words
            text_wanted_words = []
            positivity = 0
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
                                positivity = positivity - 1
                                text_wanted_words.append(buffer_word)
                                if buffer_word in negative_word_count:
                                    negative_word_count[buffer_word] = negative_word_count[buffer_word] + 1
                                else:
                                    negative_word_count[buffer_word] = 1
                                #print("Positivity is now: " + str(positivity))
                        buffer = []
                #If it hasn't been over 200 words since we've seen school, and the first school has been found (we don't want to add any words until we've seen first 'school')
                elif words_since_school <= 200 and first_school_found:
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
                        positivity = positivity - 1
                        text_wanted_words.append(word)
                        if word in negative_word_count:
                            negative_word_count[word] = negative_word_count[word] + 1
                        else:
                            negative_word_count[word] = 1
                        #print("Positivity is now: " + str(positivity))
                    words_since_school = words_since_school + 1
                    if words_since_school > 200:
                        break
                elif not first_school_found:
                    if len(buffer) <= 200:
                        buffer.append(word)
                    else:
                        buffer.pop(0)
                        buffer.append(word)
            if positivity > 0:
                positivity_scale = 2
            elif positivity < 0:
                positivity_scale = 0

            #Separate the words into a counter (word: count)
            #counts = collections.Counter(text_wanted_words)
            #most_common = counts.most_common(30)

            #print(text_wanted_words)
            print(positivity)
            # #Create .csv file, put in headers
            file_name = 'analysis/' + filepath[filepath.rfind('\\')+1:len(filepath)-4] + ' (' + str(positivity_scale) + ').csv'
            f1 = open(file_name, 'w', encoding="utf-8")
            headers = "Word, Count\n"
            f1.write(headers) 

            #OrderedDict(sorted(dates.items(), key=lambda x: x[1], reverse=True))

            positive_word_count = OrderedDict(sorted(positive_word_count.items(), key=lambda x: x[1], reverse=True))
            for word in positive_word_count:
                f1.write('\"' + str(word) + '\",' + str(positive_word_count[word]) + '\n')
            f1.write("_____,_____\n")
            negative_word_count = OrderedDict(sorted(negative_word_count.items(), key=lambda x: x[1], reverse=True))
            for word in negative_word_count:
                f1.write('\"' + str(word) + '\",' + str(negative_word_count[word]) + '\n')
            #print(most_common)
            f1.close()
            totalfile.write(filepath[filepath.rfind('\\')+1:len(filepath)-4] + "," + str(positivity_scale) + "\n")
totalfile.close()




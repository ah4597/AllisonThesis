#Takes texts from .txt file and counts how many times each word appears into a .csv

import os
import collections
import nltk
from nltk.corpus import stopwords

import pandas as pd
import matplotlib.pyplot as plt

stop_words = set(stopwords.words('english'))
""" with open ('analysis/stop_words.txt', 'w', encoding="utf-8") as f2:
    for word in stop_words:
        f2.write(word + '\n') """

for subdir, dirs, files in os.walk(r'F:\ProgramStuff\Projects\AllisonThesis\texts'):
    for filename in files:
        filepath = subdir + os.sep + filename

        with open(filepath, 'r', encoding="utf-8") as f:
            
            file_name = 'analysis/' + filepath[filepath.rfind('\\')+1:len(filepath)-4] + '.csv'
            f1 = open(file_name, 'w', encoding="utf-8")
            headers = "Word, Count\n"
            f1.write(headers)

            text = f.read()
            text = [word.lower() for word in text.split()]
            text_nsw = [word for word in text if not word in stop_words]
            counts = collections.Counter(text_nsw)

            most_common = counts.most_common(30)

            for word in most_common:
                f1.write('\"' + str(word[0]) + '\",' + str(word[1]) + '\n')
            #print(most_common)
            f1.close()



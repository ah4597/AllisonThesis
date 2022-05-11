from collections import OrderedDict

total_analysis = open('total_analysis.csv', 'w', encoding='utf-8')
dates_and_locs_read = open('dates_and_locs.csv', 'r', encoding='utf-8')
analysis_read = open('analysis_0.csv', 'r', encoding='utf-8')

dates_and_locs = dates_and_locs_read.read().split("\n")
analysis = analysis_read.read().split("\n")

headers = "year,location,overall score,# of positive,# of negative,difference positive-negative,uniqueID\n"
total_analysis.write(headers)

#Analysis and dates_and_locs should be same length
for i in range(0, len(analysis)):
#for i in range(0, 2):
    print("Combining article " + str(i) +  " of " + str(len(analysis)))
    #Want format:
    #DATE, LOCATION, OVERALL SCORE, #POS, #NEG, DIFFERENCE, UID
    len_dnl = len(dates_and_locs[i])
    
    #year = -37:-33, full date = -37:-27
    year = dates_and_locs[i][len_dnl-37:len_dnl-33]
    location = dates_and_locs[i][:len_dnl-38]
    
    analysis_split = analysis[i].split(",")

    if(len(analysis_split) >= 3):
        overall_score = 1
        num_pos = analysis_split[2]
        num_neg = analysis_split[3]
        difference = analysis_split[4]
        if int(num_pos) - int(num_neg) > 0:
            overall_score = 2
        elif int(num_pos) - int(num_neg) < 0:
            overall_score = 0
        nums = str(overall_score) + "," + num_pos + "," + num_neg + "," + difference
    else:
        nums = "ERROR"

    uid = analysis_split[0]

    #print(year + "," + location + "," + nums + "," + uid)
    total_analysis.write(year + ",\"" + location + "\"," + nums + "," + uid + "\n")
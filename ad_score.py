import csv
import datetime

#filename variables
#clicks_train contains 87,141,732
datafilein = 'clicks_train.csv'
testfilein = 'clicks_test.csv'
datafileout = 'submission.csv'
#prints the start time for the script for runtime monitoring
print(datetime.datetime.now().time())

#initialize list variables
display = {}
ad = {}

#In each case I use i as the iterator for the data files
#i[0] is the display_id
#i[1] is the ad_id
#i[2] is the clicked variable ('1' = clicked; '0' = not clicked)
with open(datafilein, 'r') as filedata:
    data = csv.reader(filedata)
    next(data, None)
    for i in data:
        #sums the number of ads in a display
        #key = display_id
        #display[key][0] = clicked ad for the display, initialized as ''
        #display[key][1] = number of ads in a display
        try:
            display[i[0]][1] += 1
        except KeyError:
            display[i[0]] = ['',1]
        #sums the number of times the ad appears in the training dataset
        #key = ad_id
        #ad[key][2] = number of times the ad appears in the training dataset
        try:
            ad[i[1]][2] += 1
        except KeyError:
            ad[i[1]] = [0,0,1,0,0]
        #if ad was clicked:
        if i[2] == '1':
            #key = display_id
            #display[key][0] = clicked ad for the display
            display[i[0]][0] = i[1]
            #sums the number of times the ad was clicked
            #key = ad_id
            #ad[key][1] = number of times the ad was clicked
            ad[i[1]][1] += 1

#scores the proportion of times the ad was clicked
#clicked/number of appearances
for key in ad:
    ad[key][0] = ad[key][1]/ad[key][2]

print("Cycle 1 complete")
print(datetime.datetime.now().time())

with open(datafilein, 'r') as filedata:
    data = csv.reader(filedata)
    next(data, None)
    for i in data:
        outof = display[i[0]][1]
        #sums the total number of ads that appeared with this ad throughout
        #the training data set
        #key = ad_id
        #ad[key][3] = total number of ads appeared with (think total marbles in the jar)
        ad[i[1]][3] += outof
        #produces the probability that the ad would never be picked
        #key = ad_id
        #ad_id[key][4] = probability that the ad would never be picked
        if ad[i[1]][4] == 0:
            ad[i[1]][4] = (outof-1)/outof
        else:
            ad[i[1]][4] *= (outof-1)/outof

minimum = 0

for key in ad:
    #if ad was never picked,
    #its score is negative(1-prob that it would never be picked)
    #this makes scores for ads that were never picked < 0
    #with negative scores further left on numberline for ads that appeared more often
    if ad[key][1] == 0:
        ad[key][0] = -(1-ad[key][4])
    #if the ad was picked at least once:
    #it's score is the proportion of times it was picked minus
    #the probability of being picked completely at random
    #key = ad_id
    #ad[key][0] = ad score
    #ad[key][2] = total ad appearances (number of blue marbles)
    #ad[key][3] = total number of ads appearing with this ad (total marbles in jar)
    else:
        ad[key][0] = ad[key][0] - (ad[key][2]/ad[key][3])
        #determines ad score with the lowest value for ads that one at least once
        if ad[key][0] < minimum:
            minimum = ad[key][0]

for key in ad:
    if ad[key][1] != 0:
        #ads the absolute value of minimum to all ads that won at least once
        #this makes all ads that were clicked at least once >= 0
        ad[key][0] += abs(minimum)

print("Ads Scored")
print(datetime.datetime.now().time())

t_display = {}

#reads the test file
with open(testfilein, 'r') as filedata:
    data = csv.reader(filedata)
    next(data, None)
    for i in data:
        #ads that never appear in the training set are given an ad_score of 0
        try:
            ad[i[1]]
        except:
            ad[i[1]] = [0,0]
        #creates a list of tuples with (ad score, ad_id) for each display_id
        try:
            t_display[i[0]] += [(ad[i[1]][0],i[1])]
        except KeyError:
            t_display[i[0]] = [(ad[i[1]][0],i[1])]

print(str(len(ad)) + " ads scored")
print(str(len(t_display)) + " test displays scored")
print(datetime.datetime.now().time())

display_list = []
for key in t_display:
    #sorts the list of tuples by ad score in decending order:
    #ads with higher scores are more likely to be clicked
    t_display[key] = [x[1] for x in sorted(t_display[key],reverse=True)]
    #creates a list of tuples with (display_id,list of sorted ads for display)
    display_list += [(int(key),t_display[key])]

#sorts the displays in acending order because
#displays became unordered in the dictionary
display_list = sorted(display_list)

print("displays sorted")
print(datetime.datetime.now().time())

headlist = ["display_id","ad_id"]
with open(datafileout, 'w', newline = '') as datafile:
        csvfile = csv.writer(datafile)
        #writes headers to file
        csvfile.writerow(headlist)
        for x in display_list:
            #writes each display line to file
            csvfile.writerow([x[0]," ".join(x[1])])
#prints the script run end time
print(datetime.datetime.now().time())




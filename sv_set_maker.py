#for standard validation
#this script creates a random training set and the corresponding test set and
#outputs them to files to be input in ad_score.py
import csv
import datetime
import random

#filename variables
#clicks_train contains 87,141,732 rows
datafilein = 'clicks_train.csv'
trainfileout = 'training_set.csv'
testfileout = 'test_set.csv'
#prints the start time for the script for runtime monitoring
print(datetime.datetime.now().time())

#initialize list variables
display = {}
ad = {}

with open(datafilein, 'r') as filedata:
    data = csv.reader(filedata)
    next(data, None)
    for i in data:
        display[i[0]] = -1

print("Cycle 1 complete")
print(datetime.datetime.now().time())

#generate random assignments
display_count = len(display)
validate = round(display_count*.9)
rand_pick = ((display_count - validate) * [0]) + (validate * [1])
random.shuffle(rand_pick)

print("Random assignments generated")
print(datetime.datetime.now().time())

rand_count = 0
valid_data = []

for key in display:
    display[key] = rand_pick[rand_count]
    rand_count += 1

print("Random assignments assigned")
print(datetime.datetime.now().time())

with open(datafilein, 'r') as filedata:
    data = csv.reader(filedata)
    next(data, None)
    headlist = ["display_id","ad_id","clicked"]
    with open(trainfileout, 'w', newline = '') as trainfile:
        csvfile1 = csv.writer(trainfile)
        #writes headers to file
        csvfile1.writerow(headlist)
        with open(testfileout, 'w', newline = '') as testfile:
            csvfile2 = csv.writer(testfile)
            #writes headers to file
            csvfile2.writerow(headlist)
            for i in data:
                if display[i[0]] == 1:
                    csvfile1.writerow([i[0],i[1],i[2]])
                else:
                    csvfile2.writerow([i[0],i[1],i[2]])

print("Training File Created")
print(datetime.datetime.now().time())








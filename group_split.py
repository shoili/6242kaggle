import csv
import datetime

#filename variables
#clicks_train contains 87,141,732
datafilein = 'clicks_train.csv'
testfilein = 'clicks_test.csv'
eventfilein = 'events.csv'
trainfileout = 'gp_train'
testfileout = 'gp_test'
group_names = ["1","2"]
#prints the start time for the script for runtime monitoring
print(datetime.datetime.now().time())

display ={}

with open(eventfilein, 'r') as filedata:
        data = csv.reader(filedata)
        next(data, None)
        for i in data:
            display[i[0]] = i[4]
#initialize list variables
group_data = {}
print(datetime.datetime.now().time())
for gp in group_names:
    group_data[gp+"train"] = []
    group_data[gp+"test"] = []
    with open(datafilein, 'r') as filedata:
        data = csv.reader(filedata)
        next(data, None)
        for i in data:
            if gp != '2':
                if display[i[0]] != '2':
                    group_data[gp+"train"] += [[i[0],i[1],i[2]]]
            else:
                if display[i[0]] == '2':
                    group_data[gp+"train"] += [[i[0],i[1],i[2]]]
    print(datetime.datetime.now().time())
    with open(testfilein, 'r') as filedata:
        data = csv.reader(filedata)
        next(data, None)
        for i in data:
            if gp != '2':
                if display[i[0]] != '2':
                    group_data[gp+"test"] += [[i[0],i[1]]]
            else:
                if display[i[0]] == '2':
                    group_data[gp+"test"] += [[i[0],i[1]]]
    print(datetime.datetime.now().time())

    with open(trainfileout+gp+".csv", 'w', newline = '') as trainfile:
        csvfile1 = csv.writer(trainfile)
        headlist = ["display_id","ad_id","clicked"]
        csvfile1.writerow(headlist)
        for i in group_data[gp+"train"]:
            csvfile1.writerow([i[0],i[1],i[2]])
    with open(testfileout+gp+".csv", 'w', newline = '') as testfile:
        csvfile1 = csv.writer(testfile)
        headlist = ["display_id","ad_id","clicked"]
        csvfile1.writerow(headlist)
        for i in group_data[gp+"test"]:
            csvfile1.writerow([i[0],i[1]])
    print(datetime.datetime.now().time())
    group_data[gp+"train"] = []
    group_data[gp+"test"] = []
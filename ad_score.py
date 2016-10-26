import csv
import datetime

#filename variables
#clicks_train contains 87,141,732 rows
datafilein = 'clicks_train.csv'
testfilein = 'clicks_test.csv'
datafileout = 'submission.csv'
#prints the start time for the script for runtime monitoring
print(datetime.datetime.now().time())

#initialize list variables
display = {}
ad = {}
count = 0

with open(datafilein, 'r') as filedata:
    data = csv.reader(filedata)
    for i in data:
        if count != 0:
            try:
                display[i[0]][1] += 1
            except KeyError:
                display[i[0]] = ['',1]
            try:
                ad[i[1]][1] += 1
            except KeyError:
                ad[i[1]] = [0,1,0]
            if i[2] == '1':
                display[i[0]][0] = i[1]
                ad[i[1]][2] += 1
        count += 1
        #if count%10000000 == 0:
        #    print(count)
print("Cycle 1 complete")
print(datetime.datetime.now().time())

count = 0

with open(datafilein, 'r') as filedata:
    data = csv.reader(filedata)
    for i in data:
        if count != 0:
            prob = 1/display[i[0]][1]
            if i[2] == '1':
                ad[i[1]][0] += prob
            #else:
                #ad[i[1]][0] += prob
        count += 1
        #if count%10000000 == 0:
        #    print(count)
        #    print(datetime.datetime.now().time())

print("Cycle 2 complete")
print(datetime.datetime.now().time())

for key in ad:
    if ad[key][2] == 0:
        ad[key] = -ad[key][1]
    else:
        ad[key] = ad[key][0] * (ad[key][2]/ad[key][1])

print(str(len(ad)) + " ads scored")
print(str(len(display)) + " displays scored")
print(datetime.datetime.now().time())

count = 0
t_display = {}

with open(testfilein, 'r') as filedata:
    data = csv.reader(filedata)
    for i in data:
        if count != 0:
            try:
                ad[i[1]]
            except:
                ad[i[1]] = -1000000
            try:
                t_display[i[0]] += [(ad[i[1]],i[1])]
            except KeyError:
                t_display[i[0]] = [(ad[i[1]],i[1])]
        count += 1

print(str(len(ad)) + " ads scored")
print(str(len(t_display)) + " test displays scored")
print(datetime.datetime.now().time())

display_list = []
for key in t_display:
    t_display[key] = [x[1] for x in sorted(t_display[key],reverse=True)]
    display_list += [(int(key),t_display[key])]

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

#with open(datafileout, 'w', newline = '') as datafile:
#        writer = csv.writer(datafile)
#        for key, value in ad.items():
            #writes each display line to file
#            writer.writerow([key,value])
#254136 ads scored

#prints the script run end time
#print(datetime.datetime.now().time())



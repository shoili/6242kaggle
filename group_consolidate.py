import csv
import datetime

testfilein = 'clicks_test.csv'
subfilesin = 'gp_submission'
submissionout = 'submission.csv'
group_names = ["1","2"]
#prints the start time for the script for runtime monitoring
print(datetime.datetime.now().time())

display ={}

for gp in group_names:
    with open(subfilesin + gp + '.csv', 'r') as filedata:
        data = csv.reader(filedata)
        next(data, None)
        for i in data:
            display[i[0]] = i[1]

display_list = []
for key in display:
    display_list += [(int(key),display[key])]

display_list = sorted(display_list)


headlist = ["display_id","ad_id"]
with open(submissionout, 'w', newline = '') as trainfile:
    csvfile1 = csv.writer(trainfile)
    #writes headers to file
    csvfile1.writerow(headlist)
    for i in display_list:
        csvfile1.writerow([i[0],i[1]])


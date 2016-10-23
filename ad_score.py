import csv
import datetime

#open files and parse observations as a list of lists
def get_obs(filename):
    #read file
    with open(filename, 'r') as filedata:
        data = csv.reader(filedata)
        #skip header
        next(data, None)
        #create a list containing a list of each observation
        obs = [line for line in data]
        #remove data from memory
        del data
    return obs

#ad score function
def score_ads(obs):
    #initialize dictionary variables
    ad_score = {}
    display_score = {}
    #initialize scoring variables
    numerator = 0
    denominator = 0
    #initialize flag variables
    equal_values = 0
    not_equal = 1
    #count is just for keeping up with iterations while script is running
    count = 0
    while equal_values == 0:
        #iterate with numbers to reference more than one list object at a time
        for i in range(len(obs)):
            numerator += 1
            denominator += 1
            #establish winning ad for this display
            if obs[i][2] == '1':
                winner = obs[i][1]
            else:
                #add previous ad scores to numerator for ads that did not win
                #in this display
                if obs[i][1] in ad_score.keys():
                    numerator += ad_score[obs[i][1]]
            #calculations occur at the last display item
            if i == len(obs)-1 or obs[i][0] != obs[i+1][0]:
                #score the display
                #numerator is the sum of the observations in this display plus
                #ad scores for ads that did not win this display
                #denominator is the sum of the observations in this display
                new_score = numerator/denominator
                #reset scoring variables
                numerator = 0
                denominator = 0
                #check if display has been scored already,
                #meaning that it would be at least the second iteration
                if obs[i][0] in display_score.keys():
                    #subtract the old display score from the ad score total
                    ad_score[winner] -= display_score[obs[i][0]]
                    #check if the new score matches the old score within
                    #2 decimal places
                    if str(round(new_score,2)) != str(round(display_score[obs[i][0]],2)):
                        #if they do not match reset the not equal flag
                        not_equal = 1
                #set the display score to the new score to be compared in the
                #next iteration
                display_score[obs[i][0]] = new_score
                #add display score to ad's total score
                if winner in ad_score.keys():
                    ad_score[winner] += new_score
                else:
                    ad_score[winner] = new_score
        #if all of the new ad scores match the old ad score within 2 decimals
        #the not_equal flag will be set to 0. not_equal is set to 0 below
        if not_equal == 0:
            #equal_values flag ends the while loop
            equal_values = 1
        #not_equal set to zero. it will be set to 1 in the next iteration if
        #any of the new scores do not match the old scores within 2 dec.
        not_equal = 0
        #these prints are to keep up with the progress of the script while
        #it is running
        print(datetime.datetime.now().time())
        count += 1
        print(count)
    #returns a list of ad ids sorted by the ad values
    return sorted(ad_score, key = ad_score.get)

#creates lines to write to submission.csv
def create_lines(obs,score_sorted):
    #initialize list variables
    display = []
    ads = []
    ads_order = []
    for i in range(len(obs)):
        #append ad observations in the same display group
        ads.append(obs[i][1])
        #append ad scores for ads that were scored. if an ad was not scored
        #this means that it was never clicked in the training group
        if obs[i][1] in score_sorted:
            ads_order.append(score_sorted.index(obs[i][1]))
        else:
            #append 0 for ads that were not scored
            ads_order.append(0)
        #checks if this is the last ad in a display group
        if i == len(obs)-1 or obs[i][0] != obs[i+1][0]:
            #sorts ad scores in descending order, returns a list of ad ids in
            #the order of their ad scores. for instance, ad A has a score of
            #3.2, and ad B has a score of 4.1...linelist = [B,A]
            linelist = [x for (y,x) in sorted(zip(ads_order,ads), reverse = True)]
            #formats each line as a string for output as follows
            #display_id,ad_ids <- separated by spaces as required by Kaggle
            line = obs[i][0] + "," + " ".join(linelist)
            #appends these output lines to display list
            display.append(line)
            #resets list variables for next display group
            ads = []
            ads_order = []
    #returns a list of strings in correct format ready for output to file
    return display

#filename variables
#clicks_train contains 58,613,961 observations and takes about 30 mins to load
#and parse into observations
datafilein = 'clicks.csv'
#clicks_test contains 32,225,162 observations and takes about ? mins to load
#and parse into observations
testfilein = 'clicks2.csv'
datafileout = 'submission.csv'
#prints the start time for the script for runtime monitoring
print(datetime.datetime.now().time())
#gets obs for the training file
obs = get_obs(datafilein)
print("datafilein")
print(datetime.datetime.now().time())
#remove obs from memory
#print("deleting obs")
#print(datetime.datetime.now().time())
#del obs
#print("read test file")
#print(datetime.datetime.now().time())
#gets obs for the test file
obs2 = get_obs(testfilein)
print("testfilein")
print(datetime.datetime.now().time())
#scores the training set
score_sorted = score_ads(obs)
print("scores sorted")
print(datetime.datetime.now().time())
#gets lines to output
display = create_lines(obs2,score_sorted)
print("lines created")
print(datetime.datetime.now().time())
#initialize header variable
headlist = ["display_id","ad_id"]
with open(datafileout, 'w', newline = '') as datafile:
        csvfile = csv.writer(datafile)
        #writes headers to file
        csvfile.writerow(headlist)
        for i in display:
            #writes each display line to file
            datafile.write(i + "\n")
#prints the script run end time
print(datetime.datetime.now().time())
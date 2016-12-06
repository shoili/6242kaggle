import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import xgboost
import gc
from sklearn.externals import joblib

#testing=False
filename = 'xgb_trainall'
#print ("Get tables to combine")
# content = pd.read_csv('promoted_content.csv')
#print('Done combining')

train1 = pd.read_csv('clicks_train_joined1.csv') #Load data ,iterator=True,chunksize=chunksize
train2 = pd.read_csv('clicks_train_joined2.csv')
# train = train1.concat(train2)
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))
train2 = pd.read_csv('clicks_train_joined3.csv')
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))
train2 = pd.read_csv('clicks_train_joined4.csv')
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))
train2 = pd.read_csv('clicks_train_joined5.csv')
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))
train2 = pd.read_csv('clicks_train_joined6.csv')
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))
train2 = pd.read_csv('clicks_train_joined7.csv')
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))
train2 = pd.read_csv('clicks_train_joined8.csv')
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))
train2 = pd.read_csv('clicks_train_joined9.csv')
train1 = train1.append(train2)
del train2
gc.collect()
print(len(train1))

print( 'Training')
predictors=[x for x in train1.columns if x not in ['display_id','clicked', 'entity_id']]
predictors = ['ad_id', 'document_id', 'campaign_id', 'advertiser_id', 'source_id', 'publisher_id', 'publish_year', 'publish_month', 'category_id', 'topic_id']
	# chunk=chunk.fillna(0.0)
train1=train1.fillna(0.0)
# alg = RandomForestClassifier(random_state=1, n_estimators=3, min_samples_split=4, min_samples_leaf=2, warm_start=True)
alg = xgboost.XGBClassifier()
# alg = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(3,3,2), random_state=1)
alg.fit(train1[predictors], train1["clicked"])#Fit the Algorithm
#	if testing:
#		break

#train=''
del train1
gc.collect()

print('Testing')
test= pd.read_csv('clicks_test_joined1.csv') #Load data ,iterator=True,chunksize=chunksize
test2= pd.read_csv('clicks_test_joined2.csv')
test = test.append(test2)
del test2
gc.collect()
test2= pd.read_csv('clicks_test_joined3.csv')
test = test.append(test2)
del test2
gc.collect()
test2= pd.read_csv('clicks_test_joined4.csv')
test = test.append(test2)
del test2
gc.collect()
test2= pd.read_csv('clicks_test_joined5.csv')
test = test.append(test2)
del test2
gc.collect()
#predY=[]
'''
for chunk in test:
	init_chunk_size=len(chunk)
	# chunk=pd.merge(chunk,content,how='left',on='ad_id')
	chunk=chunk.fillna(0.0)
	test=test.fillna(0.0)
	chunk_pred=list(alg.predict_proba(chunk[predictors]).astype(float)[:,1])
	predY += chunk_pred
	if testing:
		break
print('Done Testing')
'''
test=test.fillna(0.0)
test_pred=list(alg.predict_proba(test[predictors]).astype(float)[:,1])
test2 = test.ix[:, 0:2]
results=pd.concat((test2,pd.DataFrame(test_pred)) ,axis=1,ignore_index=True)
# results.drop_duplicates(inplace=True)
# results = results.ix[:, 0:2]

print(results.head(10))
results.columns = ['display_id','ad_id','clicked']#Rename the columns

results.sort_values(['display_id','clicked'], inplace=True, ascending=False)
subm = results.groupby('display_id').ad_id.apply(lambda x: " ".join(map(str,x))).reset_index()

#results=results[results['clicked'] > 0.0]
#results = results.sort_values(by=['display_id','clicked'], ascending=[True, False])
#results = results.reset_index(drop=True)
#results=results[['display_id','ad_id']].groupby('display_id')['ad_id'].agg(lambda col: ' '.join(map(str,col)))
# results.columns=['display_id','ad_id']

results.to_csv(filename+'.csv', header=True)	#

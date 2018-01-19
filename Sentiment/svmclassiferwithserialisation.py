import pandas as pd 
import numpy as np
import pickle
load=pd.read_csv('res.csv',delimiter=',',skipinitialspace=True)
feature_cols_train=['negative_word_count','positive_word_count','vander_score','happ_score']
X=load[feature_cols_train]
y=load.Sentiment
loadtest=pd.read_csv('res.csv',delimiter=',',skipinitialspace=True)
feature_cols_test=['negative_word_count','positive_word_count','vander_score','happ_score']
name=[loadtest.happ_score]
from sklearn.svm import SVC
clf = SVC()
clf.fit(X, y) 
predictions=clf.predict(loadtest[feature_cols_test])

docid_with_sentiment = dict()
for i,j in zip(predictions,loadtest["doc_id"]):
    docid_with_sentiment[j]=i
    
#print(docid_with_sentiment)

output = open('serialisedata.pkl', 'wb')
pickle.dump(docid_with_sentiment, output)
output.close()    
        
pkl_file = open('serialisedata.pkl', 'rb')
read_serialisedata = pickle.load(pkl_file) 

#print(read_serialisedata)
if read_serialisedata['1997595.json.html']==read_serialisedata['1997861.json.html']:
    print("same")
else:
    print("different")

import pandas as pd 
load=pd.read_csv('train.csv',delimiter=',',skipinitialspace=True)
feature_cols_train=['nltksscore','happyscore','positive','negative']
X=load[feature_cols_train]
y=load.sentiment
loadtest=pd.read_csv('test.csv',delimiter=',',skipinitialspace=True)
feature_cols_test=['nltksscore','happyscore','positive','negative']
from sklearn.svm import SVC
clf = SVC()
clf.fit(X, y) 
predictions=clf.predict(loadtest[feature_cols_test])
pd.DataFrame(predictions, columns=['predictions']).to_csv('prediction.csv')

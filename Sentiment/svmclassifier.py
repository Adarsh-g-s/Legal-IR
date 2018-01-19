import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm
load=pd.read_csv('res.csv',delimiter=',',skipinitialspace=True)
feature_cols_train=['negative_word_count','positive_word_count','vander_score','happ_score']
X=load[feature_cols_train]
y=load.Sentiment
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
clf.score(X_test, y_test) 

import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import preprocessing
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_validate
from sklearn.metrics import recall_score
from sklearn.externals import joblib


load=pd.read_csv('..\\DATA\\trainingdata_final.csv',delimiter=',',skipinitialspace=True)

feature_cols_train=['negative_word_count','positive_word_count','vander_score']#happiness_score excluded

X=load[feature_cols_train]
y=load.Sentiment

X = X.as_matrix()
y = y.as_matrix()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)


clf = svm.SVC(kernel='rbf', C=1.7,gamma=2,random_state=2,cache_size=500,class_weight='balanced')
#clf2 = svm.SVC(kernel='linear', C=20,random_state=2).fit(X_train,y_train)

#print(clf2.score(X_test, y_test))

#cross-validation

rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=10,random_state=589)

scores = cross_val_score(clf, X, y, cv=rskf,scoring='accuracy')
#scoring = 'f1_weighted'
#scoring = ['precision_macro', 'recall_macro','accuracy']
#scores = cross_validate(clf, X, y, scoring=scoring,cv=rskf, return_train_score=False)
print(scores)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
clf2 = clf.fit(X, y)
#print(clf2.score(X_test, y_test))

joblib.dump(clf2, 'svmClasifier.pkl')
#clf = joblib.load('svmClasifier.pkl')
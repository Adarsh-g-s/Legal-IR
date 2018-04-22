'''
Created on Mar 14, 2018

@author: adarsh
'''
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import nltk
from bs4 import BeautifulSoup
#nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

class Baseline:

    def __init__(self,vocabulary,corpus):
        self.vocabulary = vocabulary
        self.corpus = corpus
    
    def dataPreProcessing(self,fileContents,corpus):
        #Search for all non-letters, replace all non-letters with spaces
        fileContents=fileContents.lower()
        fileContents=fileContents.split()
        ps=PorterStemmer()
        fileContents=[ps.stem(word) for word in fileContents if not word in set(stopwords.words('english'))]
        fileContents = ' '.join(fileContents)
        corpus.append(fileContents)
        return corpus
    
    def visitPath(self,filePath):
        #Extracting html contents
        fRead = open(filePath,'r',encoding="utf8")
        fileContents = fRead.read()
        return fileContents

# Importing the dataset for training
dataset1 = pd.read_csv('NaiveBayes.csv' ,  encoding='cp437')
#iloc is integer location based indexing for selection by position -> Data Frame
filePaths=dataset1.iloc[:,0].values

baseline = Baseline(vocabulary = [],corpus= []) 
#An array of file path is returned. Extract this file path one by one
for i in range(0,101):
    filePath = filePaths[i]
    #Visit the path and extract contents
    baseline.vocabulary = baseline.visitPath(filePath)
    #Consider only contents from a specific html tag and not all tags
    htmlContents = BeautifulSoup(baseline.vocabulary,'lxml')
    #Extract all contents from the paragraph tag.
    fileContents = " "
    for i,html in enumerate(htmlContents.find_all('p')):
        fileContents += html.text
    
    #1. Give this content for data pre-processing
    
    baseline.corpus = baseline.dataPreProcessing(fileContents,baseline.corpus)
    #2. after that use classifier for training and testing.
    #sparse representation of counts for max 3000 words   
    countVectorizer=CountVectorizer(max_features=600)
    #return the term document matrix
    x=countVectorizer.fit_transform(baseline.corpus).toarray()
    #print(x)

print(x)
#Encode label with values
label=dataset1.iloc[:,1].values
print(label)
labelEncoder=LabelEncoder()
y=labelEncoder.fit_transform(label)   
 
    # Splitting the dataset into the Training set and Test set, 80%-20% for cross validation
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 23,shuffle = False)
          
    
classifier=GaussianNB()
#Classifier learning 
classifier.fit(X_train,y_train)

#Classifier prediction
predictedLabel=classifier.predict(X_test)
print(predictedLabel)
    
#y_test assumed to be the true label.
print('Accuracy score: {}'.format(accuracy_score(y_test, predictedLabel)))


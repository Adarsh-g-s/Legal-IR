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
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score

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
    
    def featureExtraction(self,numberOfFiles,filePaths,x_tf_idf):
        for i in range(0,numberOfFiles):
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
            countVectorizer=CountVectorizer(max_features=1500)
            #return the term document matrix
            x_tf_idf=countVectorizer.fit_transform(baseline.corpus).toarray()
        return x_tf_idf
    
    def extractLabels(self,dataset):
        #Encode label with values
        label=dataset.iloc[:,1].values
        print(label)
        labelEncoder=LabelEncoder()
        y_label=labelEncoder.fit_transform(label) 
        return y_label

# Importing the dataset for training
dataset1 = pd.read_csv('naivetrain.csv' ,  encoding='cp437')
#iloc is integer location based indexing for selection by position -> Data Frame
filePaths1=dataset1.iloc[:,0].values

baseline = Baseline(vocabulary = [],corpus= []) 
#An array of file path is returned. Extract this file path one by one
numberOfFiles = 78
x_tf_idf = []
x_train_tf_idf = baseline.featureExtraction(numberOfFiles,filePaths1,x_tf_idf)

print(x_train_tf_idf)
#Encode label with values
y_train_label = baseline.extractLabels(dataset1)
 
    
classifier=MultinomialNB()
#Classifier learning 
classifier.fit(x_train_tf_idf,y_train_label)

# Importing the dataset for testing
dataset2 = pd.read_csv('naivetest.csv' ,  encoding='cp437')
#iloc is integer location based indexing for selection by position -> Data Frame
filePaths2=dataset2.iloc[:,0].values

numberOfFiles = 23
x_tf_idf = []
baseline = Baseline(vocabulary = [],corpus= []) 
x_test_tf_idf = baseline.featureExtraction(numberOfFiles,filePaths2,x_tf_idf)
    
print(x_test_tf_idf)
#Encode label with values
y_test_label=baseline.extractLabels(dataset2)  


#Classifier prediction
predictedLabel=classifier.predict(x_test_tf_idf)
print(predictedLabel)

precision, recall, fscore, support = score(y_test_label, predictedLabel)
#y_test assumed to be the true label.
print('Accuracy score: {}'.format(accuracy_score(y_test_label, predictedLabel)))
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))


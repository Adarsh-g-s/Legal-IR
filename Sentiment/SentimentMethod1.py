import numpy as np
import pandas as pd
import nltk
import string
from collections import Counter
import re
from textblob import TextBlob
from bs4 import BeautifulSoup
import os
import pathlib
from sklearn import svm
from Sentiment.happiness_score import happiness_score as hs
from Sentiment.featuresExtracter import feat_analyser as fa
from sklearn.externals import joblib
from scipy.spatial import distance_matrix




from nltk.sentiment.vader import SentimentIntensityAnalyzer

class sentiment_method1:

    #global data_dir
    #data_dir = 'D:\Projects\Legal_IR\Doc_Dump\Temp'


    def sent_dist_matrix_calc(data_dir):
        #load classifier
        clf = joblib.load('../Sentiment/svmClasifier.pkl')

        feature_cols_train = ['negative_word_count', 'positive_word_count', 'vander_score']#, 'happ_score'  excluded

        df_s =pd.DataFrame(columns=['Sentiment'])

        # traverse through the data object

        #code for reading from file commented
        # for path, subdirs, files in os.walk(data_dir):
        #     for name in files:
        # code for reading from file commented

        for abs_path in data_dir:
                df = pd.DataFrame(columns=['negative_word_count', 'positive_word_count', 'vander_score', 'happ_score'])


                # print( os.path.join(path, name))
                # if row.Filename==name:
                #absolutePathToFile = pathlib.PurePath(path, name)
                #print(absolutePathToFile)
                #url = open(absolutePathToFile, encoding="utf8")
                absolutePathToFile = pathlib.PurePath(abs_path)
                url = open(absolutePathToFile, encoding="utf8")
                name = os.path.basename(abs_path)
                soup = BeautifulSoup(url, "lxml")
                data_for_chunk = soup.get_text().replace('\n', '\n\n')
                paragraphs = data_for_chunk.split("\n\n")
                count = 0

                for value in paragraphs:
                    count = count + 1
                #print(count)

                # logic to divide into paragraphs. it handles when number of paragraphs are odd numbered also
                a = count / 3
                b = (count - a) / 2
                c = (count - a - b)

                # intiating chunks
                chunk1 = ""
                chunk2 = ""
                chunk3 = ""

                # logic to add cumulative counts
                x = a
                y = x + b
                z = y + c

                countcumulative = 0

                # logic to add paragraphs to different chunks
                for value in paragraphs:
                    if countcumulative < x:
                        chunk1 = chunk1 + value
                    elif countcumulative < y:
                        chunk2 = chunk2 + value
                    elif countcumulative < z:
                        chunk3 = chunk3 + value
                    countcumulative = countcumulative + 1

                pred_list = []
                #print(chunk1)
                sent_feat1 = fa.defsentfeatextractor(chunk1)
                df.loc[name] = sent_feat1

                pred1 = clf.predict(df[feature_cols_train])
                #print(pred1)
                pred_list.append(pred1[0])

                # print(chunk2)
                sent_feat2 = fa.defsentfeatextractor(chunk2)
                df.loc[name] = sent_feat2

                pred2 = clf.predict(df[feature_cols_train])
                #print(pred2)
                pred_list.append(pred2[0])
                # print(chunk3)
                sent_feat3 = fa.defsentfeatextractor(chunk3)
                df.loc[name] = sent_feat3

                pred3 = clf.predict(df[feature_cols_train])
                #print(pred3)
                pred_list.append(pred3[0])

                # print("pred_list:")
                # print(pred_list)

                #print("count of 0:")
                #print(pred_list.count(0))

                if pred_list.count(0)>=2:
                    pred = 0
                elif pred_list.count(1)>=2:
                    pred = 1
                elif pred_list.count(2)>=2:
                    pred =2
                else:
                    pred = 0
                df= None
                df_s.loc[name] = pred
                #print(name.__str__()+" : "+pred.__str__())
        #we get the docs with all sentiments
        #now lets calculate distance
        #print(df_s)
        df2 = pd.DataFrame(distance_matrix(df_s.values, df_s.values), index=df_s.index, columns=df_s.index)
        df2=df2.applymap(sentiment_method1.zeroOrOne)
        print(df2)
        print(df2.as_matrix())
        return df2


    def zeroOrOne(x):
        if x==0.0:
            return 0
        else:
            return 1
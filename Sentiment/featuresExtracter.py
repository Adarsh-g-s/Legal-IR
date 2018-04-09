import numpy as np
import pandas as pd
import nltk
nltk.downloader.download('vader_lexicon')
nltk.download('punkt')
import string
import os
from collections import Counter
import re
from textblob import TextBlob
from happiness_score import happiness_score as hs


from nltk.sentiment.vader import SentimentIntensityAnalyzer

class feat_analyser:
    global lexicon_directory
    lexicon_directory = '../Data/opinion-lexicon-English'

    global data_dir
    data_dir = '../Data'
    global html_text
    html_text = "He is wrong guy and good hero!.?"


    def defsentfeatextractor(html_text):
        sid = SentimentIntensityAnalyzer()

        data_review = html_text


        #print(data_review)

        # Positive Lexicons\n
        positive_words = np.loadtxt(lexicon_directory + '/positive-words.txt', comments=';', dtype='bytes')
        positive_words = [x.decode('us-ascii') for x in positive_words]
        positive_words = set(positive_words)
        # print(positive_words)

        # stop words\n
        stop_words = np.loadtxt(data_dir + '/stopwords.txt', comments=';', dtype='bytes')
        stop_words = [x.decode('us-ascii') for x in stop_words]
        stop_words = set(stop_words)
        # print(stop_words)

        # Negative Lexicons
        with open(lexicon_directory + '/negative-words.txt', encoding='iso-8859-1') as f:
            negative_words = np.loadtxt(f, comments=';', dtype='bytes')
            negative_words = [x.decode('iso-8859-1') for x in negative_words.tolist()]
            negative_words = set(negative_words)
        # print(negative_words)

        # Get only the required data
        # data_review = data_review[['post_id','agrees', 'before', 'sentence', 'after', 'third', 'treatments','factual (yes/no)','sentiment (pos/neg/neu)']]
        # print(data_review.head())
        pd.set_option('display.width', 1000)

        # merge coloumns before , sentence,after and third

        def remove_punctuation(s):
            s = ''.join([i for i in s if i not in frozenset(string.punctuation)])
            return s

        data_review = remove_punctuation(data_review)
        #data_review = str(data_review)
        data_review = data_review.lower()
        #print(data_review)

        #pd.options.display.max_colwidth = 100

        # nltk.word_tokenize(df.get_value(0,'text'))
        data_review_tokens = nltk.word_tokenize(data_review)
        #print(data_review_tokens)
        data_review_tokens = set(data_review_tokens).difference(stop_words.intersection(data_review_tokens))
        #print(data_review_tokens)


        # Count the number of tokens\
        data_review_word_count = data_review_tokens.__len__()
        #print(data_review_word_count)


        feat_list = []
        pos_word_count = positive_words.intersection(data_review_tokens).__len__()
        neg_word_count = negative_words.intersection(data_review_tokens).__len__()
        total_count = pos_word_count+neg_word_count

        if total_count!=0:
            pos_word_count_norm = pos_word_count/(total_count)
            neg_word_count_norm = neg_word_count/(total_count)
        else:
            pos_word_count_norm = neg_word_count_norm = 0


        # positive words
        feat_list.append(pos_word_count_norm)

        # negative words
        feat_list.append(neg_word_count_norm)

        #Vander score
        vander_sent = sid.polarity_scores(data_review)
        feat_list.append( vander_sent['compound'])


        #Happiness Score
        feat_list.append(hs.score(data_review))

        #print(feat_list)
        return feat_list

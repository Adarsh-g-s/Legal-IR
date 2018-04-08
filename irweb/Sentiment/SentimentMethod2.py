import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import pathlib
from scipy.spatial import distance_matrix
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class sentiment_method2:

    def sent_dist_matrix_calc(data_dir):
        sent_analyzer = SentimentIntensityAnalyzer()
        df_s =pd.DataFrame(columns=['SentimentScore'])

        # traverse through the data object
        for abs_path in data_dir:

                absolutePathToFile = pathlib.PurePath(abs_path)
                url = open(absolutePathToFile, encoding="utf8")
                name = os.path.basename(abs_path)
                soup = BeautifulSoup(url, "lxml")
                entire_text = soup.get_text()

                # Vader score
                vader_sent = sent_analyzer.polarity_scores(entire_text)
                pol_score = (vader_sent['compound'])


                df_s.loc[name] = pol_score

        #we get the docs with all sentiments
        #now lets calculate distance
        #print(df_s)
        df2 = pd.DataFrame(distance_matrix(df_s.values, df_s.values), index=df_s.index, columns=df_s.index)
        #print(df2.as_matrix())
        sentDistMatrx = df2.as_matrix()
        return sentDistMatrx



from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import os
import pathlib
import pandas as pd
from Sentiment.featuresExtracter import feat_analyser as fa
from Sentiment.happiness_score import happiness_score as hs

global lexicon_directory
lexicon_directory = '../data/opinion-lexicon-English'
global data_dir
#where all the data files are located
data_dir = 'D:/Projects/Legal_IR/Doc_Dump/Results_For_Queries'

#annotation = pd.read_csv('..\DATA\Annotations.csv',delimiter=',',skipinitialspace=True)

df = pd.DataFrame(columns=['negative_word_count', 'positive_word_count', 'vander_score','happ_score'])
#annotation = annotation.reset_index()
#for row in annotation.itertuples(index=False):
root = data_dir
#print(row)
for path, subdirs, files in os.walk(root):
    for name in files:
        #print( os.path.join(path, name))
        #if row.Filename==name:
            absolutePathToFile = pathlib.PurePath(path, name)
            print(absolutePathToFile)
            url = open(absolutePathToFile,encoding="utf8")
            soup = BeautifulSoup(url, "lxml")
            entire_text = soup.get_text()

            df_temp = fa.defsentfeatextractor(entire_text)
           # print(df_temp)

            #df_temp.append(row.Sentiment)
            df.loc[name] = df_temp

            #df2.set_index(df2.columns[0:0], inplace=True)



#print(df)
df.to_csv('..\\Data\\res.csv',index_label='doc_id')


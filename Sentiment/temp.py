from Sentiment.SentimentMethod1 import sentiment_method1 as sm1



data_dir = 'D:\Projects\Legal_IR\Doc_Dump\Temp'


pred = sm1.sent_dist_matrix_calc(data_dir)

print(pred)
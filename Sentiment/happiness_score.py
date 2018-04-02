from bs4 import BeautifulSoup
import pandas as pd

class happiness_score:

    def score(entire_text):
        normalized_Frequency=0.0
        total_happiness_score=0.0
        #code to get list of word and its happiness score from document
        d = {}
        with open("../Sentiment/data1.txt") as i:
            for line in i:
               (key, val) = line.split()
               d[key] = val


        #code to get each word count present in document
        def count_all_words(entire_text):
            count_words = dict()
            words = entire_text.split()

            for word in words:
                if word in count_words:
                    count_words[word] += 1
                else:
                    count_words[word] = 1

            return count_words


        count_of_words=count_all_words(entire_text) # store all the word counts in a

        #code for getting normalized frequency
        for key in count_of_words :
            normalized_Frequency=normalized_Frequency+(count_of_words[key]) #all frequency of each word in document to get normalised frequency
           # print(a[key])
        #print(normalizedFrequency)



        for key in count_of_words :
            if key in d :
             #   countall= countall +1
                x=d[key] #happiness avg score of word
                y=count_of_words[key] #frequency of word
                total_happiness_score=total_happiness_score+float(x)*(float(y)/normalized_Frequency)

        #print(total_happiness_score)
        return total_happiness_score

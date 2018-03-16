from sklearn.metrics.pairwise import cosine_distances
from sklearn.feature_extraction.text import TfidfVectorizer

class SemanticDistCalculator(object):
    """description of class"""
    def learnVocabulary(self, filePaths):
        self.filePaths = filePaths
        self.tfidf_vectorizer = TfidfVectorizer(input='filename', stop_words='english',
                                                max_features=500, max_df=0.8, min_df=0.2)
        self.tfidf_vectorizer.fit(self.filePaths)
        # print(self.tfidf_vectorizer.vocabulary_)

    def showDocDistMatrix(self):
        tfidf_matrix = self.tfidf_vectorizer.transform(self.filePaths)
        # print(tfidf_matrix)
        self.tfidf_cosine_distance_array = cosine_distances(tfidf_matrix)
        print(self.tfidf_cosine_distance_array)

    # def getDistances(self, filepaths):
        # distList = []
        # tempDocList = []
        # tempDocList.append(filepaths[0])
        # for docIndex in range(1, len(filepaths)):
            # tempDocList.append(filepaths[docIndex])
            # tfidf_matrix = self.tfidf_vectorizer.transform(tempDocList)
            # cosine_dist_array = cosine_distances(tfidf_matrix)
            # # print(cosine_dist_array)
            # # TODO:
            # distList.append(cosine_dist_array[0][1])
            # tempDocList.pop()

        # return distList

    def calcDistMatrix(self):
        tfidf_matrix = self.tfidf_vectorizer.transform(self.filePaths)
        self.cosine_dist_array = cosine_distances(tfidf_matrix)
        
    def getDistances(self, fileIndex):
        distArray = self.cosine_dist_array[fileIndex]
        return distArray

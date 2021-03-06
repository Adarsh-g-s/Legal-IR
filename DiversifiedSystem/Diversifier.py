from SemanticDistCalculator import SemanticDistCalculator
from SentimentMethod1 import sentiment_method1 as sm1
from SentimentMethod2 import sentiment_method2 as sm2

class Diversifier(object):
    """This class is responsible for deversifying the set of documents."""
    def __init__(self, originalFileList, originalHitList):
        self.originalFileList = originalFileList
        self.originalHitList = originalHitList
        self.currentDoc = None
        self.prevDoc = None
        self.distListToCurrentDoc = None
        self.distListToPrevDoc = None
        self.docDistMtrx = None
        self.diverseDocSet = set()
        self.sumOfCurrToNext = 0
        self.sumOfPrevToNext = 0
        # alpha & beta parameters found using hyper parameter tuning is to be used here.    
        self.alpha = 0.9683331071230177 # The proportion of distance between current and next dec
        self.beta  = 0.5707760724661901 # The proportion of distance between previous and next dec


    def findMostDiverse(self, docCount):
        """ This function returns the most diverse set of documents starting from the most relevant document among the resultset. """
        
        # We prepare a distance matrix where,
        # each element = [semamtic distance(current to next) + sentiment distance(current to next)] * relevance(next),
        # such that current is referred as row and next is referred as column.

        semDistCalc = SemanticDistCalculator()
        semDistCalc.learnVocabulary(self.originalFileList)
        self.docDistMtrx = semDistCalc.calcDistMatrix()

        #TODO: Address the sentiment component too for the distance matrix
        #Sentiment Method 1
        self.sentDistMatrix = sm1.sent_dist_matrix_calc(self.originalFileList)
        # Sentiment Method 2
        #self.sentDistMatrix = sm2.sent_dist_matrix_calc(self.originalFileList)
        # to-do

        # print("Original file_list length:")
        # print(len(self.originalFileList))
        # print("Semantic matrix:")
        # print(self.docDistMtrx)
        #
        # print("Sentiment matrix:")
        # print(self.sentDistMatrix)
        self.docDistMtrx += self.sentDistMatrix

        # Multiply the relevance score of the 'potential next' document with its distances from the rest of the documents.
        for docIndex in range(0, len(self.originalFileList)):
            # Multiply relevance score to each distance in each column.
            self.docDistMtrx[:,docIndex] *= self.originalHitList[docIndex].score

        # At this point, the distance matrix is ready and we iteratively find 
        # the most diverse doc starting from the most relevant doc.
        docSetList = []
        diverseDocScoreList = []
        self.currentDoc = self.originalFileList[0]
        self.currentDocIndex = 0 # Starts with the most relevant doc
        self.diverseDocSet.add(self.currentDocIndex)
        diverseDocScoreList.append(self.originalHitList[self.currentDocIndex].score)
        docSetList.append(self.currentDoc) # Add the most relevant doc at first

        print( docCount, "Most diverse results:\n")
        print(self.currentDoc,"\n")
        
        docCounter = 1
        while docCounter != docCount:
            farthestdoc = self.__getFarthestDoc()
            if farthestdoc == None:
                break
            print(farthestdoc,"\n")
            docSetList.append(farthestdoc)
            diverseDocScoreList.append(self.originalHitList[self.currentDocIndex].score)
            docCounter += 1
            # Update new prev & current docs
            self.prevDoc = self.currentDoc
            
            # ---- For Parameter optimization -----
            self.sumOfCurrToNext += self.distListToCurrentDoc[self.currentDocIndex]
            if 2 < len(docSetList):
                self.sumOfPrevToNext += self.distListToPrevDoc[self.currentDocIndex]

            self.currentDoc = farthestdoc
            self.distListToPrevDoc = self.distListToCurrentDoc

        return docSetList, diverseDocScoreList, self.sumOfCurrToNext, self.sumOfPrevToNext


    def __getFarthestDoc(self):
        """ This function returns the farthest doc from the current doc with moderate distance from the prev doc. """
        self.distListToCurrentDoc = self.docDistMtrx[self.currentDocIndex]
        
        distArray = None
        if len(self.diverseDocSet) == 1:
            # Expected only for finding the second doc as self.distListToPrevDoc would be empty.
            distArray = self.distListToCurrentDoc
        else:
            # Calculate element wise sum of both arrays.
            distArray = (self.alpha * self.distListToCurrentDoc) + (self.beta * self.distListToPrevDoc)
        
        highIndex = distArray.argmax()
        if highIndex in self.diverseDocSet:
            highIndex = self.__findModerateFarthestDocIndex(distArray.tolist())
            if highIndex == -1:
                return None
        self.currentDocIndex = highIndex
        self.diverseDocSet.add(self.currentDocIndex)
        return self.originalFileList[self.currentDocIndex]


    def __findModerateFarthestDocIndex(self, distList):
        tempOrigList = distList
        tempList = list(tempOrigList)
        tempList.sort()
        tempList.pop() # Farthest doc is already collected to the diverse doc list.
        secondBestDist = tempList.pop()
        foundIndex = tempOrigList.index(secondBestDist)
        while foundIndex in self.diverseDocSet:
            if 0 == len(tempList):
                return -1

            secondBestDist = tempList.pop()
            foundIndex = tempOrigList.index(secondBestDist)

        return foundIndex
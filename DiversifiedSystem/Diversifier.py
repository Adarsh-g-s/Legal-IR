from SemanticDistCalculator import SemanticDistCalculator

class Diversifier(object):
    """This class is responsible for deversifying the set of documents."""
    def __init__(self, originalResult):
        self.originalResult = originalResult
        self.currentDoc = None
        self.prevDoc = None
        self.distListToCurrentDoc = None
        self.distListToPrevDoc = None
        self.semDistCalc = None
        self.diverseDocSet = set()


    def findMostDiverse(self, docCount):
        """ This function returns the most diverse set of documents starting from the most relevant document among the resultset. """

        docSetList = []
        self.currentDoc = self.originalResult[0]
        self.currentDocIndex = 0 # Starts with the most relevant doc
        docSetList.append(self.currentDoc) # Add the most relevant doc at first
        docCounter = 1

        self.semDistCalc = SemanticDistCalculator()
        self.semDistCalc.learnVocabulary(self.originalResult)
        self.semDistCalc.calcDistMatrix()

        print( docCount, "Most diverse results:\n")
        print(self.currentDoc,"\n")
        
        while docCounter != docCount:
            farthestdoc = self.__getFarthestDoc()
            if farthestdoc == None:
                break
            print(farthestdoc,"\n")
            docSetList.append(farthestdoc)
            docCounter += 1
            # Update new prev & current docs
            self.prevDoc = self.currentDoc
            self.currentDoc = farthestdoc

        return docSetList


    def __getFarthestDoc(self):
        """ This function returns the farthest doc from the current doc with moderate distance from the prev doc. """
        #TODO: 
        self.distListToCurrentDoc = self.semDistCalc.getDistances(self.currentDocIndex)
        # highDist = max(self.distListToCurrentDoc)
        highIndex = self.distListToCurrentDoc.argmax()
        if highIndex in self.diverseDocSet:
            highIndex = self.__findModerateFarthestDocIndex()
            if highIndex == -1:
                return None
        # highIndex = self.distListToCurrentDoc.index(highDist)
        self.currentDocIndex = highIndex
        self.diverseDocSet.add(self.currentDocIndex)
        return self.originalResult[self.currentDocIndex]

    def __findModerateFarthestDocIndex(self):
        tempOrigList = self.distListToCurrentDoc.tolist()
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
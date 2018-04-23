from __future__ import division
from bs4 import BeautifulSoup
import os
from glob2 import glob, iglob
from lxml import html


from whoosh.fields import *
from whoosh.analysis import *
from whoosh import index
from whoosh.writing import IndexWriter
from random import choice
from whoosh.reading import IndexReader
from whoosh.index import open_dir
from whoosh import qparser
from whoosh import scoring
from whoosh.scoring import Weighting
from whoosh.highlight import highlight, WholeFragmenter
from Diversifier import Diversifier
from hyperopt import hp
from hyperopt import fmin, Trials, tpe
import numpy
import hyperopt
from random import seed
import matplotlib.pyplot as plt

class Indexer:
    '''
    Indexes the documents
    '''

    def __init__(self):
        '''
        Constructor
        '''
#         self.path = path
#         self.contents = contents

    def getSchema(self):
        schema = Schema(
            path  = ID(stored=True),
            title = TEXT(stored=True),
            contents = TEXT(analyzer=analysis.StemmingAnalyzer(),stored=True, phrase = True)
            )
        return schema

    def indexing(self,filePath,fileContents, fileTitle):
        try:
            indexWriter.add_document(path = filePath, 
                                     title = fileTitle,
                                     contents = fileContents)   
            
        except:
            print("Inside the except clause")

class Search:
    'Search class'
    
    def getTheQueryParser(self,indexer):
        'Return the query parser with corresponding schema'
        return qparser.MultifieldParser(["title","contents"], schema=indexer.getSchema())
    
    def getResults(self,found,rank,highestScore):
        print()
        print(rank)
        print("Relevance Score: ",found.score)
        #Store the first score and use it for normalization
        if(rank == 1):
            highestScore = found.score
        
        normalizedScore = found.score/highestScore
        print("Normalized Relevance Score: ",normalizedScore)
        #Title could be longer than a line, split and display
        title = found['title']
        title = title.split(';',maxsplit=2)
#         print("Title: ",found['title'])
        print("Title: ", title[0]+ "...")
        print(found['path'])
        summary = found.highlights('contents',top=10)
        summary = summary.encode('utf-8')
        print("Summary: ",summary)
        return highestScore
        
    def showResults(self,query,pageNumber,rank,highestScore):
        pageNumber+=1
        'Adarsh changes'
        results = searcher.search_page(query, pageNumber)
        #results = searcher.search(query)
        #results.fragmenter = highlight.WholeFragmenter()
        print("Showing ", results.scored_length()," out of ", len(results), "results")
        #         print(results)
        for found in results:
            rank+=1
            highestScore = search.getResults(found,rank,highestScore)
        return pageNumber,rank, highestScore
    
    def wantNextPageResults(self):
        print("\n To see next page results \n press Y or y else press N or n")
        return input(" Enter your choice: ")
    
class Setup:
    '''
    Take document path as the user input and pass it to Indexer for Indexing
    '''

    def __init__(self, documentPath, filePath, htmlFileContents,fileTitle, choice, indexDirectory, indexName,sumOfCurrToNext,sumOfPrevToNext,space,docList,hitList):
        '''
        Constructor
        '''
        self.documentPath = documentPath
        self.filePath = filePath
        self.htmlFileContents = htmlFileContents
        self.fileTitle = fileTitle
        self.choice = choice
        self.indexDirectory = indexDirectory
        self.indexName = indexName
        self.sumOfPrevToNext = sumOfPrevToNext
        self.sumOfCurrToNext = sumOfCurrToNext
        self.space = space
        self.hitList = hitList
        self.docList = docList
    
    def userInput(self):
        print("\n Enter \n 1. Index \n 2. Search \n 3. Exit")
        self.choice = int(input("Enter your choice: "))
#         self.documentPath = input("Enter the document path")
        return
    
    def getTitle(self, filePath):
        #Get the title of the file
        fileContents = open(filePath, "r", encoding="utf8")
        htmlTitle = BeautifulSoup(fileContents,"html.parser")
        if htmlTitle.find('h1'):
#             try:
                htmlTitle = htmlTitle.find('h1').get_text()
#             except:
#                 htmlTitle = "No Title found!"
        elif htmlTitle.find('p', class_ = "parties"):
#             try: 
                  htmlTitle=htmlTitle.find('p', class_ = "parties").get_text()
#                   print(htmlTitle)
#             except:
#                 htmlTitle = "No Title found!"
        return htmlTitle
    
    def getContentsOfHtmlFiles(self, filePath):
        # open the file and access the contents
        fileContents = open(filePath, "r", encoding="utf8")
        htmlContent = BeautifulSoup(fileContents, "html.parser")
        # extract the title of the html file? How There is no title tag.
        try:
            htmlContent = htmlContent.find('body').get_text()
        except:
            htmlContent = "Null"
        return htmlContent
    
    def getIndexDirectory(self):
        'Location of the index folder'
        currentDirectory = os.getcwd()
#creating an index directory
        setup.indexDirectory= currentDirectory + '\..\index' #os.path.join(currentDirectory,"index")
        if not os.path.exists(setup.indexDirectory):
            os.makedirs(setup.indexDirectory)
#         print(setup.indexDirectory)
        return setup.indexDirectory
    
    def getPathTitleAndContents(self,directory,indexer):
        #For all files in a directory, get the contents
        for root, dirs,files in os.walk(directory):
            for file in files:
                filename = os.fsdecode(file)
                if filename.endswith(".html"): 
                    setup.htmlFileContents = None
                    # parse the contents of this file
                    setup.filePath = os.path.join(root, filename)
                    print(setup.filePath)
                    #get Title of the file
                    setup.fileTitle = setup.getTitle(setup.filePath)
                    setup.htmlFileContents = setup.getContentsOfHtmlFiles(setup.filePath)
                    # Send parsed output for tokenization, stopword removal and stemming.
                    indexer.indexing(setup.filePath, setup.htmlFileContents,setup.fileTitle)
                else:
                    print("File is in a format other than html")
    '''
        Define the objective function to find the maximums
    '''
    
    def objective(self,space):
        a = space['a']
        b = space['b']
        diversifier = Diversifier(setup.docList, setup.hitList)
        k = 20
        if( k > len(setup.docList) ): k = len(setup.docList)
        diversifier.alpha = a
        diversifier.beta = b
        diverseResult, scoreList, setup.sumOfCurrToNext,setup.sumOfPrevToNext = diversifier.findMostDiverse(k)
        return -(a * setup.sumOfCurrToNext + b * setup.sumOfPrevToNext)
                    
setup = Setup(documentPath = None, filePath = None, htmlFileContents= None, fileTitle = None, choice = None, indexDirectory=None, indexName = None,sumOfCurrToNext = None,sumOfPrevToNext = None,space = None,docList = None, hitList = None )

while (True):
    indexDirectory = setup.getIndexDirectory()
    setup.userInput()
    indexer = Indexer()
    #Based on the choice, go for corresponding task.
    if setup.choice==1:
        'Do Indexing'
    # parse the contents in this document path.
        setup.documentPath = input("Enter document path: ")
    # from the path, go to a file and then parse it.
        directory = os.fspath(setup.documentPath)
    #The schema specifies the fields of documents in an index.
        schema = indexer.getSchema()
       
        #Check if an index folder exists, if it does not then create else use existing one.
        setup.indexName = glob(indexDirectory+"/"+'**')
        if not os.path.exists(indexDirectory):
            indexFolder = index.create_in(indexDirectory, schema)
        else:
            indexFolder = index.open_dir(indexDirectory)
    #create the index writer
        indexWriter = indexFolder.writer()
        
        #setup.getPathTitleAndContents(directory,indexer)
        setup.getPathTitleAndContents(directory,indexer)
        
        indexWriter.commit()
        
        print("Done!")
        
    elif setup.choice==2:
        'Searching'
    #open the index directory and read the contents
#         print(setup.indexDirectory)
        indexReader = open_dir(setup.indexDirectory)
        search = Search()
        queryParser = search.getTheQueryParser(indexer)
        query = input("Enter the query: ")
        query = queryParser.parse(query)
        print(query)
        
#         rankingModel = scoring.BM25F(B=0.75,K1=1.5)
        with indexReader.searcher(weighting=scoring.BM25F(B=0.75,K1=1.2)) as searcher:
#             results=searcher.search(query, terms = True)
            pageNumber = 0
            rank = 0
            highestScore = 1

            # Get all the search result with limit = None
            immediateResult = searcher.search(query, limit = None)

            # Prepare the list of document paths
            setup.docList = []
            setup.hitList = []
            counter = 0
            for hit in immediateResult:
                # The 'k' most diverse docs shall be searched in the 100 most relevant docs.
                # TODO: Find better cut off.
                if counter < 100:
                    setup.docList.append(hit['path'])
                    counter = counter + 1
                setup.hitList.append(hit)

            # Pass the document path to the Diversifier
#             diversifier = Diversifier(docList, scoreList)
#             k = 20
#             diverseResult,setup.sumOfCurrToNext,setup.sumOfPrevToNext = diversifier.findMostDiverse(k)
            '''
            # Remove the top 'k' from the entire list & add them at the beginning for the final list.
            for fileName in reversed(diverseResult):
                if fileName in docList:
                    docList.remove(fileName)

                docList.insert(0, fileName)


            #totalNumberOfPages = int(len(docList)/10)
            #pageNumber, rank, highestScore = search.showResults(query,pageNumber,rank,highestScore)
            print("\nFinal Result:")
            for fileName in docList:
                rank = rank + 1
                print("\nRank#", rank, ": ", fileName)
                if 0 == rank % 10:
                    setup.choice = search.wantNextPageResults()
                    if setup.choice == 'Y' or setup.choice == 'y':
                        continue
                    else:
                        break
            '''
    
            # Parameter search space
 
            '''
            Use random integer distribution for finding alpha(a) and beta(b)
            
            '''
            setup.space={
                'a': hp.uniform ('a',0.6,1),
                'b': hp.uniform ('b',0,0.6)
                }
     
            '''
            Run the hyperparameter optimization
            '''
 
            # The Trials object will store details of each iteration
            seed = 150
            trials = Trials()
            
            best = fmin(fn=setup.objective,
                        space=setup.space,
                        algo=hyperopt.rand.suggest,
                        max_evals=150,trials=trials,rstate= numpy.random.RandomState(seed))
            
 
            print("Maximum: ", best)
#             print('trials:')
#             for trial in trials.trials[:2]:
#                 print(trial)
 
            '''
            Plot of the function for a
            '''
            f, ax = plt.subplots(1)
            xs = [t['misc']['vals']['a'] for t in trials.trials]
            ys = [t['result']['loss'] for t in trials.trials]
            ax.scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75)
            ax.set_title('$val$ $vs$ $a$ ', fontsize=18)
            ax.set_xlabel('$a$', fontsize=16)
            ax.set_ylabel('$val$', fontsize=16)
            plt.show()
    
            '''
            Plot of the function for b
            '''
            f, ax = plt.subplots(1)
            xs = [t['misc']['vals']['b'] for t in trials.trials]
            ys = [t['result']['loss'] for t in trials.trials]
            ax.scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75)
            ax.set_title('$val$ $vs$ $b$ ', fontsize=18)
            ax.set_xlabel('$b$', fontsize=16)
            ax.set_ylabel('$val$', fontsize=16)
            plt.show()
            break          
    else:
        exit()
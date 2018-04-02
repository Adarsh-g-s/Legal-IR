'''
Created on Feb 27, 2018

@author: adarsh
'''
from __future__ import division

import pathlib
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

class SearchTwo:
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
        summary = found.highlights('contents')
        summary = summary.encode('utf-8')
        print("Summary: ",summary)
        return highestScore

#     def showResults(self,query,pageNumber,rank,highestScore,pageLength):
#         # search = SearchTwo()
#         # root_path = os.path.abspath(os.path.dirname(__file__))
#         # indexDirectory = os.path.join(root_path, "index")
#         # indexReader = open_dir(indexDirectory)
#         # searcher = indexReader.searcher(weighting=scoring.BM25F(B=0.75, K1=1.5))
#         # results = searcher.search_page(query, pageNumber, pagelen=pageLength)
#         # pageNumber+=1
#         'Adarsh changes'
#         results = searcher.search_page(query, pageNumber)
#         #results = searcher.search(query)
#         #results.fragmenter = highlight.WholeFragmenter()
#         print("Showing ", results.scored_length()," out of ", len(results), "results")
#         #         print(results)
#         for found in results:
#             rank+=1
#             highestScore = search.getResults(found,rank,highestScore)
#         return pageNumber,rank, highestScore
#
#     def wantNextPageResults(self):
#         print("\n To see next page results \n press Y or y else press N or n")
#         return input(" Enter your choice: ")
#
# class Setup:
#     '''
#     Take document path as the user input and pass it to Indexer for Indexing
#     '''

#     def __init__(self, documentPath, filePath, htmlFileContents,fileTitle, choice, indexDirectory, indexName):
#         '''
#         Constructor
#         '''
#         self.documentPath = documentPath
#         self.filePath = filePath
#         self.htmlFileContents = htmlFileContents
#         self.fileTitle = fileTitle
#         self.choice = choice
#         self.indexDirectory = indexDirectory
#         self.indexName = indexName
#
#     def userInput(self):
#         print("\n Enter \n 1. Index \n 2. Search \n 3. Exit")
#         self.choice = int(input("Enter your choice: "))
# #         self.documentPath = input("Enter the document path")
#         return
#
#     def getTitle(self, filePath):
#         #Get the title of the file
#         fileContents = open(filePath, "r", encoding="utf8")
#         htmlTitle = BeautifulSoup(fileContents,"html.parser")
#         if htmlTitle.find('h1'):
# #             try:
#                 htmlTitle = htmlTitle.find('h1').get_text()
# #             except:
# #                 htmlTitle = "No Title found!"
#         elif htmlTitle.find('p', class_ = "parties"):
# #             try:
#                   htmlTitle=htmlTitle.find('p', class_ = "parties").get_text()
# #                   print(htmlTitle)
# #             except:
# #                 htmlTitle = "No Title found!"
#         return htmlTitle

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

#     def getIndexDirectory(self):
#         'Location of the index folder'
#         currentDirectory = os.getcwd()
# #creating an index directory
#         setup.indexDirectory=os.path.join(currentDirectory,"index")
#         if not os.path.exists(setup.indexDirectory):
#             os.makedirs(setup.indexDirectory)
# #         print(setup.indexDirectory)
#         return setup.indexDirectory

    # def getPathTitleAndContents(self,directory,indexer):
    #     #For all files in a directory, get the contents
    #     for root, dirs,files in os.walk(directory):
    #         for file in files:
    #             filename = os.fsdecode(file)
    #             if filename.endswith(".html"):
    #                 setup.htmlFileContents = None
    #                 # parse the contents of this file
    #                 setup.filePath = os.path.join(root, filename)
    #                 print(setup.filePath)
    #                 #get Title of the file
    #                 setup.fileTitle = setup.getTitle(setup.filePath)
    #                 setup.htmlFileContents = setup.getContentsOfHtmlFiles(setup.filePath)
    #                 # Send parsed output for tokenization, stopword removal and stemming.
    #                 indexer.indexing(setup.filePath, setup.htmlFileContents,setup.fileTitle)
    #             else:
    #                 print("File is in a format other than html")

# setup = Setup(documentPath = None, filePath = None, htmlFileContents= None, fileTitle = None, choice = None, indexDirectory=None, indexName = None)
#
# while (True):
#     indexDirectory = setup.getIndexDirectory()
#     setup.userInput()
#     indexer = Indexer()
    # #Based on the choice, go for corresponding task.
    # if setup.choice==1:
    #     'Do Indexing'
    # # parse the contents in this document path.
    #     setup.documentPath = input("Enter document path: ")
    # # from the path, go to a file and then parse it.
    #     directory = os.fspath(setup.documentPath)
    # #The schema specifies the fields of documents in an index.
    #     schema = indexer.getSchema()
    #
    #     #Check if an index folder exists, if it does not then create else use existing one.
    #     setup.indexName = glob(indexDirectory+"/"+'**')
    #     if not os.path.exists(indexDirectory):
    #         indexFolder = index.create_in(indexDirectory, schema)
    #     else:
    #         indexFolder = index.open_dir(indexDirectory)
    # #create the index writer
    #     indexWriter = indexFolder.writer()
    #
    #     #setup.getPathTitleAndContents(directory,indexer)
    #     setup.getPathTitleAndContents(directory,indexer)
    #
    #     indexWriter.commit()
    #
    #     print("Done!")
    #
    # elif setup.choice==2:
    #     'Searching'


    @staticmethod
    def passingQuery(queryInput, pageNumber, pageLength):


        search = SearchTwo()
        root_path = os.path.abspath(os.path.dirname(__file__))
        indexDirectory = os.path.join(root_path, "index")
        indexReader = open_dir(indexDirectory)
        indexer = Indexer()
        queryParser = search.getTheQueryParser(indexer)
        query = queryParser.parse(queryInput)

        with indexReader.searcher(weighting=scoring.BM25F(B=0.75,K1=1.2)) as searcher:

            # Get all the search result with limit = None
            immediateResult = searcher.search(query, limit = None)
            # print(immediateResult)


            # Prepare the list of document paths
            docList = []
            scoreList = []
            resHitList = []
            # counter = 0
            for hit in immediateResult:
                # counter = counter+1
                docList.append(hit['path'])
                scoreList.append(hit.score)
                resHitList.append(hit)
                # if counter==10:
                # break

            # Pass the document path to the Diversifier
            diversifier = Diversifier(docList, resHitList)
            k = 20
            diverseFileList, diverseDocScoreList = diversifier.findMostDiverse(k)

            # Remove the top 'k' from the entire list & add them at the beginning for the final list.
            for nDocIdx in range(k - 1, 0, -1):
                if diverseFileList[nDocIdx] in docList:
                    docList.remove(diverseFileList[nDocIdx])
                docList.insert(0, diverseFileList[nDocIdx])
                for whooshHit in resHitList:
                    if whooshHit.score == diverseDocScoreList[nDocIdx]:
                        resHitList.remove(whooshHit)
                        resHitList.insert(0, whooshHit)
                        break

            outputs = []

            for found in resHitList:
                summary = found.highlights('contents')
                title = found['title']
                title = title[:100]
                title = title.split(';', maxsplit=2) #should it be too longer than a line
                result = {
                    'relevantScore': found.score,
                    'title': title, #just pick the first element
                    'path': pathlib.Path(found['path']).as_uri(),
                    # 'path': found['path'].split("Legalfiles")[1],

                    'summary': summary
                }

                outputs.append(result)

            return outputs

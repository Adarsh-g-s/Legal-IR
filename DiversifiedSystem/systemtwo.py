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
        indexDirectory = os.getcwd() + '\..\index'
        if not os.path.exists(indexDirectory):
            os.makedirs(indexDirectory)

        return indexDirectory


    @staticmethod
    def passingQuery(queryInput, pageNumber, pageLength):


        search = SearchTwo()
        indexDirectory = search.getIndexDirectory()
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
            counter = 0
            for hit in immediateResult:
                # The 'k' most diverse docs shall be searched in the 100 most relevant docs.
                # TODO: Find better cut off.
                if counter < 100:
                    docList.append(hit['path'])
                    counter = counter + 1
                resHitList.append(hit)
                # if counter==10:
                # break

            # Pass the document path to the Diversifier
            diversifier = Diversifier(docList, resHitList)
            k = 20
            resultSize = len(docList)
            if( k > resultSize ): k = resultSize
            diverseFileList, diverseDocScoreList, sumX, sumY = diversifier.findMostDiverse(k)

            # Remove the top 'k' from the entire list & add them at the beginning for the final list.
            for nDocIdx in range(k - 1, -1, -1):
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
                    'path': found['path'].split("Legalfiles")[1],

                    'summary': summary
                }

                outputs.append(result)

            return outputs
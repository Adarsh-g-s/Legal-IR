from bs4 import BeautifulSoup
import os
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
            path=ID(stored=True),
            title=TEXT(stored=True),
            contents=TEXT(analyzer=analysis.StemmingAnalyzer(), stored=True, phrase=True)
        )
        return schema

class Search:
    'Search class'


    def getTheQueryParser(self, indexer):
        'Return the query parser with corresponding schema'
        return qparser.MultifieldParser(["title", "contents"], schema=indexer.getSchema(),group=qparser.OrGroup)

    def getResults(self, found, rank):
        print()
        print(rank)
        print("Relevance Score: ", found.score)
        print("Title: ", found['title'])
        print(found['path'])
        summary = found.highlights('contents')
        summary = summary.encode('utf-8')
        print("Summary: ", summary)

    def showResults(self, query, pageNumber,pageLength):
        # pageNumber += 1
        search = Search()
        indexDirectory = search.getIndexDirectory()
        indexReader = open_dir(indexDirectory)
        searcher = indexReader.searcher(weighting=scoring.BM25F(B=0.75, K1=1.5))
        results = searcher.search_page(query,pageNumber,pagelen=pageLength)
        results.results.fragmenter.surround = 50
        # results = searcher.search(query, limit=100)
        # results = searcher.search_page(query, 1)

        return results

    def getIndexDirectory(self):
       indexDirectory = os.getcwd() + '\..\index'
       if not os.path.exists(indexDirectory):
            os.makedirs(indexDirectory)

       return indexDirectory

    @staticmethod
    def passingQuery(queryInput,pageNumber,pageLength):

        search = Search()
        indexDirectory = search.getIndexDirectory()

        indexReader = open_dir(indexDirectory)
        indexer = Indexer()
        queryParser = search.getTheQueryParser(indexer)
        query = queryParser.parse(queryInput)

        # rankingModel = scoring.BM25F(B=0.75,K1=1.5)
        with indexReader.searcher(weighting=scoring.BM25F(B=0.75, K1=1.5)) as searcher:
            #     results=searcher.search(query, terms = True)
            # pageNumber = 0
            # rank = 0
            # totalNumberOfPages = int(len(searcher.search(query)) / 10)
            # pageNumber, rank = search.showResults(query, pageNumber, rank)
            return search.showResults(query, pageNumber,pageLength)




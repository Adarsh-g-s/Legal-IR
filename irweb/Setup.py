'''
Created on Dec 14, 2017

@author: adarsh
'''
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
    
    def getResults(self,found,rank):
        print()
        print(rank)
        print("Relevance Score: ",found.score)
        #Title could be longer than a line, split and display
        title = found['title']
        title = title.split(';',maxsplit=2)
#         print("Title: ",found['title'])
        print("Title: ", title[0]+ "...")
        print(found['path'])
        summary = found.highlights('contents')
        summary = summary.encode('utf-8')
        print("Summary: ",summary)
        
    def showResults(self,query,pageNumber,rank):
        pageNumber+=1
        results = searcher.search_page(query, pageNumber)
        print("Showing ", results.scored_length()," out of ", len(results), "results")
        #         print(results)
                
        for found in results:
            rank+=1
            search.getResults(found,rank)
        return pageNumber,rank
    
    def wantNextPageResults(self):
        print("\n To see next page results \n press Y or y else press N or n")
        return input(" Enter your choice: ")
        

class Setup:
    '''
    Take document path as the user input and pass it to Indexer for Indexing
    '''

    def __init__(self, documentPath, filePath, htmlFileContents,fileTitle, choice, indexDirectory):
        '''
        Constructor
        '''
        self.documentPath = documentPath
        self.filePath = filePath
        self.htmlFileContents = htmlFileContents
        self.fileTitle = fileTitle
        self.choice = choice
        self.indexDirectory = indexDirectory
    
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
            try:
                htmlTitle = htmlTitle.find('h1').get_text()
            except:
                htmlTitle = "No Title found!"
        else:
            try: 
                  htmlTitle=htmlTitle.find('p', class_ = "parties").get_text()
#                   print(htmlTitle)
            except:
                htmlTitle = "No Title found!"
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
        setup.indexDirectory=os.path.join(currentDirectory,"index")
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
                    
setup = Setup(documentPath = None, filePath = None, htmlFileContents= None, fileTitle = None, choice = None, indexDirectory=None)

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
       
        indexFolder = index.create_in(indexDirectory, schema)
    #create the index writer
        indexWriter = indexFolder.writer()
        
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
            totalNumberOfPages = int(len(searcher.search(query))/10)
            pageNumber, rank = search.showResults(query,pageNumber,rank)
            
            while(True):
                setup.choice = search.wantNextPageResults()
                if setup.choice == 'Y' or setup.choice == 'y':
                    pageNumber, rank = search.showResults(query,pageNumber,rank)
                else:
                    break
            
    else:
        exit()
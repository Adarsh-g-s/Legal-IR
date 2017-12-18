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

    def indexing(self,filePath,fileContents, fileTitle):
        try:
            indexWriter.add_document(path = filePath, 
                                     title = fileTitle,
                                     contents = fileContents)   
        except:
            print("Inside the except clause")
           

class Setup:
    '''
    Take document path as the user input and pass it to Indexer for Indexing
    '''

    def __init__(self, documentPath, filePath, htmlFileContents,fileTitle):
        '''
        Constructor
        '''
        self.documentPath = documentPath
        self.filePath = filePath
        self.htmlFileContents = htmlFileContents
        self.fileTitle = fileTitle
    
    def userInput(self):
        self.documentPath = input("Enter the document path")
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
        return htmlContent.find('body').get_text()
    
    def getPathTitleAndContents(self,directory):
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
        #             print(setup.htmlFileContents)
                    # Send parsed output for tokenization, stopword removal and stemming.
                    indexer = Indexer()
                    indexer.indexing(setup.filePath, setup.htmlFileContents,setup.fileTitle)
                else:
                    print("File is in a format other than html")

setup = Setup(documentPath = None, filePath = None, htmlFileContents= None, fileTitle = None)
setup.userInput()

# parse the contents in this document path.
# from the path, go to a file and then parse it.
directory = os.fspath(setup.documentPath)
#create the index writer
#The schema specifies the fields of documents in an index.
schema = Schema(
            path  = ID(stored=True),
            title = TEXT(stored=True),
            contents = TEXT(analyzer=analysis.StemmingAnalyzer(),stored=True, phrase = True)
            )
currentDirectory = os.getcwd()

#creating an index directory
indexDirectory=os.path.join(currentDirectory,"index")
if not os.path.exists(indexDirectory):
    os.makedirs(indexDirectory)
    
print(indexDirectory)
indexFolder = index.create_in(indexDirectory, schema)
indexWriter = indexFolder.writer()

setup.getPathTitleAndContents(directory)

indexWriter.commit()
print("Done!")

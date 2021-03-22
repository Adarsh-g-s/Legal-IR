# Legal-IR (Diversifying Search Results in Legal Information Retrieval System)
Legal Information Retrieval with diversification model - Uses a semantic and a sentiment diversification model for opinion diversification.

## Abstract
We aim to represent the top-k search results which are diversified and relevant,
by applying sentiment and semantic analysis for information retrieval system. Support
Vector Machine (SVM) classifier is used to perform document-level sentiment
classification, whose results are later leveraged to find sentiment distance between
documents. The Semantic analysis includes computation of cosine distance between
documents. We propose a diversification algorithm which maximizes the summation
of sentiment and semantic distances for documents to obtain top k results which
are diversified. We also propose a methodology for evaluation of diversified results
by customizing standard measures like precision, recall and discounted cumulative
gain. We performed a web-based user study to evaluate the built diversified system
against standard information retrieval system, results obtained from user study are
promising.

![image](https://user-images.githubusercontent.com/26891940/112000107-f2473f00-8b1d-11eb-94e6-dfc1c48772f3.png)
Figure 1: Top-3 results for the query "refugee" in the diversified system

![image](https://user-images.githubusercontent.com/26891940/112000340-30dcf980-8b1e-11eb-97fa-6252750c35b2.png)
Figure 2: Semantic differences between document 2 and 3

Python version:3.6

# To run the user study

Copy the mydatabase.db file to any where on your system
and set the directory as specified in the irweb.py to point to that directory.

Note: 1. Please install dependencies(**vader,numpy,nltk** etc) for your IDE.
      2. Sort your import dependencies as per your respective IDE. e.x. below
      3. Create a folder named "rawfiles" and copy all the raw documents inside so they can be opened during the search

PyDev: Folder structure of the project
 
IRSystem                  
 DiversifiedSystem                                       
    * Diversifier.py         
    * Setup.py


If one is importing the Diversifier.py in PyDev then 
1. In Properties set the "SourceFolder" as the project directory(IRSystem).
2. Use the import statement as from DiversifiedSystem.Diversifier import Diversifier in the setup.py file.

Using Visual Studio:
--------------------
While using visual studio to create the prjects from the existing code, .pyproj files will be created for each. Be sure to add Sentiment project as a reference to the created project.

P.S. Copy the html files to the "rawfiles" folder in the current working directory(project directory), to open the files in web.

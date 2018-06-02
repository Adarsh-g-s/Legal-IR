# Legal-IR
Legal Information Retrieval with diversification model

Uses a semantic and a sentiment diversification model for opinion diversification.

Python version:3.6

#To run the user study

Copy the mydatabase.db file to any where on your system
and set the directory as specified in the irweb.py to point to that directory.

Note: 1. Please install dependencies(vader,numpy,nltk etc) for your IDE.
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

# Legal-IR
Legal Information Retrieval with diversification model

Uses a semantic and a sentiment diversification model for opinion diversification.

Python version:3.6

#To run the user study

Copy the mydatabase.db file to any where on your system
and set the directory as specified in the irweb.py to point to that directory.

Note: 1. Please install dependencies(vader,numpy,nltk etc) for your IDE.
      2. Sort your import dependencies as per your respective IDE. e.x. below

PyDev: Folder structure of the project
> IRSystem
  > DiversifiedSystem
    > Diversifier.py
    > Setup.py


If one is importing the Diversifier.py in PyDev then 
1. In Properties set the "SourceFolder" as the project directory(IRSystem).
2. Use the import statement as from DiversifiedSystem.Diversifier import Diversifier in the setup.py file.


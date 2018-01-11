import os
import pathlib
from bs4 import BeautifulSoup

#Folder where files need to be deleted
root = 'C:/Users/adars/Downloads/Temp/Docs/TypesOfHtml/ohio_html'
filesToBeDeleted=[]

for path, subdirs, files in os.walk(root):
    for name in files:
        filePath = path+"/"+name
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
        else:
            filesToBeDeleted.append(filePath) 
            
    
print("Files to be deleted ",filesToBeDeleted)

i=0
while(i<len(filesToBeDeleted)):
    os.remove(filesToBeDeleted[i])
    i=i+1

print("Files were removed")
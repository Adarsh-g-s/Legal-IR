import json as j
import bs4 as b
import os
import pathlib


root = 'C:/Users/adars/Downloads/Temp/Docs/Test'

for path, subdirs, files in os.walk(root):
    for name in files:
        #print( os.path.join(path, name))
        absolutePathToFile = pathlib.PurePath(path, name)
        #print(absolutePathToFile)

        #path = pathlib.PureWindowsPath('D:/Projects/Legal_IR/Doc_Dump/Docs/ca1/3.json')
        #absolutePathToFile = pathlib.PureWindowsPath(absolutePathToFile)


        fRead = open(absolutePathToFile,'r',encoding="utf8")
        parsed_json = j.load(fRead)
        #print(parsed_json['html_with_citations'])

        #Creating a new folder
        htmlFolderName = absolutePathToFile.parent.name+"_html"

        parentDir = absolutePathToFile.parent.parent

        #print(parentDir)

        newPath  = ("%s/%s"%(parentDir,htmlFolderName))

        #print(newPath)
        if not os.path.exists(newPath):
            os.makedirs(newPath)


        #name = 1.json, remove file name after "."
        position=name.index('.')
        fileName = name[:position]
        parsedHtmlFilename = ("%s/%s.html" % (newPath,fileName))
        f = open(parsedHtmlFilename, 'w',encoding="utf8")
        #print(parsedHtmlFilename)

        #Tag to dealt with from Json file
        html_with_citations = parsed_json['html_with_citations']


        #Formatting Html file
        countOfPreTagOpen = str(html_with_citations).count('<pre class=\"inline\">')

        countOfPreTagClose = str(html_with_citations).count('</pre>')

        preTagOpenStr = '<pre class=\"inline\">'

        html_page = str(html_with_citations).replace(preTagOpenStr, 'temp123', 1)

        html_page = html_page.replace(preTagOpenStr,'',countOfPreTagOpen-1)

        html_page = html_page.replace('</pre>','',countOfPreTagClose-1)

        html_page = html_page.replace('temp123',preTagOpenStr,1)

        #Parsing Html file
        d= b.BeautifulSoup(html_page,"lxml")

        #Writing Html file
        f.write(str(d))
        f.close()

        #print(d)

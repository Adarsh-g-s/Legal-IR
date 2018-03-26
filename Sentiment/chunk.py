#code to split into chunks
from bs4 import BeautifulSoup
url = open('E:\\Masters\\3rd semester\\DKE project\\document new\\Religion\\106281.json.html', 'r')#file name
soup=BeautifulSoup(url,"lxml")
data=soup.get_text().replace('\n','\n\n')
paragraphs = data.split("\n\n")
count=0


for value in paragraphs:
    count=count+1
print(count)

#logic to divide into paragraphs. it handles when number of paragraphs are odd numbered also
a=count/3
b=(count-a)/2
c=(count-a-b)

#intiating chunks
chunk1=""
chunk2=""
chunk3=""

#logic to add cumulative counts
x=a
y=x+b
z=y+c

countcumulative=0

#logic to add paragraphs to different chunks
for value in paragraphs:
    if countcumulative<x:
        chunk1=chunk1+value
    elif countcumulative < y:
        chunk2=chunk2+value
    elif countcumulative < z:
        chunk3=chunk3+value
    countcumulative=countcumulative+1

print(chunk1)

print(chunk2)

print(chunk3)

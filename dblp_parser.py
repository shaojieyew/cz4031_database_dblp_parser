import xml.etree.ElementTree as ET
import csv
import string
from w3lib.html import replace_entities
from bs4 import BeautifulSoup

#initalise reader and writer
fr = open( "dblp.xml", "r" )
#fr = open( "test1.txt", "r" )
fr.seek(0, 1)
#fw = open("test.txt","w+")
fw = open('dblp.csv', 'w', encoding='utf-8')
csvwriter = csv.writer(fw, lineterminator="\n")
count=0
record = ''
started = 0
types = ["article","inproceedings","proceedings","book","incollection",
                "phdthesis","mastersthesis","www","data"];
cols=["key","type","author","editor","title","booktitle","pages","year","address","journal","volume","number","month","url","ee","series"]#,"publisher","crossref","isbn","series","school","chapter"]

#write the table header to csv
header =[]
for col in cols:
    header.append(col)
csvwriter.writerow(header)


#remove special character for parse
def remove_non_ascii(text):
    text = replace_entities(text);
    return text;
#check if its the start of an publiObject, if not return nothing
def get_start_parent_element(text):
    for publiType in types:
        if ('<'+publiType+' ') in words:
            return '<'+publiType+' ';
#check if its the end of an publiObject, if not return nothing
def get_end_parent_element(text):
    for publiType in types:
        if ('</'+publiType+'>') in words:
            return '</'+publiType+'>';

#process the information of a publiObject
def endPubli(record, endTag):
    started =0
    record = record+endTag
    #record = remove_non_ascii(record)
    print (count)
    try:
        soup = BeautifulSoup(record)
        #tree = ET.fromstring(record)
    except:
        print( record)
        print ("Unexpected error:"+ sys.exc_info()[0])
    publi =[]
    #key = tree.attrib['key']
    tree = soup.find("body").contents[0]
    key = tree['key']
    publi.append(key)
    publiType = tree.name
    publi.append(publiType)

    authors = "{"
    for member in tree.find_all('author'):
        authors=authors+member.text+","
    if len(authors)>1:
        authors=authors[:len(authors)-1]
    authors=authors+"}"
    authors = str.replace(authors, '"','')
    publi.append(authors)

    editors = "{"
    for member in tree.find_all('editor'):
        editors=editors+member.text+","
    if len(editors)>1:
        editors=editors[:len(editors)-1]
    editors=editors+"}"
    editors = str.replace(editors, '"','')
    publi.append(editors)

    for col in cols:
        if col!='author' and col!='editor' and col!='key' and col!='type':
            value = tree.find(col)
            if value is not None:
                value=value.text
            publi.append(value)

    csvwriter.writerow(publi)

#read line by line XML
for line in fr:
    words = line
    startPubliType =  get_start_parent_element(words);
    endPubliType =  get_end_parent_element(words);

    #if it is end of an object, stop recoding the line and process the object
    if endPubliType is not None and endPubliType in words:
        count=count+1
        try:
            endPubli(record,(endPubliType))
        except:
            print(record)
            print ("Unexpected error:"+ sys.exc_info()[0])
        record=''
        #if count==200:
        #    break

    #if it is start of an object, start to record the lines
    if startPubliType is not None and (startPubliType) in words:
        started=1
        record=''
        if endPubliType is not None:
            words = str.replace(words, (endPubliType),'')

    #only record line if the head of the object was found
    if started==1:
        record = record+words;

#end of the file, close the csv file
fw.close()

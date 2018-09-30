import json
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json

# Importing file from json
reports = []
with open('../ufodata.json') as f:
    for i in f:
        reports.append(json.loads(i))

#Accessing text and creating list of lists with beautiful soup
soup_list2 = []
for idx in range(len(reports)):
    try:
        soup = BeautifulSoup(reports[idx]['html'], 'html.parser')
        lst = [text for text in soup.tbody.stripped_strings]
        soup_list2.append(lst)
    except AttributeError:
        continue

#Joining 'Description' text from end of file
for lst in soup_list2:
    joined = ' '.join(lst[6:])
    lst.insert(6,joined)

#Writing out to csv
with open("../output.csv", "wb") as f:
    writer = csv.writer(f)
    for row in soup_list2:
        row = row[:7]
        row=[s.encode('utf-8') for s in row]
        writer.writerows([row])

#Reloading as pd dataframe
ufo = pd.read_csv('../data/output.csv', header=None)
ufo.rename({0:'Occurred',1:'Reported',2:'Posted',3:'Location',4:'Shape',5:'Duration',6:'Description'},axis=1,inplace=True)
ufo.to_pickle('../data/ufo_db.pkl')

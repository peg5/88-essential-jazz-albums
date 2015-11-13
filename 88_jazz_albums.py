#!/usr/bin/python3

from urllib.request import urlopen
from lxml.html import parse
from pandas.io.parsers import TextParser
from pandas import DataFrame

URL = "http://www.jazzandblues.org/programming/top88/index.aspx"

#Open the website and gather all the HTML info.
parsed = parse(urlopen(URL))
doc = parsed.getroot()

#Find all the HTML info specific to the table that contains the 88 albums.
table = doc.findall(".//table[@id='dgrdTop88list']")

#Function to grab the info from each row of the table.
def _unpack(row):
    elts = row.findall('.//td')
    return [val.text_content() for val in elts]

#Function to organize the table data in a pandas DataFrame-friendly way.
#Has previous function nested within.
def parse_options_data(table):
    rows = table[0].findall('.//tr')
    header = _unpack(rows[0])
    data = [_unpack(r) for r in rows[1:]]
    data_clean = [data[i].strip() for i in data]
    return TextParser(data_clean, names=header).get_chunk()

#Create pandas DataFrame with all the info
final = parse_options_data(table)
print(final)

#Export DataFrame to CSV, excluding columns we don't care about.
#final.to_csv('albums.csv', index=False)

#Notify user of completeion.
#print("Albums written to CSV.")

import os
from csv import DictReader
from pprint import pprint as pp
from collections import defaultdict
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.spells

working_dir = os.path.dirname(os.path.abspath(__file__))
spell_files = [os.path.join(working_dir, f)
               for f in os.listdir(working_dir) if f.endswith('.csv')]

for csv_file in spell_files:
    with open(csv_file, 'r') as fh:
        reader = DictReader(fh)
        print(reader)
        # document = defaultdict()
        # for row in reader:
        #     row[2] = int(row[2])  # Cast level to int
        #     document[row[0]]

import csv
import json
from collections import defaultdict
from pymongo import MongoClient

to_hit = defaultdict(dict)

client = MongoClient('localhost', 27017)
db = client['dnd_database']
collection = db['classes']

with open('ranger.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for i in range(-10, 11):
            to_hit[row["lvl"]][str(i)] = row[str(i)]

filter = {"classname": "ranger"}
newvalue = {"$set": {"to_hit": to_hit}}

collection.update_one(filter, newvalue)

cursor = collection.find({"classname": "ranger"})
for record in cursor:
    print(record)

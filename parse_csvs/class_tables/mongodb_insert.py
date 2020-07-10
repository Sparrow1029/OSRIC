from pymongo import MongoClient
from pprint import pprint
from collections import defaultdict
from class_dicts import RESTRICTIONS_DICT, SAVING_THROWS_DICT, TO_HIT_DICT

client = MongoClient('localhost', 27017)
db = client['dnd_database']
collection = db['classes']

document = defaultdict(dict)

for clss in RESTRICTIONS_DICT:
    document[clss]["restrictions"] = RESTRICTIONS_DICT[clss]
for clss in SAVING_THROWS_DICT:
    document[clss]["saving_throws"] = SAVING_THROWS_DICT[clss]
for clss in TO_HIT_DICT:
    document[clss]["to_hit"] = TO_HIT_DICT[clss]

for key in document:
    document[key].update({"classname": key})
    collection.insert_one(document[key])

cursor = collection.find()
for record in cursor:
    print(record)

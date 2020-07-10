from pymongo import MongoClient
from class_to_hit import TO_HIT_UPDATED

client = MongoClient('localhost', 27017)
db = client['dnd_database']
collection = db['classes']

for clss in TO_HIT_UPDATED:
    filter = {"classname": clss}
    newvalue = {"$set": {"to_hit": TO_HIT_UPDATED[clss]}}
    collection.update_one(filter, newvalue)

cursor = collection.find()
for record in cursor:
    print(record)

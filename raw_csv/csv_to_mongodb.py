from pymongo import MongoClient
import csv
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client.equipment

equipment_files = ['items', 'armor', 'weapons', 'missile_weapons', ]

for name in equipment_files:
    with open(f"{name}.csv", 'r') as f:
        reader = csv.reader(f)
        headers = [h.lower() for h in next(reader, None)]
        for row in reader:
            for i in range(len(row)):
                try:
                    val = float(row[i])
                    if val.is_integer():
                        row[i] = int(val)
                    else:
                        row[i] = val
                except ValueError:
                    pass
            document = dict(zip(headers, row))
            # pprint(dict(zip(headers, row)))
            d_id = db[name].insert_one(document).inserted_id
            print(d_id)

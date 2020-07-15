import os
import csv
from pprint import pprint
from collections import defaultdict
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.equipment

# equipment_files = ['items', 'armor', 'weapons', 'missile_weapons', ]
working_dir = os.path.dirname(os.path.realpath(__file__))
equipment_files = [os.path.join(working_dir, 'equipment_tables', f)
                   for f in os.listdir('equipment_tables')]
race_files = [os.path.join(working_dir, 'race_tables', f)
              for f in os.listdir('race_tables')]
class_files = [os.path.join(working_dir, 'class_tables', f)
               for f in os.listdir('class_tables')]
spell_files = [os.path.join(working_dir,'spell_tables', f)
               for f in os.listdir('spell_tables')]

for name in equipment_files:
    with open(name, 'r') as f:
        reader = csv.reader(f)
        headers = [
            '_'.join(h.replace('/', ' ').split()).lower() for h in next(reader, None)
        ]
        headers[0] = "name"
        if name == 'missile_weapons':
            headers[4] = 'range'
        # print(headers)
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
            # d_id = db[name].insert_one(document).inserted_id
            # pprint(d_id)

class_document = defaultdict()
db = client.classes
for csv_file in class_files:
    embedded_name = os.path.splitext(os.path.basename(csv_file))[0]
    print(embedded_name)
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        if embedded_name == "restrictions":
            headers = [
                '_'.join(h.replace('/', ' ').split()).lower() for h in next(reader, None)
            ][1:]
        else:
            headers = [
                '_'.join(h.replace('/', ' ').split()).lower() for h in next(reader, None)
            ][2:]
        for row in reader:
            class_name = row[0].strip()
            if class_name not in class_document:
                class_document[class_name] = defaultdict()
                class_document[class_name]["to_hit"] = defaultdict()
                class_document[class_name]["restrictions"] = defaultdict()
                class_document[class_name]["saving_throws"] = defaultdict()

            if embedded_name in ["saving_throws", "to_hit"]:
                levels = list(map(int, row[1].split('-')))
                if len(levels) < 2:
                    levels.append(levels[0])
                for i in range(levels[0], levels[1]+1):
                    class_document[class_name][embedded_name][str(i)] = dict(zip(headers, row[2:]))
            elif embedded_name == "restrictions":
                # row[-3] = row[-3].split()
                # create lists for weapons_permitted, shield, armor, alignment
                for i in range(-3, -7, -1):
                    row[i] = row[i].split()
                class_document[class_name][embedded_name] = dict(zip(headers, row[1:]))

# pprint(class_document)


for i in class_document:
    print(f"{i.upper():#^20}")
    to_hit_tbl = class_document[i]["to_hit"]
    for lvl in to_hit_tbl:
        print(f"LEVEL {lvl:#<77}")
        for hit in to_hit_tbl[lvl].keys():
            print(f"{hit: >3}", end=' ')
        print()
        for score in to_hit_tbl[lvl].values():
            print(f"{score: >3}", end=' ')
        print('\n' + '-'*83)

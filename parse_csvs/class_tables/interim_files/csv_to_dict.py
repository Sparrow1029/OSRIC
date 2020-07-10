import csv
import json
# from pprint import pprint as pp
from collections import defaultdict

to_hit_tbl = defaultdict(dict)
to_hit_tbl = {
    "assassin": defaultdict(dict),
    "cleric": defaultdict(dict),
    "thief": defaultdict(dict),
    "paladin": defaultdict(dict),
    "magic_user": defaultdict(dict),
    "ranger": defaultdict(dict),
    "illusionist": defaultdict(dict),
    "druid": defaultdict(dict),
    "fighter": defaultdict(dict),
}
restrictions_tbl = defaultdict(dict)
saving_throws = {
    "assassin": defaultdict(dict),
    "cleric": defaultdict(dict),
    "thief": defaultdict(dict),
    "paladin": defaultdict(dict),
    "magic_user": defaultdict(dict),
    "ranger": defaultdict(dict),
    "illusionist": defaultdict(dict),
    "druid": defaultdict(dict),
    "fighter": defaultdict(dict),
}

# Create class_to_hit file as JSON (manually went in and made it python dict)
with open("to_hit.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if "-" in row["level"]:
            low, high = list(map(int, row["level"].split("-")))
            rng = range(low, high+1)
            for i in rng:
                for roll in [str(r) for r in range(-10, 11)]:
                    to_hit_tbl[row["class"]][i][roll] = int(row[roll])
        else:
            for roll in [str(r) for r in range(-10, 11)]:
                to_hit_tbl[row["class"]][int(row["level"])] = int(row[roll])

out_dict = json.dumps(to_hit_tbl)

with open("class_to_hit.py", "w") as outfile:
    outfile.write(out_dict)

# Create class_restrictions file as above
with open("restrictions.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        for header in reader.fieldnames:
            if header in ["alignment", "armor", "shield", "weapons_permitted"]:
                restrictions_tbl[row["class"]][header] = row[header].split()
            elif header == "penalty_to_hit":
                restrictions_tbl[row["class"]][header] = int(row[header])
            else:
                if row[header].isdigit():
                    restrictions_tbl[row["class"]][header] = int(row[header])
                else:
                    restrictions_tbl[row["class"]][header] = row[header]

# out_dict = json.dumps(restrictions_tbl)

# with open("class_restrictions.py", "w") as outfile:
#     outfile.write(out_dict)

# Create saving_throws file
with open("saving_throws.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if "-" in row["level"]:
            low, high = list(map(int, row["level"].split("-")))
            rng = range(low, high+1)
            for lvl in rng:
                for save in (set(reader.fieldnames) - set(["class", "level"])):
                    saving_throws[row["class"]][lvl][save] = int(row[save])
        else:
            for save in (set(reader.fieldnames) - set(["class", "level"])):
                saving_throws[row["class"]][int(row["level"])][save] = row[save]

# out_dict = json.dumps(saving_throws)

# with open("class_saving_throws.py", "w") as outfile:
#     outfile.write(out_dict)

import os, re
from csv import DictReader
from collections import defaultdict
import json

from database import db
from database.models import (
    Class, Race, ClassRestrictions, Ability, Spell, LevelAdvancement, SpellsByLevel,
    Item, Weapon, Armor
)
from database.seed_data import (
    RESTRICTIONS_DICT, SAVING_THROWS_DICT, TO_HIT_DICT,
    HUMAN, HALFLING, HALF_ELF, HALF_ORC, ELF, GNOME, DWARF
)

db.connect("dnd_database", host="127.0.0.1", port=27017)

classnames = ["druid", "thief", "ranger", "cleric", "fighter", "paladin", "assassin", "magic_user",
              "illusionist"]
races = [HUMAN, HALFLING, HALF_ELF, HALF_ORC, ELF, GNOME, DWARF]

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database/seed_data/")
abilities_file = os.path.join(data_dir, "class_abilities.csv")
spell_file = os.path.join(data_dir, "all_spells.csv")
item_dir = os.path.join(data_dir, "equipment_tables")


class EmbeddedTable:
    def __init__(self, text):
        self.data = text
        self.title = None
        self.headers = None
        self.rows = []
        self.format_embedded_table()

    @staticmethod
    def get_tables(orig):
        tables = []
        capturing = False
        cur_table = []
        for i in range(len(orig)):
            char = orig[i]
            if char == '@':
                capturing = False
                tables.append(''.join(cur_table))
                cur_table = []
            if capturing:
                cur_table.append(char)
            elif char == '$':
                capturing = True
        return tables

    def format_embedded_table(self):
        data = self.data.splitlines()
        if data[0]:
            title, headstr = data[0].split(':')
            self.title = title
            if headstr:
                t_headers = headstr.split('|')
                self.headers = t_headers
        for tbl_row in data[1:]:
            self.rows.append(tbl_row.split('|'))

    def pprint(self):
        if self.headers:
            fmt_str = " {:-^30} |"*len(self.headers)
            headers = fmt_str.format(*self.headers)
        else:
            headers = ''
        if self.title:
            title = "{:^60}".format(self.title)
        else:
            title = ''
        num_fields = len(self.rows[0])
        fmt_row = " {:^30} |"*num_fields
        formatted = [
            title, headers,
            *[fmt_row.format(*row) for row in self.rows]
        ]

        return '\n'.join(formatted)


def parse_spells(csv_file):
    embed_rgx = re.compile(r"\$[^\$]*@", re.S | re.M)

    with open(csv_file, 'r') as f:
        reader = DictReader(f)
        for row in reader:
            embedded_tables = []
            orig_description = row['description']
            if '$' in orig_description:
                new_description = re.sub(embed_rgx, '', orig_description)
                tables = EmbeddedTable.get_tables(orig_description)
                embedded = [EmbeddedTable(data) for data in tables]

                embedded_tables = [
                    {"title": e.title,
                     "headers": e.headers,
                     "rows": e.rows} for e in embedded]

            spell = Spell(
                classname=row["classname"].strip().lower(),
                spellname=row["spellname"].strip().lower(),
                level=row["level"],
                range=row["range"],
                duration=row["duration"],
                aoe=row["aoe"],
                components=row["components"].split(),
                casting_time=row["casting_time"],
                saving_throw=row["saving_throw"],
                description=orig_description,
            )
            if embedded_tables:
                spell.embedded_tables = embedded_tables
                spell.description = new_description

            spell.save()


def parse_class_abilities(csv_file):
    abilities_dict = {
        "fighter": [],
        "paladin": [],
        "cleric": [],
        "thief": [],
        "assassin": [],
        "ranger": [],
        "magic_user": [],
        "illusionist": [],
        "druid": [],
    }
    with open(csv_file, 'r') as f:
        reader = DictReader(f)
        for row in reader:
            ability = defaultdict()
            for header in reader.fieldnames[1:]:
                ability[header] = row[header]
            abilities_dict[row["class"].strip()].append(ability)

    return abilities_dict


def create_classes():
    abilities = parse_class_abilities(abilities_file)
    for name in classnames:
        r = RESTRICTIONS_DICT[name]
        restrictions = ClassRestrictions(
            min_str=r["min_str"],
            min_dex=r["min_dex"],
            min_con=r["min_con"],
            min_int=r["min_int"],
            min_wis=r["min_wis"],
            min_cha=r["min_cha"],
            hit_die=r["hit_die"],
            alignment=r["alignment"],
            shield=r["shield"],
            weapons_permitted=r["weapons_permitted"],
            proficiencies=r["proficiencies"],
            penalty_to_hit=r["penalty_to_hit"]
        )
        class_abilities = [
            Ability(name=a["ability"], level=a["level"], description=a["description"])
            for a in abilities[name]
        ]
        db_class_obj = Class(
            name=name,
            restrictions=restrictions,
            abilities=class_abilities,
            saving_throws=SAVING_THROWS_DICT[name],
            to_hit=TO_HIT_DICT[name],
        )
        db_class_obj.save()


def create_races():
    for race in races:
        if race["abilities"]:
            race_abilities = [Ability(name=k, description=v, level=1) for k, v in race["abilities"].items()]
        else:
            race_abilities = []
        db_race_obj = Race(
            name=race["name"],
            base_stat_mods=race["base_stat_mods"],
            abilities=race_abilities,
            bonuses=race["bonuses"],
            languages=race["languages"],
            max_addl_languages=race["max_addl_languages"],
            permitted_classes=race["permitted_classes"],
            starting_age=race["starting_age"],
            score_limits=race["score_limits"],
            movement_rate=race["movement_rate"],
        )

        db_race_obj.save()


def link_spells():
    for classname in classnames:
        spell_objs = Spell.objects.filter(classname=classname)
        if spell_objs:
            class_obj = Class.objects.get(name=classname)
            class_obj.spells.extend([spell.id for spell in spell_objs])
            class_obj.save()


def insert_items():
    for csv_file in os.listdir(item_dir):
        fpath = os.path.join(item_dir, csv_file)
        reader = DictReader(open(fpath))
        headers = reader.fieldnames
        if headers[0] == "weapon":
            headers[0] = "name"
            for row in reader:
                attrs = {header: row[header].lower() for header in headers}
                json_str = json.dumps(attrs)
                weapon_doc = Weapon.from_json(json_str)
                weapon_doc.save()
        elif headers[0] == "item":
            headers[0] = "name"
            for row in reader:
                attrs = {header: row[header].lower() for header in headers}
                json_str = json.dumps(attrs)
                item_doc = Item.from_json(json_str)
                item_doc.save()
        elif headers[0] == "type":
            headers[0] = "name"
            for row in reader:
                attrs = {header: row[header].lower() for header in headers}
                json_str = json.dumps(attrs)
                armor_doc = Armor.from_json(json_str)
                armor_doc.save()


if __name__ == "__main__":
    pass
    parse_spells(spell_file)
    create_classes()
    create_races()
    link_spells()
    insert_items()

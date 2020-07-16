import os, re
from csv import DictReader
from collections import defaultdict

from database import db
from database.models import (
    Class, Race, ClassRestrictions, Ability, Spell,  # LevelAdvancement, SpellsByLevel,
    # Item, Weapon, Armor
)
from database.seed_data import (
    RESTRICTIONS_DICT, SAVING_THROWS_DICT, TO_HIT_DICT,
    HUMAN, HALFLING, HALF_ELF, HALF_ORC, ELF, GNOME, DWARF
)

db.connect("dnd_database", host="127.0.0.1", port=27017)

classnames = ["druid", "thief", "ranger", "cleric", "fighter", "paladin", "assassin", "magic_user",
              "illusionist"]
races = [HUMAN, HALFLING, HALF_ELF, HALF_ORC, ELF, GNOME, DWARF]

working_dir = os.path.dirname(os.path.abspath(__file__))
abilities_file = os.path.join(working_dir, "database/seed_data/all_spells.csv")
spell_file = os.path.join(working_dir, "database/seed_data/all_spells.csv")


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
    for classname in classnames:
        r = RESTRICTIONS_DICT[classname]
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
            for a in abilities[classname]
        ]
        db_class_obj = Class(
            classname=classname,
            restrictions=restrictions,
            abilities=class_abilities,
            saving_throws=SAVING_THROWS_DICT[classname],
            to_hit=TO_HIT_DICT[classname],
        )
        db_class_obj.save()


def create_races():
    for race in races:
        db_race_obj = Race(
            name=race["name"],
            base_stat_mods=race["base_stat_mods"],
            abilities=race["abilities"],
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
            class_obj = Class.objects.get(classname=classname)
            class_obj.spells.extend([spell.id for spell in spell_objs])
            class_obj.save()


if __name__ == "__main__":
    pass
    parse_spells(spell_file)
    create_classes()
    create_races()
    link_spells()

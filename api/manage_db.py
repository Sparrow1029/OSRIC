from database.db import db
from database.class_models import (
    Class, Race, ClassRestrictions, LevelAdvancement, SpellsByLevel
)
from database.object_models import Ability, Spell  # Item, Weapon, Armor
from database.seed_data.class_dicts import (
    RESTRICTIONS_DICT, SAVING_THROWS_DICT, TO_HIT_DICT
)

from parse_spells import parse_spells, parse_class_abilities
from database.seed_data.races import *

db.connect("dnd_database", host="127.0.0.1", port=27017)

classnames = ["druid", "thief", "ranger", "cleric", "fighter", "paladin", "assassin", "magic_user",
              "illusionist"]
races = [HUMAN, HALFLING, HALF_ELF, HALF_ORC, ELF, GNOME, DWARF]

# abilities_file = "/home/sparrow/Projects/Python/OSRIC/api/database/seed_data/class_abilities.csv"
# spell_file = "/home/sparrow/Projects/Python/OSRIC/api/database/seed_data/all_spells.csv"
abilities_file = "/home/sparrow/Projects/DnDTracker/api/database/seed_data/class_abilities.csv"
spell_file = "/home/sparrow/Projects/DnDTracker/api/database/seed_data/all_spells.csv"
abilities_dict = parse_class_abilities(abilities_file)


def create_classes():
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
            for a in abilities_dict[classname]
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
    # parse_spells(spell_file)
    # create_classes()
    # create_races()
    # link_spells()

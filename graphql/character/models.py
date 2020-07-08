from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField,
    ReferenceField,
    StringField,
    FloatField,
    ListField,
    IntField,
)
from ..dndclass import Class, Race
from ..items import Item, Armor, Weapon


class Inventory(EmbeddedDocument):

    gold = FloatField()
    loot = ListField(Item)
    armor = ListField(Armor)
    weapons = ListField(Weapon)
    equipment = ListField(Item)


class Stats(EmbeddedDocument):

    str = IntField(required=True)
    dex = IntField(required=True)
    con = IntField(required=True)
    int = IntField(required=True)
    wis = IntField(required=True)
    cha = IntField(required=True)

    # def apply_base_stat_race_mods(self, racename):
    #     if racename == 'dwarf':
    #         self.con += 1
    #         self.cha -= 1
    #     elif racename == 'elf':
    #         self.dex += 1
    #         self.con -= 1
    #     elif racename == 'halfling':
    #         self.str -= 1
    #         self.dex += 1
    #     elif racename == 'half-orc':
    #         self.str += 1
    #         self.con += 1
    #         self.cha -= 2


class Character(Document):

    meta = {"collection": "character"}
    name = StringField(max_length=32, required=True)
    stats = EmbeddedDocumentField(Stats, required=True)
    clss = ReferenceField(Class)
    race = ReferenceField(Race)
    cur_campaign = StringField()
    align = StringField(required=True)
    inventory = EmbeddedDocumentField(Inventory)

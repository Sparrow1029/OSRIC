from datetime import datetime
from .db import db
from .object_models import Item, Weapon, Armor
from .class_models import Class, Race


class Stats(db.EmbeddedDocument):
    str = db.IntField(required=True)
    con = db.IntField(required=True)
    dex = db.IntField(required=True)
    int = db.IntField(required=True)
    wis = db.IntField(required=True)
    cha = db.IntField(required=True)


class Inventory(db.EmbeddedDocument):
    gold = db.FloatField()
    loot = db.ListField(db.GenericReferenceField)
    equipped_armor = db.ListField(db.ReferenceField(Armor))
    equipped_weapons = db.ListField(db.ReferenceField(Weapon))
    equipment = db.ListField(db.ReferenceField(Item))


class ThiefChance(db.EmbeddedDocument):
    level = db.IntField()
    climb_walls = db.FloatField()
    find_traps = db.FloatField()
    hear_noise = db.FloatField()
    hide_in_shadows = db.FloatField()
    move_quietly = db.FloatField()
    open_locks = db.FloatField()
    pick_pockets = db.FloatField()
    read_languages = db.FloatField()


class Character(db.Document):
    name = db.StringField(required=True)
    level = db.IntField(default=0)
    stats = db.EmbeddedDocumentField(Stats)
    class_ = db.ReferenceField(Class, db_field="class")  # `class` is a reserved keyword
    race = db.ReferenceField(Race)
    inventory = db.EmbeddedDocumentField(Inventory)
    created_at = db.DateTimeField(default=datetime.utcnow)
    owner = db.ReferenceField('Player')

    def determine_thief_chance():
        # skill_chance = db.EmbeddedDocumentListField(ThiefChance)
        pass

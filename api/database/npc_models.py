from .db import db
from .object_models import Spell, Ability, Note


class Npc(db.Document):
    meta = {"collection": "npcs"}
    name = db.StringField(required=True)
    location = db.StringField(required=True)
    ac = db.IntField()
    to_hit = db.IntField()
    abilities = db.EmbeddedDocumentListField(Ability, null=True)
    spells = db.ListField(db.LazyReferenceField(Spell), null=True)
    notes = db.EmbeddedDocumentListField(Note)


class Monster(db.Document):
    meta = {"collection": "monsters"}
    name = db.StringField(required=True)
    description = db.StringField()
    frequency = db.StringField()
    no_encountered = db.StringField()
    size = db.StringField()
    move = db.IntField()
    ac = db.IntField()
    hit_dice = db.StringField()
    attacks = db.IntField()
    damage = db.StringField()
    special_atk = db.StringField()
    special_def = db.StringField()
    magic_resist = db.StringField()
    lair_probability = db.FloatField()
    intelligence = db.StringField()
    alignment = db.StringField()
    level_xp = db.StringField()

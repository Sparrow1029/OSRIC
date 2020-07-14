from datetime import datetime
from .db import db


class Item(db.Document):
    meta = {"collection": "items"}
    name = db.StringField(required=True)
    weight = db.FloatField()
    cost = db.FloatField()
    special = db.StringField()


class Weapon(db.Document):
    meta = {"collection": "weapons"}
    name = db.StringField(required=True)
    category = db.StringField(required=True)  # missile or melee or magic?
    dmg_sm_md = db.StringField()
    dmg_lg = db.StringField()
    encumbrance = db.FloatField()
    cost = db.FloatField()
    magic = db.StringField()

    # missile weapons only
    rate_of_fire = db.FloatField(null=True)
    rng = db.IntField(null=True)


class Armor(db.Document):
    meta = {"collection": "armor"}
    material = db.StringField()
    encumbrance = db.IntField()
    max_move = db.IntField()
    ac = db.IntField()
    cost = db.FloatField()


class Ability(db.EmbeddedDocument):
    name = db.StringField(required=True)
    level = db.IntField(required=True)
    description = db.StringField(required=True)


class Spell(db.Document):
    meta = {"collection": "spells"}
    classname = db.StringField()
    spellname = db.StringField(required=True)
    level = db.IntField()
    range = db.StringField()
    duration = db.StringField()
    aoe = db.StringField()
    components = db.ListField()
    casting_time = db.StringField()
    saving_throw = db.StringField(default='None')
    description = db.StringField()
    embedded_tables = db.ListField(db.DictField(), null=True)


class Note(db.EmbeddedDocument):
    # date = db.DateTimeField(default=datetime.utcnow)
    author = db.ReferenceField('Player')
    title = db.StringField(max_length=32)
    content = db.StringField(required=True)


class Session(db.EmbeddedDocument):
    date = db.DateTimeField(default=datetime.utcnow)
    notes = db.ListField(db.ObjectIdField())  # Note IDs
    npcs = db.ListField(db.ObjectIdField())
    monsters = db.ListField(db.ObjectIdField())


class Campaign(db.EmbeddedDocument):
    title = db.StringField(required=True)
    dungeon_master = db.ReferenceField('Player')
    players = db.ListField(db.ReferenceField('Player'))
    # players = db.ListField(db.ReferenceField(Player))
    sessions = db.EmbeddedDocumentListField(Session)

from mongoengine import Document
from mongoengine.fields import (
    StringField,
    FloatField,
    IntField,
)


class Item(Document):

    meta = {"collection": "items"}
    name = StringField(required=True)
    weight = FloatField()
    cost = FloatField()
    special = StringField()


class Weapon(Document):

    meta = {"collection": "weapons"}
    name = StringField(required=True)
    category = StringField(required=True)  # missile or melee or magic?
    dmg_sm_md = StringField()
    dmg_lg = StringField()
    encumbrance = FloatField()
    cost = FloatField()
    magic = StringField()

    # missile weapons only
    rate_of_fire = FloatField()
    rng = IntField()


class Armor(Document):

    material = StringField()
    encumbrance = IntField()
    max_move = IntField()
    ac = IntField()
    cost = FloatField()

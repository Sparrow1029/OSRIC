from mongoengine import Document
from mongoengine.fields import (
    IntField,
    StringField,
    ListField,
    ReferenceField
)
from ..dndclass import Class


class Spell(Document):
    meta = {"collection": "spells"}
    clss = ReferenceField(Class)
    spell_name = StringField(required=True, unique=True)
    lvl = IntField()
    rng = StringField()
    duration = StringField()
    aoe = StringField()
    components = ListField()
    saving_throw = StringField(default='None')
    description = StringField()

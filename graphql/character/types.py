import graphene
from graphene_mongo import MongoengineObjectType

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField, EmbeddedDocumentField, ReferenceField, ListField,
    EmbeddedDocumentListField
)


class Stats(EmbeddedDocument):

    str = IntField(required=True)
    dex = IntField(required=True)
    con = IntField(required=True)
    int = IntField(required=True)
    wis = IntField(required=True)
    cha = IntField(required=True)


class ClassMods(EmbeddedDocument):

    min_str = IntField()
    min_dex = IntField()
    min_con = IntField()
    min_int = IntField()
    min_wis = IntField()
    min_cha = IntField()
    hit_die = StringField()
    alignment = StringField()
    armor_type = ListField()
    shield_type = StringField()
    weapons = ListField()
    proficiencies = StringField()
    penalty_to_hit = IntField()


class Ability(EmbeddedDocument):

    meta = {"collection": "ability"}
    name = StringField(max_length=32, required=True)
    description = StringField()


class Character(Document):

    meta = {"collection": "character"}
    name = StringField(max_length=32, required=True)
    stats = EmbeddedDocumentField(Stats, required=True)
    class_ = ReferenceField(Class)
    race = ReferenceField(Race)
    cur_campaign = StringField()
    align = StringField(required=True)

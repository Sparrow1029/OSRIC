import graphene
import graphene_mongo

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField, EmbeddedDocumentListField, 
    StringField, ListField, IntField, ReferenceField
)


class Ability(EmbeddedDocument):

    meta = {"collection": "ability"}
    name = StringField(max_length=32, required=True)
    description = StringField()


class Modifiers(EmbeddedDocument):

    meta = {"collection": "modifiers"}
    type_ = StringField(db_field="type", required=True)
    value = IntField(required=True)


class Race(Document):

    name = StringField(required=True)
    mods = EmbeddedDocumentListField(Modifiers)
    abilities = EmbeddedDocumentListField(Ability)
    permitted_classes = ListField(StringField())


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


class Class(Document):

    meta = {"collection": "class"}
    name = StringField(required=True)
    mods = EmbeddedDocumentField(ClassMods)
    abilities = EmbeddedDocumentListField(Ability)

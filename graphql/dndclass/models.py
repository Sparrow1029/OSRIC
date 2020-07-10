from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    StringField,
    ListField,
    IntField,
)


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
    name = StringField(max_length=32, required=True)
    description = StringField()


class Modifier(EmbeddedDocument):
    name = StringField(db_field="type", required=True)
    value = IntField(required=True)


class Race(Document):
    meta = {"collection": "races"}
    name = StringField(required=True)
    mods = EmbeddedDocumentListField(Modifier)
    abilities = EmbeddedDocumentListField(Ability)
    permitted_classes = ListField(StringField())


class Class(Document):
    meta = {"collection": "classes"}
    name = StringField(required=True)
    mods = EmbeddedDocumentField(ClassMods)
    abilities = EmbeddedDocumentListField(Ability)

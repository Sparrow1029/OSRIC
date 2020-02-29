from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField,
    # EmbeddedDocumentList,
    ReferenceField,
    ObjectIdField,
    StringField,
    ListField,
    IntField,
)


class Stats(EmbeddedDocument):

    str_ = IntField(db_field="str", required=True)
    dex = IntField(required=True)
    con = IntField(required=True)
    int_ = IntField(db_field="int", required=True)
    wis = IntField(required=True)
    cha = IntField(required=True)


class Ability(EmbeddedDocument):

    meta = {"collection": "ability"}
    name = StringField(max_length=32, required=True)
    description = StringField()


class Modifiers(EmbeddedDocument):

    meta = {"collection": "modifiers"}
    type_ = StringField(db_field="type", required=True)


class Race(Document):

    name = StringField(required=True)
    mods = EmbeddedDocumentField(Modifiers)
    abilities = EmbeddedDocumentField(Ability)
    permitted_classes = ListField(StringField())


class Class(Document):

    meta = {"collection": "class"}
    name = StringField(required=True)


class Character(Document):

    meta = {"collection": "character"}
    name = StringField(max_length=32, required=True)
    stats = EmbeddedDocumentField(Stats, required=True)
    class_ = StringField(db_field="class", required=True)
    cur_campaign = StringField()
    align = StringField(required=True)


class Player(Document):

    meta = {"collection": "player"}
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    characters = ListField(ReferenceField(Character))
    real_name = StringField()


class Campaign(Document):

    meta = {"collection": "campaigns"}
    owner = ReferenceField(Player, required=True)
    title = StringField(required=True)
    characters = ListField(ReferenceField(Character))

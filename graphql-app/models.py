from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ReferenceField,
    # ObjectIdField,
    StringField,
    ListField,
    IntField,
)
from flask_bcrypt import generate_password_hash, check_password_hash


class Stats(EmbeddedDocument):

    str_ = IntField(db_field="str", required=True)
    dex = IntField(required=True)
    con = IntField(required=True)
    int_ = IntField(db_field="int", required=True)
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


class Modifiers(EmbeddedDocument):

    meta = {"collection": "modifiers"}
    type_ = StringField(db_field="type", required=True)
    value = IntField(required=True)


class Race(Document):

    name = StringField(required=True)
    mods = EmbeddedDocumentListField(Modifiers)
    abilities = EmbeddedDocumentListField(Ability)
    permitted_classes = ListField(StringField())


class Class(Document):

    meta = {"collection": "class"}
    name = StringField(required=True)
    mods = EmbeddedDocumentField(ClassMods)
    abilities = EmbeddedDocumentListField(Ability)


class Character(Document):

    meta = {"collection": "character"}
    name = StringField(max_length=32, required=True)
    stats = EmbeddedDocumentField(Stats, required=True)
    class_ = ReferenceField(Class)
    race = ReferenceField(Race)
    cur_campaign = StringField()
    align = StringField(required=True)


class Player(Document):

    meta = {"collection": "player"}
    username = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    characters = ListField(ReferenceField(Character))
    real_name = StringField()

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


class Campaign(Document):

    meta = {"collection": "campaigns"}
    owner = ReferenceField(Player, required=True)
    title = StringField(required=True)
    characters = ListField(ReferenceField(Character))

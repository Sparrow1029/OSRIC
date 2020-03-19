import graphene
from graphene_mongo import MongoengineObjectType

from mongoengine import EmbeddedDocument
from mongoengine.fields import (
    StringField, IntField
)

class Ability(EmbeddedDocument):

    meta = {"collection": "ability"}
    name = StringField(max_length=32, required=True)
    description = StringField()


class Modifiers(EmbeddedDocument):

    meta = {"collection": "modifiers"}
    type_ = StringField(db_field="type", required=True)
    value = IntField(required=True)

class gModifiers(MongoengineObjectType):
    class Meta:
        model = CharacterModel

from mongoengine import Document
from mongoengine.fields import (
    ReferenceField,
    StringField,
    ListField
)
from ..player import Player
from ..character import Character


class Campaign(Document):

    meta = {"collection": "campaigns"}
    owner = ReferenceField(Player, required=True)
    title = StringField(required=True)
    characters = ListField(ReferenceField(Character))

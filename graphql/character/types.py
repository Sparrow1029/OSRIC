from graphene_mongo import MongoengineObjectType
from graphene.relay import Node

from .models import Character, Stats, Inventory


class StatsType(MongoengineObjectType):
    class Meta:
        model = Stats
        interfaces = (Node,)


class InventoryType(MongoengineObjectType):
    class Meta:
        model = Inventory
        interfaces = (Node,)


class CharacterType(MongoengineObjectType):
    class Meta:
        model = Character
        interfaces = (Node,)

from graphene_mongo import MongoengineObjectType
from graphene.relay import Node

from .models import Item, Weapon, Armor


class ItemType(MongoengineObjectType):
    class Meta:
        model = Item
        interfaces = (Node,)


class WeaponType(MongoengineObjectType):
    class Meta:
        model = Weapon
        interfaces = (Node,)


class ArmorType(MongoengineObjectType):
    class Meta:
        model = Armor
        interfaces = (Node,)

from graphene import ObjectType, Field
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField

from .mutations import CreateItem, CreateWeapon, CreateArmor
from .types import ItemType, WeaponType, ArmorType


class ItemQueries(ObjectType):
    node = Node.Field()
    all_items = MongoengineConnectionField(ItemType)
    all_weapons = MongoengineConnectionField(WeaponType)
    all_armor = MongoengineConnectionField(ArmorType)
    item = Field(ItemType)
    weapon = Field(WeaponType)
    armor = Field(ArmorType)


class ItemMutations(ObjectType):
    create_item = CreateItem.Field()
    create_weapon = CreateWeapon.Field()
    create_armor = CreateArmor.Field()

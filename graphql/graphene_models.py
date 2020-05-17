# This file provides mappings of pymongo Model objects to graphene MongoEngineObjects
from graphene.relay import Node
from graphene import String, List
from graphene_mongo import MongoengineObjectType

from .models import (
    Campaign as CampaignModel,
    Player as PlayerModel,
    Character as CharacterModel,
    Modifiers as ModifiersModel,
    Ability as AbilityModel,
    Stats as StatsModel,
    Class as ClassModel,
    Race as RaceModel,

    Spell as SpellModel,
    Weapon as WeaponModel,
    Armor as ArmorModel,
    Item as ItemModel,
)

class Campaign(MongoengineObjectType):
    class Meta:
        model = CampaignModel
        interfaces = (Node,)


class Player(MongoengineObjectType):
    class Meta:
        model = PlayerModel
        interfaces = (Node,)


class Race(MongoengineObjectType):
    class Meta:
        model = RaceModel
        interfaces = (Node,)


class Class(MongoengineObjectType):
    class Meta:
        model = ClassModel
        interfaces = (Node,)


class Ability(MongoengineObjectType):
    class Meta:
        model = AbilityModel
        interfaces = (Node,)


class Modifiers(MongoengineObjectType):
    class Meta:
        model = ModifiersModel
        interfaces = (Node,)


class Stats(MongoengineObjectType):
    class Meta:
        model = StatsModel
        interfaces = (Node,)


class Character(MongoengineObjectType):
    # race_name = String()

    class Meta:
        model = CharacterModel
        interfaces = (Node,)

    # def resolve_race_name(parent, info):
    #     race = RaceModel.objects.get(id=parent.race.id)
    #     return str(race.name)


class Weapon(MongoengineObjectType):
    class Meta:
        model = WeaponModel
        interfaces = (Node,)


class Armor(MongoengineObjectType):
    class Meta:
        model = ArmorModel
        interfaces = (Node,)


class Item(MongoengineObjectType):
    class Meta:
        model = ItemModel
        interfaces = (Node,)


class Spell(MongoengineObjectType):
    class Meta:
        model = SpellModel
        interfaces = (Node,)

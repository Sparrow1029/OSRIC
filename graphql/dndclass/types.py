from graphene_mongo import MongoengineObjectType
from graphene.relay import Node

from .models import ClassMods, Ability, Modifier, Race, Class


class ClassModsType(MongoengineObjectType):
    class Meta:
        model = ClassMods
        interfaces = (Node,)


class AbilityType(MongoengineObjectType):
    class Meta:
        model = Ability
        interfaces = (Node,)


class ModifierType(MongoengineObjectType):
    class Meta:
        model = Modifier
        interfaces = (Node,)


class RaceType(MongoengineObjectType):
    class Meta:
        model = Race
        interfaces = (Node,)


class ClassType(MongoengineObjectType):
    class Meta:
        model = Class
        interfaces = (Node,)

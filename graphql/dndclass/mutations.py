from graphene import InputObjectType, Mutation, String, List

from .models import Race, Class, ClassMods, Ability, Modifier
from .types import RaceType, ClassType


class RaceInput(InputObjectType):
    name = String(required=True)
    mods = List(Modifier)
    abilities = List(Ability)
    permitted_classes = List(String)


class ClassInput(InputObjectType):
    name = String(required=True)
    mods = List(Modifier)
    mods = ClassMods()
    abilities = List(Ability)

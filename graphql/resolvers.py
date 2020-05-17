from .models import *
from graphene import String

def resolve_all_players(self, info):
    return list(Player.objects.all())


def resolve_characters(self, info):
    # return list(CharacterModel.objects.filter(**kwargs).all())
    return list(Character.objects.all())


def get_chars_by_class(parent, info, classname=String(required=True)):
    class_obj = Class.objects.get(name=classname)
    return list(Character.objects.get(race=class_obj.id))

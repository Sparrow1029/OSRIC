from graphene_mongo import MongoengineObjectType
from flask_jwt_extended import (
    get_jwt_claims, jwt_required, get_jwt_identity
)

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

from graphene import (
    ObjectType,
    Mutation,
    String,
    Field,
    Union, List,
)

# from flask_graphql_auth import (
#     AuthInfoField,
#     query_jwt_required,
#     get_jwt_claims,
#     get_jwt_data,
# )


class Campaign(MongoengineObjectType):
    class Meta:
        model = CampaignModel


class Player(MongoengineObjectType):
    class Meta:
        model = PlayerModel


class Race(MongoengineObjectType):
    class Meta:
        model = RaceModel


class Class(MongoengineObjectType):
    class Meta:
        model = ClassModel


class Ability(MongoengineObjectType):
    class Meta:
        model = AbilityModel


class Modifiers(MongoengineObjectType):
    class Meta:
        model = ModifiersModel


class Stats(MongoengineObjectType):
    class Meta:
        model = StatsModel


class Character(MongoengineObjectType):
    class Meta:
        model = CharacterModel


class Weapon(MongoengineObjectType):
    class Meta:
        model = WeaponModel


class Armor(MongoengineObjectType):
    class Meta:
        model = ArmorModel


class Item(MongoengineObjectType):
    class Meta:
        model = ItemModel


class Spell(MongoengineObjectType):
    class Meta:
        model = SpellModel


# class Claims(ObjectType):
#     claims = String()
def resolve_all_characters(self, info):
    return list(CharacterModel.objects.all())


class Query(ObjectType):
    all_characters = List(Character, resolver=resolve_all_characters)
    all_players = List(Player)
    find_character = Field(Character, name=(String(required=True)))
    find_race = Field(Race, name=(String(required=True)))
    find_class = Field(Class, name=(String(required=True)))
    # get_claims = Field(Claims)
    # @jwt_required
    def resolve_all_characters(self, info):
        return list(CharacterModel.objects.all())

    # @jwt_required
    def resolve_all_players(self, info):
        print(get_jwt_claims())
        print(get_jwt_identity())
        return list(PlayerModel.objects.all())

    def resolve_find_character(self, info, name):
        return CharacterModel.objects.get(name=name)

    def resolve_find_race(self, info, name):
        return RaceModel.objects.get(name=name)

    def resolve_find_class(self, info, name):
        return ClassModel.objects.get(name=name)

    # def resolve_get_claims(self, info):
    #     claims = get_jwt_claims()
    #     return Claims(claims=claims)


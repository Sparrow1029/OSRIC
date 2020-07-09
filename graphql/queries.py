# from graphene_mongo import MongoengineObjectType
from .graphene_models import (
    # Campaign,
    Player,
    Character,
    # Modifiers,
    # Ability,
    # Stats,
    Class,
    Race,
)
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField
# from flask_jwt_extended import (
#     get_jwt_claims,
#      jwt_required,
#     get_jwt_identity # )


from graphene import (
    ObjectType,
    # Mutation,
    # String,
    # Field,
    # Union,
    # List,
)


# class Claims(ObjectType):
#     claims = String()
# def resolve_all_characters(self, info):
#     return list(CharacterModel.objects.all())


class Query(ObjectType):
    # all_characters = List(Character, resolver=resolve_all_characters)
    node = Node.Field()
    # all_players = List(Player, resolver=resolve_all_players)
    # find_character = Field(Character, name=(String(required=True)))
    # find_race = Field(Race, name=(String(required=True)))
    # find_class = Field(Class, name=(String(required=True)))
    # characters = List(Character, resolver=resolve_characters)
    players = MongoengineConnectionField(Player)
    races = MongoengineConnectionField(Race)
    classes = MongoengineConnectionField(Class)
    characters = MongoengineConnectionField(Character)
    # get_claims = Field(Claims)
    # @jwt_required
    # def resolve_all_characters(self, info):
    #     return list(CharacterModel.objects.all())

    # @jwt_required
    # def resolve_all_players(self, info):
    #     print(get_jwt_claims())
    #     print(get_jwt_identity())
    #     return list(PlayerModel.objects.all())
    # def resolve_get_claims(self, info):
    #     claims = get_jwt_claims()
    #     return Claims(claims=claims)


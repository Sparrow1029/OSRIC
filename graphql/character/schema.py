from graphene import ObjectType, Field
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField

from .mutations import CreateCharacter
from .types import CharacterType


class CharacterQueries(ObjectType):
    node = Node.Field()
    characters = MongoengineConnectionField(CharacterType)
    character = Field(CharacterType)


class CharacterMutations(ObjectType):
    create_character = CreateCharacter.Field()

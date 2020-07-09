from graphene import ObjectType, Field
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField

from .mutations import CreatePlayer
from .types import PlayerType


class PlayerQueries(ObjectType):
    node = Node.Field()
    players = MongoengineConnectionField(PlayerType)
    player = Field(PlayerType)


class PlayerMutations(ObjectType):
    create_player = CreatePlayer.Field()

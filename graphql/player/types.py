from graphene_mongo import MongoengineObjectType
from graphene.relay import Node

from .models import Player


class PlayerType(MongoengineObjectType):
    class Meta:
        model = Player
        interfaces = (Node,)

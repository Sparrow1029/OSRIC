from graphene_mongo import MongoengineObjectType
from .models import Player as PlayerModel


class Player(MongoengineObjectType):
    class Meta:
        model = PlayerModel

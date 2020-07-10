from graphene.relay import Node
from graphene_mongo import MongoengineObjectType

from .models import Campaign


class CampaignType(MongoengineObjectType):
    class Meta:
        model = Campaign
        interfaces = (Node,)

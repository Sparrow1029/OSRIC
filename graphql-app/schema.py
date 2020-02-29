import graphene
# from graphene.relay import Node
# from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from graphene_mongo import MongoengineObjectType

from models import Stats as StatsModel
from models import Character as CharacterModel


class Stats(MongoengineObjectType):
    class Meta:
        model = StatsModel


class Character(MongoengineObjectType):
    class Meta:
        model = CharacterModel


class CharacterInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    str_ = graphene.Int()
    dex = graphene.Int()
    con = graphene.Int()
    int_ = graphene.Int()
    wis = graphene.Int()
    cha = graphene.Int()
    align = graphene.String()
    class_ = graphene.String()
    cur_campaign = graphene.String()

class CreateCharacter(graphene.Mutation):
    character = graphene.Field(Character)

    class Arguments:
        char_data = CharacterInput(required=True)

    def mutate(self, info, char_data=None):
        stats = StatsModel(
            str_ = char_data.str_,
            con = char_data.con,
            dex = char_data.dex,
            int_ = char_data.int_,
            wis = char_data.wis,
            cha = char_data.cha,
        )
        if char_data.cur_campaign:
            cur_campaign = char_data.cur_campaign
        else:
            cur_campaign = 'none'
        character = CharacterModel(
            name = char_data.name,
            class_ = char_data.class_,
            stats = stats,
            cur_campaign = cur_campaign,
            align = char_data.align,
        )
        character.save()

        return CreateCharacter(character=character)


class Query(graphene.ObjectType):
    characters = graphene.List(Character)

    def resolve_characters(self, info):
        return list(CharacterModel.objects.all())


class Mutations(graphene.ObjectType):
    create_character = CreateCharacter.Field(description="Make a new character")


schema = graphene.Schema(query=Query, mutation=Mutations, types=[Stats, Character])

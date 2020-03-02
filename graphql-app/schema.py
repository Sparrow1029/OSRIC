import graphene
# from graphene.relay import Node
# from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from graphene_mongo import MongoengineObjectType  # MongoengineConnectionField

from models import Character as CharacterModel
from models import Modifiers as ModifiersModel
from models import Ability as AbilityModel
from models import Stats as StatsModel
from models import Class as ClassModel
from models import Race as RaceModel

from models import Campaign as CampaignModel
from models import Player as PlayerModel


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
    race = graphene.String()
    class_ = graphene.String()
    cur_campaign = graphene.String()


class PlayerInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    characters = graphene.List(graphene.String)
    real_name = graphene.String()


class RegisterPlayer(graphene.Mutation):
    player = graphene.Field(Player)

    class Arguments:
        player_data = PlayerInput(required=True)

    def mutate(self, info, player_data=None):
        char_ids = [CharacterModel.objects.get(name=char).id
                    for char in player_data.characters]
        player = PlayerModel(
            username=player_data.username,
            password=PlayerModel.set_password(player_data.password),
            characters=char_ids,
            real_name=player_data.real_name or 'anonymous'
        )
        player.save()

        return RegisterPlayer(player=player)


class CreateCharacter(graphene.Mutation):
    character = graphene.Field(Character)

    class Arguments:
        char_data = CharacterInput(required=True)

    def mutate(self, info, char_data=None):
        if char_data.cur_campaign:
            cur_campaign = char_data.cur_campaign
        else:
            cur_campaign = 'none'
        get_class = ClassModel.objects.get(name=char_data.class_).id
        get_race = RaceModel.objects.get(name=char_data.race).id
        stats = StatsModel(
            str_=char_data.str_,
            con=char_data.con,
            dex=char_data.dex,
            int_=char_data.int_,
            wis=char_data.wis,
            cha=char_data.cha,
        )
        character = CharacterModel(
            name=char_data.name,
            race=get_race,
            class_=get_class,
            stats=stats,
            cur_campaign=cur_campaign,
            align=char_data.align,
        )
        character.save()

        return CreateCharacter(character=character)


class CheckPassword(graphene.Mutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, username, password):
        player = PlayerModel.objects.get(username=username)
        if player.check_password_hash(password):
            return CheckPassword(ok=True)
        return CheckPassword(ok=False)


class Query(graphene.ObjectType):
    all_characters = graphene.List(Character)
    all_players = graphene.List(Player)
    find_character = graphene.Field(Character, name=(graphene.String(required=True)))
    find_race = graphene.Field(Character, name=(graphene.String(required=True)))
    find_class = graphene.Field(Class, name=(graphene.String(required=True)))

    def resolve_all_characters(self, info):
        return list(CharacterModel.objects.all())

    def resolve_all_players(self, info):
        return list(PlayerModel.objects.all())

    def resolve_find_character(self, info, name):
        return CharacterModel.objects.get(name=name)

    def resolve_find_race(self, info, name):
        return RaceModel.objects.get(name=name)

    def resolve_find_class(self, info, name):
        return ClassModel.objects.get(name=name)


class Mutations(graphene.ObjectType):
    create_character = CreateCharacter.Field(description="Make a new character")
    register_player = RegisterPlayer.Field(description="Register a new user")
    check_password = CheckPassword.Field(description="Check user password (bCrypt)")


schema = graphene.Schema(
    query=Query,
    mutation=Mutations,
    types=[
        Character,
        Modifiers,
        Ability,
        Player,
        Stats,
        Class,
        Race,
    ])

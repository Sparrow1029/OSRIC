from bson import ObjectId
# from qlmain import jwt
from models import (
    Campaign as CampaignModel,
    Player as PlayerModel,
    Character as CharacterModel,
    Modifiers as ModifiersModel,
    Stats as StatsModel,
    Class as ClassModel,
    Race as RaceModel,
)

from queries import (
    Campaign,
    Player,
    Character,
    Modifiers,
    Ability,
    Stats,
)
from graphene import (
    InputObjectType, ObjectType,
    Mutation,
    Boolean,
    Field,
    String,
    List,
    Int,
    ID,
)

# from auth import AuthMutation, RefreshMutation  # , GetClaims
# from flask_graphql_auth import (
#     mutation_jwt_refresh_token_required,
#     mutation_jwt_required
# )

class CharacterInput(InputObjectType):
    id = ID()
    player_id = String()
    name = String()
    str = Int()
    dex = Int()
    con = Int()
    int = Int()
    wis = Int()
    cha = Int()
    align = String()
    race = String()
    class_ = String()
    cur_campaign = String()


class PlayerInput(InputObjectType):
    id = ID()
    username = String(required=True)
    password = String(required=True)
    characters = List(String)
    real_name = String()


class RegisterPlayer(Mutation):
    player = Field(Player)

    class Arguments:
        player_data = PlayerInput(required=True)

    def mutate(self, info, player_data=None):
        char_ids = []
        if player_data.characters:
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


class CreateCharacter(Mutation):
    character = Field(Character)

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
            str=char_data.str,
            con=char_data.con,
            dex=char_data.dex,
            int=char_data.int,
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


class CheckPassword(Mutation):
    class Input:
        username = String(required=True)
        password = String(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(self, info, username, password):
        player = PlayerModel.objects.get(username=username)
        if player.check_password_hash(password):
            return CheckPassword(ok=True)
        return CheckPassword(ok=False)


class Mutations(ObjectType):
    create_character = CreateCharacter.Field(description="Make a new character")
    register_player = RegisterPlayer.Field(description="Register a new user")
    check_password = CheckPassword.Field(description="Check user password (bCrypt)")
    # create_auth_token = AuthMutation.Field(description="Create JWT auth token")
    # refresh_token = RefreshMutation.Field(description="Assign refresh token")
    # get_claims = GetClaims.Field(description="Get user_claims from JWT")

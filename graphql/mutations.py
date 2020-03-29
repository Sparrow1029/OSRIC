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
    Weapon as WeaponModel,
    Item as ItemModel,
    Spell as SpellModel,
)

from queries import (
    Campaign, Player, Character, Modifiers, Ability, Stats, Weapon,
    Armor, Item, Spell

)
from graphene import (
    InputObjectType, ObjectType, Mutation, Boolean, Field, String,
    List, Int, Float, ID,
)

# from auth import AuthMutation, RefreshMutation  # , GetClaims
# from flask_graphql_auth import (
#     mutation_jwt_refresh_token_required,
#     mutation_jwt_required
# )


class AbilityInput(InputObjectType):
    name = String(max_length=32, required=True)
    description = String(required=True)


class ItemInput(InputObjectType):
    name = String(required=True)
    weight = Float()
    cost = Float()
    special = String()


class WeaponInput(InputObjectType):
    name = String(required=True)
    type = String(required=True)
    dmg_sm_md = String(required=True)
    dmg_lg = String(required=True)
    encumbrance = Float(required=True)
    rate_of_fire = Float()
    rng = Int()


class SpellInput(InputObjectType):
    clss = String(required=True)
    spell_name = String(required=True)
    lvl = Int(required=True)
    rng = String()
    aoe = String()
    components = List(String)
    saving_throw = String()
    description = String()


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


class CreateSpell(Mutation):
    class Arguments:
        spell_data = SpellInput(required=True)

    spell = Field(Spell)

    def mutate(self, info, spell_data=None):
        spell = SpellModel(
            clss=spell_data.clss,
            spell_name=spell_data.spell_name,
            lvl=spell_data.lvl,
            rng=spell_data.rng,
            duration=spell_data.duration,
            aoe=spell_data.aoe,
            components=spell_data.components,
            saving_throw=spell_data.saving_throw,
            description=spell_data.description,
        ) 
        spell.save()

        return CreateSpell(spell=spell)


class CreateWeapon(Mutation):
    class Arguments:
        weapon_data = WeaponInput(required=True)

    weapon = Field(Weapon)

    def mutate(self, info, weapon_data=None):
        rate_of_fire = weapon_data.rate_of_fire or '-'
        rng = weapon_data.rate_of_fire or '-'
        magic = weapon_data.magic or '-'

        weapon = WeaponModel(
            name=weapon_data.name,
            type=weapon_data.type,
            dmg_sm_md=weapon_data.dmg_sm_md,
            dmg_lg=weapon_data.dmg_lg,
            encumbrance=weapon_data.encumbrance,
            cost=weapon_data.cost,
            rate_of_fire=rate_of_fire,
            rng=rng,
            magic=magic
        )
        weapon.save()

        return CreateWeapon(weapon=weapon)


class RegisterPlayer(Mutation):
    class Arguments:
        player_data = PlayerInput(required=True)

    player = Field(Player)

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
    class Arguments:
        char_data = CharacterInput(required=True)

    character = Field(Character)

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

from graphene import InputObjectType, Mutation, Field, String, Int

from .models import Character, Stats, Inventory
from .types import CharacterType, StatsType, InventoryType
from ..dndclass.models import Race, Class


class CharacterInput(InputObjectType):
    # id = ID()
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
    clss = String()
    cur_campaign = String()


class CreateCharacter(Mutation):
    class Arguments:
        char_data = CharacterInput(required=True)

    character = Field(CharacterType)

    def mutate(self, info, char_data=None):
        if char_data.cur_campaign:
            cur_campaign = char_data.cur_campaign
        else:
            cur_campaign = 'none'
        classname = char_data.classname.lower()
        racename = char_data.racename.lower()
        get_class = Class.objects.get(name=classname).id
        get_race = Race.objects.get(name=racename).id
        stats = Stats(
            str=char_data.str,
            con=char_data.con,
            dex=char_data.dex,
            int=char_data.int,
            wis=char_data.wis,
            cha=char_data.cha,
        )
        stats.apply_base_stat_race_mods(racename)
        character = Character(
            name=char_data.name,
            raceref=get_race,
            racename=racename,
            classref=get_class,
            classname=classname,
            stats=stats,
            cur_campaign=cur_campaign,
            align=char_data.align,
        )
        character.save()

        return CreateCharacter(character=character)

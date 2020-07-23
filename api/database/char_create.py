import json
from .models import Race, Class, ThiefChance, Spell, Inventory, Character


def init_abilities(char):
    race_abls = Race.objects.get(id=char.raceref.id).abilities
    clss_abls = Class.objects.get(id=char.classref.id).abilities
    char.abilities = race_abls + clss_abls


def link_player(char, player):
    char.owner = player
    char.save()
    player.add_character(char.id)
    player.save()


def init_thief_skills(char):
    classname = char.classref.name
    if classname not in ["thief", "assassin"]:
        return
    Thief = Class.objects.get(name="thief")
    raceref = Race.objects.get(name=char.raceref.name)
    race_adj = raceref.thief_skill_adj
    print(race_adj._fields)
    base_list = [obj.to_json() for obj in Thief.thief_skill_chance]
    dicts = list(map(lambda x: json.loads(x), base_list))
    # adjust for dexterity score and race
    for d in dicts:
        for key in d.keys():
            if key == "level":
                continue
            if char.base_stats.dex in [9, 10, 11, 12, 16, 17, 18, 19]:
                dex_adj = Thief.thief_dex_adj.get(level=char.base_stats.dex)
                d[key] += dex_adj[key]
            d[key] += race_adj[key]

    char.thief_tbl = [ThiefChance.from_json(json.dumps(d)) for d in dicts]
    char.cur_thief_skills = [
        d for d in dicts if d["level"] == 1
    ][0]


def add_initial_spells(char):
    classname = char.classref.name
    if classname in ["druid", "cleric", "magic_user", "illusionist"]:
        char.available_spells = list(Spell.objects.filter(classname=classname, level=1))


def create_character(payload, player):
    char_class = Class.objects.get(name=payload["class"])
    char_race = Race.objects.get(name=payload["race"])
    del payload["class"]
    del payload["race"]
    payload["classref"] = char_class.id
    payload["raceref"] = char_race.id

    # apply race modifiers to stats
    for stat in char_race.base_stat_mods:
        payload["base_stats"][stat] += char_race.base_stat_mods[stat]

    char = Character(**payload)
    char.save()  # Save object first before adding initial stuff
    init_abilities(char)
    init_thief_skills(char)
    add_initial_spells(char)
    char.inventory = Inventory()
    char.cur_stats = char.base_stats
    link_player(char, player)
    return char

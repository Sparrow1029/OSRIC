from .fields import MongoId
from flask_restx import fields

from ..routes import dnd_api as api
from .spells import spell
from .classes import class_, race
# from .players import player
from .objects import item, weapon, armor, item_inventory, weapon_inventory, armor_inventory

stats = api.model("StatsModel", {
    "str": fields.Integer,
    "con": fields.Integer,
    "dex": fields.Integer,
    "int": fields.Integer,
    "wis": fields.Integer,
    "cha": fields.Integer
})

ability = api.model("Ability", {
    "name": fields.String, "level": fields.Integer, "description": fields.String
})

inventory = api.model("Inventory", {
    "gold": fields.Float,
    "armor": fields.List(fields.Nested(armor_inventory)),
    "weapons": fields.List(fields.Nested(weapon_inventory)),
    "items": fields.List(fields.Nested(item_inventory)),
})

character_input = api.model("CharacterInput", {
    "name": fields.String(required=True),
    "base_stats": fields.Nested(stats),
    "class": fields.String(attr="classref"),
    "race": fields.String(attr="raceref"),
    "gender": fields.String
})

equipped_weapons = api.model("EquippedWeapons", {
    "main": fields.Nested(weapon),
    "secondary": fields.Nested(weapon),
    "missile": fields.Nested(weapon),
    "other1": fields.Nested(weapon),
    "other2": fields.Nested(weapon)
})

equipped_armor = api.model("EquippedArmor", {
    "armor": fields.Nested(armor),
    "shield": fields.Nested(armor),
    "hands": fields.List(fields.Nested(armor)),
    "other": fields.List(fields.Nested(armor))
})

equipped_items = api.model("EquippedItems", {
    "feet": fields.Nested(item),
    "clothes": fields.List(fields.Nested(item)),
    "cape": fields.Nested(item),
    "other": fields.List(fields.Nested(item))
})

equipment = api.model("Equipment", {
    "weapons": fields.Nested(equipped_weapons),
    "items": fields.Nested(equipped_items),
    "armor": fields.Nested(equipped_items),
}, skip_none=True)

memorized_spell = api.clone("MemSpells", spell, {
    "num_remaining": fields.Integer
})

player_ref = api.model("PlayerRef", {
    "id": MongoId,
    "username": fields.String,
    "email": fields.String,
    "real_name": fields.String,
    "characters": fields.List(MongoId),
    "created_at": fields.DateTime,
})

character = api.model("Character", {
    "id": MongoId,
    "name": fields.String,
    "level": fields.Integer,
    "base_stats": fields.Nested(stats),
    "cur_stats": fields.Nested(stats),
    "classref": fields.Nested(class_, skip_none=True),
    "raceref": fields.Nested(race, skip_none=True),
    "abilities": fields.List(fields.Nested(ability)),
    "gender": fields.String,

    "cur_hp": fields.Integer,
    "max_hp": fields.Integer,
    "exp": fields.Integer,
    "alive": fields.Boolean,
    "status_effects": fields.Raw,
    "inventory": fields.Nested(inventory),
    "equipped": fields.Nested(equipment, skip_none=True),
    "available_spells": fields.List(fields.Nested(spell, skip_none=True)),
    "cur_spells": fields.List(fields.Nested(memorized_spell, skip_none=True)),
    "skill_chance": fields.Raw,

    "created_at": fields.DateTime,
    "public": fields.Boolean(description="Is this character visible to all users"),
    "owner": fields.Nested(player_ref, skip_none=True)
})

character_update = api.model("CharacterUpdate", {
    "cur_stats": fields.Nested(stats),
    "status_effects": fields.List(fields.String),
    "inventory": fields.Raw,
    "equipped": fields.Raw,
})

from flask_restx import fields
from .fields import MongoId

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
    "name": fields.String,
    "level": fields.Integer,
    "description": fields.String
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

equipment = api.model("Equipment", {
    "armor": fields.List(fields.Nested(armor)),
    "weapons": fields.List(fields.Nested(weapon)),
    "items": fields.List(fields.Nested(item))
})

memorized_spell = api.clone("MemSpells", spell, {
    "num_remaining": fields.Integer
})

ref = api.model("Ref", {
    "name": fields.String,
    "classname": fields.String,
    "username": fields.String,
    "id": MongoId
})

character = api.model("Character", {
    "id": MongoId,
    "name": fields.String,
    "level": fields.Integer,
    "base_stats": fields.Nested(stats),
    "cur_stats": fields.Nested(stats),
    # "classref": fields.Nested(class_, mask="{classref{name,id}}"),
    "classref": fields.Nested(ref, skip_none=True),
    # "raceref": fields.Nested(race, mask="{raceref{name,id}}"),
    "raceref": fields.Nested(ref, skip_none=True),
    "abilities": fields.List(fields.Nested(ability)),
    "gender": fields.String,

    "cur_hp": fields.Integer,
    "max_hp": fields.Integer,
    "exp": fields.Integer,
    "alive": fields.Boolean,
    "status_effects": fields.Raw,
    "inventory": fields.Nested(inventory),
    "equipped": fields.Nested(equipment),
    "available_spells": fields.List(fields.Nested(ref, skip_none=True)),
    "cur_spells": fields.List(fields.Nested(memorized_spell, skip_none=True)),
    "skill_chance": fields.Raw,

    "created_at": fields.DateTime,
    "public": fields.Boolean(description="Is this character visible to all users"),
    "owner": fields.Nested(ref, skip_none=True)
})

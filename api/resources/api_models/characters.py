from flask_restx import fields
from .fields import MongoId

from ..routes import dnd_api as api
from .spells import spell
from .classes import class_, race
# from .players import player
from .objects import item, weapon, armor, item_inventory, weapon_inventory, armor_inventory

stats = api.model("Stats", {
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
    "class_": fields.String,
    "race": fields.String,
    "gender": fields.String
})

equipment = api.model("Equipment", {
    "armor": fields.List(fields.Nested(armor)),
    "weapons": fields.List(fields.Nested(weapon)),
    "items": fields.List(fields.Nested(item))
})

memorized_spell = api.clone("MemorizedSpells", spell, {
    "num_remaining": fields.Integer
})

character = api.clone("Character", character_input, {
    "id": MongoId,
    "level": fields.Integer,
    "cur_stats": fields.Nested(stats),
    "class": fields.Nested(class_),
    "race": fields.Nested(race),
    "abilities": fields.List(fields.Nested(ability)),
    "gender": fields.String,

    "cur_hp": fields.Integer,
    "max_hp": fields.Integer,
    "exp": fields.Integer,
    "alive": fields.Boolean,
    "status_effects": fields.Raw,
    "inventory": fields.Nested(inventory),
    "equipped": fields.Nested(equipment),
    "cur_spells": fields.List(fields.Nested(memorized_spell)),
    "skill_chance": fields.Raw,

    "created_at": fields.DateTime,
    "public": fields.Boolean(description="Is this character visible to all users"),
    "owner": MongoId
})

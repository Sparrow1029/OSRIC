from flask_restx import fields
from .fields import MongoId

from ..routes import dnd_api as api
from .spells import spell
from .classes import class_

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
    "loot": fields.List(fields.Raw),
    "armor": fields.List(fields.Raw),
    "weapons": fields.List(fields.Raw),
    "items": fields.List(fields.Raw),  # Items?
})

character_input = api.model("CharacterInput", {
    "name": fields.String(required=True),
    "stats": fields.Nested(stats),
    "class_": fields.Nested(class_),
    "race": MongoId,
})

character = api.clone("Character", character_input, {
    "id": MongoId,
    "level": fields.Integer,
    "abilities": fields.List(fields.Nested(ability)),

    "gold": fields.Float,
    "cur_hp": fields.Integer,
    "cur_status": fields.List(fields.String),
    "cur_spells": fields.List(fields.Nested(spell)),
    "inventory": fields.Nested(inventory),
    "equipment": fields.Raw,

    "public": fields.Boolean(description="Is this character visible to all users"),
    "created_at": fields.DateTime,
    "owner": MongoId
})

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


character_input = api.model("CharacterInput", {
    "name": fields.String(required=True),
    "level": fields.Integer,
    "stats": fields.Nested(stats),
    "class_": fields.Nested(class_),
    "race": MongoId,
})

character = api.clone("Character", character_input, {
    "id": MongoId,
    "cur_hp": fields.Integer,
    "cur_status": fields.List(fields.String),
    "cur_spells": fields.List(fields.Nested(spell)),
    "created_at": fields.DateTime,
    "inventory": fields.Raw,
    "owner": MongoId
})

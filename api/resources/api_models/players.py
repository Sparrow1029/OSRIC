from flask_restx import fields
from .fields import MongoId

from ..routes import dnd_api as api
from .characters import character

login = api.model("Login", {
    "username": fields.String(required=True),
    "password": fields.String(required=True)
})

player_input = api.clone("PlayerInput", login, {
    "email": fields.String,
    "real_name": fields.String,
})

player = api.clone("Player", player_input, {
    "id": MongoId,
    "characters": fields.List(fields.Nested(character)),
    "created_at": fields.DateTime,
})

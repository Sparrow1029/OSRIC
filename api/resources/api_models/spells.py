from flask_restx import fields
from .fields import MongoId

from ..routes import dnd_api as api

spell_input = api.model("SpellInput", {
    "classname": fields.String,
    "spellname": fields.String(required=True),
    "level": fields.Integer,
    "range": fields.String,
    "duration": fields.String,
    "aoe": fields.String,
    "components": fields.List(fields.String),
    "saving_throw": fields.String(default='None'),
    "description": fields.String,
    "embedded_tables": fields.List(fields.Raw)
})  # , mask="{id,spellname,classname}")

spell = api.clone("Spell", spell_input, {
    "id": MongoId
})

from flask_restx import fields
from .fields import MongoId  # , BsonObjectId

from ..routes import dnd_api as api

item_input = api.model("ItemInput", {
    "name": fields.String,
    "weight": fields.Float,
    "cost": fields.Float,
    "description": fields.String,
    "magic": fields.Boolean
})

item = api.clone("Item", item_input, {
    "id": MongoId
})

item_inventory = api.model("ItemInventory", {
    "info": fields.Nested(item),
    "count": fields.Integer
})

armor_input = api.model("ArmorInput", {
    "name": fields.String,
    "encumbrance": fields.Float,
    "max_move": fields.Integer,
    "ac": fields.Integer,
    "cost": fields.Float,
    "description": fields.String,
    "magic": fields.Boolean
})

armor = api.clone("Armor", armor_input, {
    "id": MongoId
})

armor_inventory = api.model("ArmorInventory", {
    "info": fields.Nested(armor),
    "count": fields.Integer
})

weapon_input = api.model("WeaponInput", {
    "name": fields.String,
    "category": fields.String,
    "dmg_sm_md": fields.String,
    "dmg_lg": fields.String,
    "encumbrance": fields.Float,
    "cost": fields.Float,
    "magic": fields.Boolean,
    "description": fields.String,
    # missile weapons
    "rate_of_fire": fields.Float,
    "rng": fields.Integer,
})

weapon = api.clone("Weapon", weapon_input, {
    "id": MongoId
})


weapon_inventory = api.model("WeaponInventory", {
    "info": fields.Nested(weapon),
    "count": fields.Integer
})

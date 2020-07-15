from flask_restx import fields
from .routes import dnd_api as api


class MongoId(fields.Raw):
    def __init__(self, *args, **kwargs):
        self.desc = "Mongodb ObjectId ($oid)"
        super().__init__(description=self.desc, *args, **kwargs)

    def format(self, value):
        return str(value)


restrictions = api.model("Restrictions", {
    # "id": MongoId,
    "min_str": fields.Integer,
    "min_dex": fields.Integer,
    "min_con": fields.Integer,
    "min_int": fields.Integer,
    "min_wis": fields.Integer,
    "min_cha": fields.Integer,
    "hit_die": fields.String,
    "alignment": fields.List(fields.String),
    "armor": fields.List(fields.String),
    "shield": fields.List(fields.String),
    "weapons_permitted": fields.List(fields.String),
    "proficiencies": fields.String,
    "penalty_to_hit": fields.Integer,
})

ability = api.model("Ability", {
    # "id": MongoId,
    "name": fields.String,
    "level": fields.Integer,
    "description": fields.String
})

lvl_adv = api.model("LevelAdvancement", {
    # "id": MongoId,
    "level": fields.Integer,
    "exp_req": fields.Integer,
    "num_hit_dice": fields.Integer,
    "notes": fields.String
})

thief_chance = api.model("ThiefChance", {
    # "id": MongoId,
    "level": fields.Integer,
    "climb_walls": fields.Float,
    "find_traps": fields.Float,
    "hear_noise": fields.Float,
    "hide_in_shadows": fields.Float,
    "move_quietly": fields.Float,
    "open_locks": fields.Float,
    "pick_pockets": fields.Float,
    "read_languages": fields.Float,
})

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
}, mask={"id", "classname"})

spell = api.clone("Spell", spell_input, {
    "id": MongoId
})

clss = api.model("Class", {
    "id": MongoId,
    "classname": fields.String,
    "restrictions": fields.Nested(restrictions),
    "abilities": fields.List(fields.Nested(ability)),
    "saving_throws": fields.Raw,
    "to_hit": fields.Raw,
    "level_advancement": fields.List(fields.Nested(lvl_adv)),
    "skill_chance": fields.List(fields.Nested(thief_chance)),
    "spells": fields.List(fields.Nested(spell))
})

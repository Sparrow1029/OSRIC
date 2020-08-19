from .spells import spell

from .fields import MongoId

restrictions = api.model("Restrictions", {
    "min_str": fields.Integer, "min_dex": fields.Integer,
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
    "name": fields.String,
    "level": fields.Integer,
    "description": fields.String
})

lvl_adv = api.model("LevelAdvancement", {
    "level": fields.Integer,
    "exp_req": fields.Integer,
    "num_hit_dice": fields.Integer,
    "notes": fields.String
})

thief_chance = api.model("ThiefChance", {
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

race_input = api.model("RaceInput", {
    "name": fields.String,
    "base_stat_mods": fields.Raw,
    "abilities": fields.Nested(ability),
    "bonuses": fields.List(fields.String),
    "languages": fields.List(fields.String),
    "max_addl_languages": fields.Integer,
    "permitted_classes": fields.List(fields.String),
    "starting_age": fields.Raw,
    "score_limits": fields.Raw,
    "movement_rate": fields.Integer
})

race = api.clone("Race", race_input, {
    "id": MongoId
})

class_input = api.model("ClassInput", {
    "name": fields.String,
    "restrictions": fields.Nested(restrictions),
    "abilities": fields.List(fields.Nested(ability)),
    "saving_throws": fields.Raw,
    "to_hit": fields.Raw,
    "level_advancement": fields.List(fields.Nested(lvl_adv)),
    "skill_chance": fields.List(fields.Nested(thief_chance)),
    "spells": fields.List(fields.Nested(spell))
})

class_ = api.clone("Class", class_input, {
    "id": MongoId,
})

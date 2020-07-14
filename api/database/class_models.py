from .db import db
from .object_models import Ability, Spell


class ClassRestrictions(db.EmbeddedDocument):
    min_str = db.IntField()
    min_dex = db.IntField()
    min_con = db.IntField()
    min_int = db.IntField()
    min_wis = db.IntField()
    min_cha = db.IntField()
    hit_die = db.StringField()
    alignment = db.StringField()
    armor = db.ListField()
    shield = db.StringField()
    weapons_permitted = db.ListField()
    proficiencies = db.StringField()
    penalty_to_hit = db.IntField()


class LevelAdvancement(db.EmbeddedDocument):
    level = db.IntField()
    exp_req = db.IntField()
    num_hit_dice = db.IntField()
    notes = db.StringField(null=True)


class ThiefChance(db.EmbeddedDocument):
    level = db.IntField()
    climb_walls = db.FloatField()
    find_traps = db.FloatField()
    hear_noise = db.FloatField()
    hide_in_shadows = db.FloatField()
    move_quietly = db.FloatField()
    open_locks = db.FloatField()
    pick_pockets = db.FloatField()
    read_languages = db.FloatField()


class Race(db.Document):
    meta = {"collection": "races"}
    name = db.StringField(required=True)
    mods = db.DictField()
    abilities = db.EmbeddedDocumentListField(Ability)
    permitted_classes = db.ListField(db.StringField())
    class_adj = db.DictField()


class Class(db.Document):
    meta = {"collection": "classes"}
    classname = db.StringField()
    restrictions = db.EmbeddedDocumentField(ClassRestrictions)
    abilities = db.EmbeddedDocumentListField(Ability)
    saving_throws = db.DictField()
    to_hit = db.DictField()
    level_advancement = db.EmbeddedDocumentListField(LevelAdvancement)
    skill_chance = db.EmbeddedDocumentListField(ThiefChance, null=True)
    spells = db.ListField(db.ReferenceField(Spell, reverse_delete_rule=db.PULL))

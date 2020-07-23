from ..db import db
from .object_models import Ability, Spell
from .character_models import ThiefChance


class ClassRestrictions(db.EmbeddedDocument):
    min_str = db.IntField()
    min_dex = db.IntField()
    min_con = db.IntField()
    min_int = db.IntField()
    min_wis = db.IntField()
    min_cha = db.IntField()
    hit_die = db.StringField()
    alignment = db.ListField()
    armor = db.ListField()
    shield = db.ListField()
    weapons_permitted = db.ListField()
    proficiencies = db.StringField()
    penalty_to_hit = db.IntField()


class SpellsByLevel(db.EmbeddedDocument):
    spell_class = db.StringField()
    level = db.IntField()
    spells = db.DictField()


class LevelAdvancement(db.EmbeddedDocument):
    level = db.IntField()
    exp_req = db.IntField()
    num_hit_dice = db.IntField()
    notes = db.StringField()


class Race(db.Document):
    meta = {"collection": "races"}
    name = db.StringField(unique=True, required=True)
    base_stat_mods = db.DictField()
    abilities = db.EmbeddedDocumentListField(Ability)
    bonuses = db.ListField(db.StringField())
    languages = db.ListField(db.StringField())
    max_addl_languages = db.IntField(default=0)
    permitted_classes = db.ListField(db.StringField())
    starting_age = db.DictField()
    score_limits = db.DictField()
    movement_rate = db.IntField()
    thief_skill_adj = db.EmbeddedDocumentField(ThiefChance)


class Class(db.Document):
    meta = {"collection": "classes"}
    name = db.StringField()
    restrictions = db.EmbeddedDocumentField(ClassRestrictions)
    abilities = db.EmbeddedDocumentListField(Ability)
    saving_throws = db.DictField()
    to_hit = db.DictField()
    level_advancement = db.EmbeddedDocumentListField(LevelAdvancement)
    spells = db.ListField(db.ReferenceField(Spell, reverse_delete_rule=db.PULL))
    spells_by_level = db.EmbeddedDocumentListField(SpellsByLevel)
    thief_skill_chance = db.EmbeddedDocumentListField(ThiefChance, null=True)
    thief_dex_adj = db.EmbeddedDocumentListField(ThiefChance, null=True)

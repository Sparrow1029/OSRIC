from datetime import datetime
from ..db import db
from .object_models import Item, Weapon, Armor, Spell, Ability
from .class_models import Class, Race


class Stats(db.EmbeddedDocument):
    str = db.IntField(required=True)
    con = db.IntField(required=True)
    dex = db.IntField(required=True)
    int = db.IntField(required=True)
    wis = db.IntField(required=True)
    cha = db.IntField(required=True)


class Inventory(db.EmbeddedDocument):
    gold = db.FloatField()
    loot = db.ListField(db.GenericReferenceField)
    armor = db.ListField(db.ReferenceField(Armor))
    weapons = db.ListField(db.ReferenceField(Weapon))
    items = db.ListField(db.ReferenceField(Item))


class Equipment(db.EmbeddedDocument):
    equipped_weapons = db.ListField(db.GenericReferenceField)


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


class MemorizedSpells(db.EmbeddedDocument):
    spells = db.ListField(db.ReferenceField(Spell))
    num_remaining = db.IntField()


class Character(db.Document):
    name = db.StringField(required=True)
    level = db.IntField(default=1)
    stats = db.EmbeddedDocumentField(Stats)
    class_ = db.ReferenceField(Class, db_field="class")  # `class` is a reserved keyword
    race = db.ReferenceField(Race)
    abilities = db.ListField(Ability)

    created_at = db.DateTimeField(default=datetime.utcnow)
    public = db.BooleanField(default=True)
    owner = db.ReferenceField('Player')

    cur_hp = db.IntField()
    max_hp = db.IntField()
    alive = db.BooleanField()
    status_effects = db.ListField(db.DictField())
    inventory = db.EmbeddedDocumentField(Inventory)

    def determine_thief_chance():
        # skill_chance = db.EmbeddedDocumentListField(ThiefChance)
        pass

    def _set_init_abilities(self):
        race_abls = Race.objects.get(id=self.race.id).abilities
        clss_abls = Class.objects.get(id=self.class_.id).abilities
        self.abilities = race_abls + clss_abls

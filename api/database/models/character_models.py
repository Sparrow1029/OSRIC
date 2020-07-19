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


class InventoryItem(db.EmbeddedDocument):
    ref = db.LazyReferenceField(Item)
    amount = db.IntField()


class InventoryWeapon(db.EmbeddedDocument):
    ref = db.LazyReferenceField(Weapon)
    amount = db.IntField()


class InventoryArmor(db.EmbeddedDocument):
    ref = db.LazyReferenceField(Armor)
    amount = db.IntField()


class Inventory(db.EmbeddedDocument):
    gold = db.FloatField()
    armor = db.ListField(InventoryArmor)
    weapons = db.ListField(InventoryWeapon)
    items = db.ListField(InventoryItem)


class Equipment(db.EmbeddedDocument):
    armor = db.EmbeddedDocumentListField(InventoryArmor)
    items = db.EmbeddedDocumentListField(InventoryItem)
    weapons = db.EmbeddedDocumentListField(InventoryWeapon)


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
    spell = db.LazyReferenceField(Spell)
    num_remaining = db.IntField()


class Character(db.Document):
    name = db.StringField(required=True)
    level = db.IntField(default=1, required=True)
    base_stats = db.EmbeddedDocumentField(Stats, required=True)
    cur_stats = db.EmbeddedDocumentField(Stats)
    class_ = db.ReferenceField(Class, db_field="class")  # `class` is a reserved keyword
    race = db.ReferenceField(Race)
    abilities = db.ListField(Ability)
    gender = db.StringField(choices=["male", "female"])

    cur_hp = db.IntField()
    max_hp = db.IntField()
    alive = db.BooleanField()
    status_effects = db.ListField(db.DictField())
    inventory = db.EmbeddedDocumentField(Inventory)
    equipped = db.EmbeddedDocumentField(Equipment)
    cur_spells = db.EmbeddedDocumentListField(MemorizedSpells)
    skill_chance = db.EmbeddedDocumentField(ThiefChance)

    created_at = db.DateTimeField(default=datetime.utcnow)
    public = db.BooleanField(default=True)
    owner = db.ReferenceField('Player')

    def determine_thief_chance():
        # skill_chance = db.EmbeddedDocumentListField(ThiefChance)
        pass

    def set_init_abilities(self):
        race_abls = Race.objects.get(id=self.race.id).abilities
        clss_abls = Class.objects.get(id=self.class_.id).abilities
        self.abilities = race_abls + clss_abls

    def __repr__(self):
        string = ""
        for field in self._fields:
            string += f"{field}: {getattr(self, field)}"
        return string


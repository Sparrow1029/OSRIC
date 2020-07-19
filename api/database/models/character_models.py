from datetime import datetime
from ..db import db
from .object_models import Item, Weapon, Armor, Spell, Ability
from .class_models import Class, Race
from bson import ObjectId


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
    meta = {"collection": "characters"}
    name = db.StringField(required=True)
    level = db.IntField(default=1, required=True)
    base_stats = db.EmbeddedDocumentField(Stats, required=True)
    cur_stats = db.EmbeddedDocumentField(Stats)
    class_ = db.ReferenceField(Class, db_field="class")  # `class` is a reserved keyword
    race = db.ReferenceField(Race)
    abilities = db.EmbeddedDocumentListField(Ability)
    gender = db.StringField(choices=["male", "female"])

    cur_hp = db.IntField()
    max_hp = db.IntField()
    exp = db.IntField(default=0)
    alive = db.BooleanField(default=True)
    status_effects = db.DictField()
    inventory = db.EmbeddedDocumentField(Inventory)
    equipped = db.EmbeddedDocumentField(Equipment)
    cur_spells = db.EmbeddedDocumentListField(MemorizedSpells)
    skill_chance = db.EmbeddedDocumentField(ThiefChance)

    created_at = db.DateTimeField(default=datetime.utcnow)
    public = db.BooleanField(default=True)
    owner = db.ReferenceField('Player')

    def thief_chance(self):
        Thief = Class.objects.get(classname="thief")
        self.skill_chance = Thief.skills["1"]
        race_adj = Thief.race_adj[self.race]
        for key in self.skill_chance:
            self.skill_chance[key] += race_adj[key]

    def link_player(self, player_id):
        from .player_models import Player
        self.owner = Player.objects.with_id(player_id)

    def set_init_abilities(self):
        race_abls = Race.objects.get(id=self.race.id).abilities
        clss_abls = Class.objects.get(id=self.class_.id).abilities
        print(race_abls, clss_abls)
        # self.abilities = [ability for ability in race_abls.extend(clss_abls)]
        self.abilities = race_abls + clss_abls

    def clean(self):
        self.cur_stats = self.base_stats
        self.set_init_abilities()
        # self.class_ = Class.objects.get(classname=self.class_).id
        # self.race = Race.objects.get(race=self.race).id

    def __repr__(self):
        string = ""
        for field in self._fields:
            string += f"{field}: {getattr(self, field)}"
        return string


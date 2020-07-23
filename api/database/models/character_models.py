from ..db import db
from .object_models import Item, Weapon, Armor, Spell
# from bson import ObjectId


class Stats(db.EmbeddedDocument):
    str = db.IntField(min_value=3, max_value=19)
    con = db.IntField(min_value=3, max_value=19)
    dex = db.IntField(min_value=3, max_value=19)
    int = db.IntField(min_value=3, max_value=19)
    wis = db.IntField(min_value=3, max_value=19)
    cha = db.IntField(min_value=3, max_value=19)


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
    gold = db.FloatField(default=100.0)
    armor = db.ListField(InventoryArmor, default=[])
    weapons = db.ListField(InventoryWeapon, default=[])
    items = db.ListField(InventoryItem, default=[])


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


class MemSpell(db.EmbeddedDocument):
    spell = db.LazyReferenceField(Spell)
    num_remaining = db.IntField()

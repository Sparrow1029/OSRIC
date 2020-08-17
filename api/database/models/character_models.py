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

    def __repr__(self):
        for stat in self._fields:
            print(f"{stat.upper()}: {getattr(self, stat)}")


class StrMods(db.EmbeddedDocument):
    hit_bonus = db.IntField()
    dmg_bonus = db.IntField()
    encumb_adj = db.IntField()
    minor_tests = db.StringField()
    major_tests = db.StringField()


class DexMods(db.EmbeddedDocument):
    surprise = db.IntField()
    to_hit = db.IntField()
    ac = db.IntField()


class ConMods(db.EmbeddedDocument):
    hit_per_die = db.IntField()
    survive_dead = db.IntField()
    survive_sys_shock = db.IntField()


class ChaMods(db.EmbeddedDocument):
    max_henchmen = db.IntField()
    loyalty_bonus = db.IntField()
    reaction_bonus = db.IntField()


class BaseMods(db.EmbeddedDocument):
    str_mods = db.EmbeddedDocumentField(StrMods)
    dex_mods = db.EmbeddedDocumentField(DexMods)
    con_mods = db.EmbeddedDocumentField(ConMods)
    cha_mods = db.EmbeddedDocumentField(ChaMods)


class InventoryItem(db.EmbeddedDocument):
    info = db.ReferenceField(Item)
    count = db.FloatField()


class InventoryWeapon(db.EmbeddedDocument):
    info = db.ReferenceField(Weapon)
    count = db.IntField()


class InventoryArmor(db.EmbeddedDocument):
    info = db.ReferenceField(Armor)
    count = db.IntField()


class Inventory(db.EmbeddedDocument):
    gold = db.FloatField(default=100.0)
    armor = db.EmbeddedDocumentListField(InventoryArmor, default=[])
    weapons = db.EmbeddedDocumentListField(InventoryWeapon, default=[])
    items = db.EmbeddedDocumentListField(InventoryItem, default=[])


class EquippedWeapons(db.EmbeddedDocument):
    main = db.ReferenceField(Weapon)
    secondary = db.ReferenceField(Weapon)
    missile = db.ReferenceField(Weapon)
    other1 = db.ReferenceField(Weapon)
    other2 = db.ReferenceField(Weapon)


class EquippedArmor(db.EmbeddedDocument):
    armor = db.ReferenceField(Armor)
    shield = db.ReferenceField(Armor)
    hands = db.ListField(db.ReferenceField(Armor))
    other = db.ListField(db.ReferenceField(Armor))


class EquippedItems(db.EmbeddedDocument):
    feet = db.ReferenceField(Item)
    clothes = db.ListField(db.ReferenceField(Item))
    cape = db.ReferenceField(Item)
    other = db.ListField(db.ReferenceField(Item))


class Equipment(db.EmbeddedDocument):
    weapons = db.EmbeddedDocumentField(EquippedWeapons)
    armor = db.EmbeddedDocumentField(EquippedArmor)
    items = db.EmbeddedDocumentField(EquippedItems)


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

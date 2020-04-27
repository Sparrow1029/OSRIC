from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ReferenceField,
    ObjectIdField,
    StringField,
    FloatField,
    EmailField, ListField,
    IntField,
)
from flask_bcrypt import generate_password_hash, check_password_hash


class Stats(EmbeddedDocument):

    str = IntField(required=True)
    dex = IntField(required=True)
    con = IntField(required=True)
    int = IntField(required=True)
    wis = IntField(required=True)
    cha = IntField(required=True)

    def apply_base_stat_race_mods(self, racename: str):
        if racename == 'dwarf':
            self.con += 1
            self.cha -= 1
        elif racename == 'elf':
            self.dex += 1
            self.con -= 1
        elif racename == 'halfling':
            self.str -= 1
            self.dex += 1
        elif racename == 'half-orc':
            self.str += 1
            self.con += 1
            self.cha -= 2


class ClassMods(EmbeddedDocument):

    min_str = IntField()
    min_dex = IntField()
    min_con = IntField()
    min_int = IntField()
    min_wis = IntField()
    min_cha = IntField()
    hit_die = StringField()
    alignment = StringField()
    armor_type = ListField()
    shield_type = StringField()
    weapons = ListField()
    proficiencies = StringField()
    penalty_to_hit = IntField()


class Ability(EmbeddedDocument):

    meta = {"collection": "ability"}
    name = StringField(max_length=32, required=True)
    description = StringField()


class Modifiers(EmbeddedDocument):

    meta = {"collection": "modifiers"}
    type = StringField(db_field="type", required=True)
    value = IntField(required=True)


class Race(Document):

    name = StringField(required=True)
    mods = EmbeddedDocumentListField(Modifiers)
    abilities = EmbeddedDocumentListField(Ability)
    permitted_classes = ListField(StringField())


class Class(Document):

    meta = {"collection": "classes"}
    name = StringField(required=True)
    mods = EmbeddedDocumentField(ClassMods)
    abilities = EmbeddedDocumentListField(Ability)


class Item(Document):

    meta = {"collection": "items"}
    name = StringField(required=True)
    weight = FloatField()
    cost = FloatField()
    special = StringField()


class Weapon(Document):

    meta = {"collection": "weapons"}
    name = StringField(required=True)
    type = StringField(required=True)  # missile or melee or magic?
    dmg_sm_md = StringField()
    dmg_lg = StringField()
    encumbrance = FloatField()
    cost = FloatField()
    magic = StringField()

    # missile weapons only
    rate_of_fire = FloatField()
    rng = IntField()


class Armor(Document):

    type = StringField()
    encumbrance = IntField()
    max_move = IntField()
    ac = IntField()
    cost = FloatField()


class Inventory(EmbeddedDocument):

    gold = FloatField()
    loot = ListField(Item)
    armor =ListField(Armor)
    weapons = ListField(Weapon)
    equipment = ListField(Item)


class Character(Document):

    meta = {"collection": "character"}
    name = StringField(max_length=32, required=True)
    stats = EmbeddedDocumentField(Stats, required=True)
    clss = ReferenceField(Class)
    race = ReferenceField(Race)
    cur_campaign = StringField()
    align = StringField(required=True)
    inventory = EmbeddedDocumentField(Inventory)


class Player(Document):

    meta = {
        "collection": "player",
        "indexes": ["username"],
           }
    # _id = ObjectIdField(unique=True)
    # username = StringField(required=True, unique=True)
    # password = StringField(required=True, min_length=8)
    # email = EmailField(unique=True)
    username = StringField(required=True)
    password = StringField(required=True, min_length=8)
    email = EmailField()
    characters = ListField(ReferenceField(Character))
    real_name = StringField()

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


class Campaign(Document):

    meta = {"collection": "campaigns"}
    owner = ReferenceField(Player, required=True)
    title = StringField(required=True)
    characters = ListField(ReferenceField(Character))


class Spell(Document):

    meta = {"collection": "spells"}
    clss = ReferenceField(Class)
    spell_name = StringField(required=True, unique=True)
    lvl = IntField()
    rng = StringField()
    duration = StringField()
    aoe = StringField()
    components = ListField()
    saving_throw = StringField(default='None')
    description = StringField()

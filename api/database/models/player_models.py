from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from .character_models import Stats, Inventory, Equipment, ThiefChance, MemSpell, BaseMods
from .object_models import Spell, Ability
from .class_models import Class, Race

from ..db import db


class Character(db.Document):
    meta = {"collection": "characters"}
    name = db.StringField(required=True)
    level = db.IntField(default=1, required=True)
    base_stats = db.EmbeddedDocumentField(Stats, required=True)
    cur_stats = db.EmbeddedDocumentField(Stats)
    base_mods = db.EmbeddedDocumentField(BaseMods)
    classref = db.ReferenceField(Class)
    raceref = db.ReferenceField(Race)
    abilities = db.EmbeddedDocumentListField(Ability)
    gender = db.StringField(choices=["male", "female"])

    cur_hp = db.IntField()
    max_hp = db.IntField()
    exp = db.IntField(default=0)
    ac = db.IntField()
    alive = db.BooleanField(default=True)
    status_effects = db.ListField(db.StringField)
    inventory = db.EmbeddedDocumentField(Inventory, null=False, default=Inventory())
    equipped = db.EmbeddedDocumentField(Equipment)
    available_spells = db.ListField(db.ReferenceField(Spell))
    cur_spells = db.EmbeddedDocumentListField(MemSpell)
    thief_tbl = db.EmbeddedDocumentListField(ThiefChance, null=True)
    cur_thief_skills = db.DictField(null=True)

    created_at = db.DateTimeField(default=datetime.utcnow)
    public = db.BooleanField(default=True)
    owner = db.ReferenceField('Player', unique_with="name")

    def __repr__(self):
        string = ""
        for field in self._fields:
            string += f"{field}: {getattr(self, field)}\n"
        return string


class Player(db.Document):
    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True)
    real_name = db.StringField(default="Anonymous", null=False)
    password = db.StringField(required=True)
    characters = db.ListField(db.ReferenceField('Character', reverse_delete_rule=db.PULL))
    created_at = db.DateTimeField(default=datetime.utcnow)
    admin = db.BooleanField(required=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf-8")

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def clean(self):
        if not self.real_name:
            self.real_name = "Anonymous"
        # self.admin = False

    def add_character(self, id):
        char = Character.objects.with_id(id)
        self.characters.append(char)
        self.save()


Player.register_delete_rule(Character, 'owner', db.CASCADE)

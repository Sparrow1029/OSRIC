from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from .db import db
from .character_models import Character


class Player(db.Document):
    username = db.StringField(required=True, unique=True)
    real_name = db.StringField(null=True)
    password = db.StringField(required=True)
    character = db.EmbeddedDocumentListField(Character)
    created_at = db.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


class Note(db.EmbeddedDocument):
    date = db.DateTimeField(default=datetime.utcnow)
    content = db.StringField(required=True)


class Session(db.EmbeddedDocument):
    date = db.DateTimeField(default=datetime.utcnow)


class Campaign(db.EmbeddedDocument):
    title = db.StringField(required=True)
    dungeon_master = db.ObjectIdField()
    players = db.ListField(db.ObjectIdField)
    notes = db.EmbeddedDocumentListField(Note)

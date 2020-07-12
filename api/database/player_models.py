from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from .db import db
from .character_models import Character


class Player(db.Document):
    meta = {
        "indexes": [
            {"fields": ("username", "email"), "unique": True}
        ]
    }
    username = db.StringField(required=True)  #, unique=True)
    email = db.EmailField()  #unique_with="username")
    real_name = db.StringField(null=True)
    password = db.StringField(required=True)
    character = db.EmbeddedDocumentListField(Character)
    created_at = db.DateTimeField(default=datetime.utcnow)

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

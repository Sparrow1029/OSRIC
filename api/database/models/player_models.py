from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from ..db import db
from .character_models import Character


class Player(db.Document):
    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True)
    real_name = db.StringField(default="Anonymous", null=False)
    password = db.StringField(required=True)
    characters = db.ListField(Character, reverse_delete_rule=db.PULL)
    created_at = db.DateTimeField(default=datetime.utcnow)
    admin = db.BooleanField(required=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf-8")

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

    def clean(self):
        if not self.real_name:
            self.real_name = "Anonymous"
        self.admin = False


Player.register_delete_rule(Character, 'owner', db.CASCADE)
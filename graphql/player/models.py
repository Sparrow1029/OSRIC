from mongoengine import Document
from mongoengine.fields import ReferenceField, StringField, ListField
from ..character.models import Character
from flask_bcrypt import generate_password_hash, check_password_hash


class Player(Document):

    meta = {"collection": "player"}
    username = StringField(required=True, unique=True)
    password = StringField(required=True, min_length=8)
    characters = ListField(ReferenceField(Character))
    real_name = StringField()

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)

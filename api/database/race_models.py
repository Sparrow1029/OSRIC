from .db import db
from .object_models import Ability


class Race(db.Document):
    meta = {"collection": "races"}
    name = db.StringField(required=True)
    mods = db.DictField()
    abilities = db.EmbeddedDocumentListField(Ability)
    permitted_classes = db.ListField(db.StringField())

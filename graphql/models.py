from mongoengine.fields import (
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ReferenceField,
    # ObjectIdField,
    StringField,
    FloatField,
    EmailField,
    ListField,
    IntField,
)


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

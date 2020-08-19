import mongoengine_marshmallow as ma

from ...database.models import Spell, Class, Race, Character


class ClassSchema(ma.ModelSchema):
    class Meta:
        model = Class


class RaceSchema(ma.ModelSchema):
    class Meta:
        model = Race


class SpellSchema(ma.ModelSchema):
    class Meta:
        model = Spell


class CharacterSchema(ma.ModelSchema):
    class Meta:
        model = Character

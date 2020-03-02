# from flask import current_app
# db = current_app.db
from . import db, ma


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(64), index=True)
    char_name = db.Column(db.String(64))
    race = db.Column(db.String)
    class_ = db.Column(db.String)
    exp = db.Column(db.Integer)
    lvl = db.Column(db.Integer)
    str = db.Column(db.Integer)
    dex = db.Column(db.Integer)
    con = db.Column(db.Integer)
    int = db.Column(db.Integer)
    wis = db.Column(db.Integer)
    cha = db.Column(db.Integer)

    def __repr__(self):
        string = f"Player: {self.player_name}\t\tCharacter: {self.char_name}\nStr: {self.strength}"
        return string


class CharacterClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(64), index=True)
    abilities = db.Column(db.Text)
    max_wp = db.Column(db.Integer)
    hit_die = db.Column(db.String(4))
    max_hit_die = db.Column(db.Integer)
    weapon_spec = db.Column(db.Text)
    permitted_weapons = db.Column(db.Text)

    def __repr__(self):
        string = \
            f"Abilites:\n{self.abilities}\nHit Die Type:{self.hit_die} (max {self.max_hit_die})"
        return string


class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player


class CharacterClassSchema(ma.ModelSchema):
    class Meta:
        model = CharacterClass

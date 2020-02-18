# from flask import current_app
# db = current_app.db
from . import db, ma

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(64), index=True)
    char_name = db.Column(db.String(64))
    strength = db.Column(db.Integer)

    def __repr__(self):
        string = \
        f"Player: {self.player_name}\t\tCharacter: {self.char_name}\n"
        "Str: {self.strength}"
        return string


class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player

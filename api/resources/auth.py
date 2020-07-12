from flask import request
from flask_restx import Resource

from database.player_models import Player


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        player = Player(**body)
        player.hash_password()
        player.save()
        id = player.id
        return {"id": str(id)}, 200

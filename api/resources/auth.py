from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_restx import Resource
import datetime

from database.player_models import Player


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        player = Player(**body)
        player.hash_password()
        player.save()
        id = player.id
        return {"id": str(id)}, 200


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        player = Player.objects.get(username=body.get("username"))
        if not list(player):
            player = Player.objects.get(email=body.get("username"))
        authorized = player.check_password_hash(body.get("password"))
        if not authorized:
            return {"error": "Invalid username/email password combination"}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(player.id), expires_delta=expires)
        return {"token": access_token}, 200

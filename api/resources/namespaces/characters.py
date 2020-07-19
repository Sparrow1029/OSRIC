from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity

from ...core.auth import admin_required
from ...database.models import Character, Player
from bson import ObjectId
from ..routes import dnd_api as api
from ..api_models import spell, character, character_input

ns = api.namespace("characters", description="DnD Database - Characters")


@ns.route("/public")
class CharactersApi(Resource):
    @jwt_required
    @api.doc(responses={500: "Something went wrong", 200: "Success"})
    @api.param("player_id", description="Player MongoId")
    @api.marshal_list_with(character, skip_none=True)
    def get():
        return list(Character.objects.filter(public=True))


@ns.route("/player/<string:player_id>")
class PlayerCharactersApi(Resource):
    pass


@ns.route("/create")
class CreateCharacter(Resource):
    @jwt_required
    def post(self):
        player_id = get_jwt_identity()
        new_char = Character(**api.payload)
        print()

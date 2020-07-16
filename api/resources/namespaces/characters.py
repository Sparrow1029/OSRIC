from flask_restx import Resource, abort

from ...core.auth import admin_required
from ...database.models import Character, Player
from bson import ObjectId
from ..routes import dnd_api as api
from ..api_models import spell, character, character_input

ns = api.namespace("characters", description="DnD Database - Characters")


@ns.route("/")
class CharactersApi(Resource):
    @api_marshal_list_with(character, skip_none=True)
    def get():
        return list(Character.objects.filter(public=True))

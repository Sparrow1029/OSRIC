from flask import request, Response
from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity

from ...core.auth import admin_required
from ...database.models import Character, Player, Race, Class, Inventory
from bson import ObjectId
from ..routes import dnd_api as api
from ..api_models import character_input, character

ns = api.namespace("characters", description="DnD Database - Characters")


@ns.route("/public")
class CharactersApi(Resource):
    @jwt_required
    @api.doc(responses={500: "Something went wrong", 200: "Success"})
    @api.param("player_id", description="Player MongoId")
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    @api.marshal_list_with(character, skip_none=True)
    def get(self):
        player_id = request.args.get("player_id")
        if player_id:
            return list(char for char in Character.objects.filter(public=True, owner=ObjectId(player_id)))
        return list(char for char in Character.objects.filter(public=True))


@ns.route("/player/<string:player_id>")
class PlayerCharactersApi(Resource):
    pass


@ns.route("/create")
class CreateCharacter(Resource):
    @jwt_required
    @api.expect(character_input)
    @api.doc(responses={200: "Success", 500: "Oh Noes", 404: "Player not found"})
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    def post(self):
        player_id = get_jwt_identity()
        # player_id = "5f15ec2e1b61d55ba4bbef8f"
        player = Player.objects.with_id(player_id)
        if not player:
            return 404, "Player not found"
        payload = api.payload
        # from pprint import pprint
        # pprint(payload)
        char_class = Class.objects.get(name=payload["class"])
        char_race = Race.objects.get(name=payload["race"])
        del payload["class"]
        del payload["race"]
        payload["classref"] = char_class.id
        payload["raceref"] = char_race.id

        # apply race modifiers to stats
        for stat in char_race.base_stat_mods:
            payload["base_stats"][stat] += char_race.base_stat_mods[stat]

        # create `Character` object and apply other modifications
        new_char = Character(**payload)
        print(new_char._fields)
        new_char.save()  # Save object first before it can be referenced on `Player` object
        if new_char.classref.name in ["druid", "cleric", "magic_user", "illusionist"]:
            new_char.add_initial_spells(new_char.classref.name)
        new_char.set_init_abilities()
        new_char.cur_stats = new_char.base_stats
        new_char.inventory = Inventory()

        new_char.link_player(player)
        return {"id": str(new_char.id), "message": "Successfully Created Character"}


@ns.route("/delete")
class DeleteCharacter(Resource):
    @jwt_required
    @api.param("character_id", description="MongoDb ObjectId of character")
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    @api.doc(responses={
        400: "Bad Query",
        401: "Bad Owner",
        404: "Character Does Not Exist",
        204: "Character Deleted"
    })
    def delete(self):
        player_id = get_jwt_identity()
        # player_id = "5f15ec2e1b61d55ba4bbef8f"
        char_id = request.args.get("character_id")
        if not char_id:
            abort(400, "Bad Query")
        char_obj = Character.objects.with_id(char_id)
        if not char_obj:
            abort(404, "Character Does Not Exist")
        if not str(char_obj.owner.id) == player_id:
            abort(401, "Bad Owner")
        char_obj.delete()
        return Response("Character Deleted", 204)

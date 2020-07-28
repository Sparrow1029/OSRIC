from flask import request, Response
from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity  # , get_jwt_claims

# import json
# from ...core.auth import admin_required
from ...database.char_mgmt import update_character
from ...database.models import Character, Player, Race, Class, Inventory
from ...database.char_create import create_character
from bson import ObjectId
from ..routes import dnd_api as api
from ..api_models import character_input, character

ns = api.namespace("character", description="DnD Database - Characters")


@ns.route("/")
class CharactersApi(Resource):
    @jwt_required
    @api.doc(responses={500: "Something went wrong", 200: "Success"})
    @api.param("char_id", description="Character MongoId")
    @api.param("player_id", description="Player MongoId")
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    @api.marshal_list_with(character, skip_none=True)
    def get(self):
        player_id = request.args.get("player_id")
        if player_id:
            if get_jwt_identity() == player_id:
                return Player.objects.with_id(player_id).characters
            return list(char for char in Character.objects.filter(public=True, owner=ObjectId(player_id)))
        char_id = request.args.get("char_id")
        if char_id:
            char_obj = Character.objects.with_id(char_id)
            if not char_obj.public:
                if get_jwt_identity() != player_id:
                    return Response("Unauthorized Player", 403)
                return char_obj
            return char_obj

        return list(char for char in Character.objects.filter(public=True))


@ns.route("/update")
class UpdateCharacter(Resource):
    @jwt_required
    @api.param("char_id", description="Character MongoId", required=True)
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    @api.expect(character)
    def patch(self):
        char_id = request.args.get("char_id")
        if not char_id:
            return Response("Character ID is required", 400)

        character = Character.objects.get(id=char_id)
        if not character:
            abort(404, "Character Does Not Exist")

        if not get_jwt_identity() == str(character.owner.id):
            return Response("Unauthorized User", 403)

        try:
            # update = Character.objects.get(id=char_id).modify(__raw__={"$set": dict(**api.payload)}, full_response=True)
            update = update_character(character, api.payload)
            print(update)
            return update
            if update:
                return Response("Updated Successfully", 200)
        except Exception as e:
            return Response(f"{e}", 500)


@ns.route("/create")
class CreateCharacter(Resource):
    @jwt_required
    @api.expect(character_input)
    @api.doc(responses={200: "Success", 500: "Oh Noes", 404: "Player not found"})
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    def post(self):
        player_id = get_jwt_identity()
        player = Player.objects.with_id(player_id)
        if not player:
            return 404, "Player not found"
        new_char = create_character(api.payload, player)
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

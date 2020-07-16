from flask import Response, request
from flask_restx import Resource, abort
from flask_jwt_extended import jwt_required

from ..database.models import Spell, Class
# from ..database.class_models import Class
from bson import ObjectId
# from mongoengine.queryset.visitor import Q
from .routes import dnd_api as api
from .api_models import spell, spell_input

ns = api.namespace("spells", description="Database - Spells operations")


@ns.route("/")
class SpellsApi(Resource):
    @api.doc("list_spells")
    @api.marshal_list_with(spell)
    def get(self):
        return list(Spell.objects())
        abort(500, "FUCK")


@ns.route("/<string:id>")
@ns.param("id", description="Mongodb ObjectId", _in="query")
class SpellApi(Resource):
    @api.marshal_with(spell, skip_none=True)
    def get(self, id):
        if ObjectId.is_valid(id):
            spell_obj = Spell.objects.get(id=id)
            if spell_obj:
                return spell_obj
        abort(400, error="Invalid ObjectId")

    @jwt_required
    # @admin_reqiured  # <-- TODO: make wrapper that checks jwt_claims for `admin` status
    @api.response(204, "Spell deleted")
    @api.param("Authorization", description="Bearer Token", _in="header")
    def delete(self, id):
        print(request)
        print(id)
        if ObjectId.is_valid(id):
            spell_obj = Spell.objects.get(id=id)
            spell_obj.delete()
            return "success", 201
        else:
            abort(400, error="Invalid ObjectId")

    # @jwt_required
    @api.expect(spell_input)
    @api.param("Authorization", description="Bearer Token", _in="header")
    @api.response(200, "Spell successfully updated")
    def put(self, id):
        if ObjectId.is_valid(id):
            obj = Spell.objects.get(id=id)
            obj.modify(**api.payload)
            return "", 204
        abort(400, "bad endpoint", error="Invalid ObjectId")

    @api.expect(spell_input)
    @api.marshal_list_with(spell, code=201, skip_none=True)
    @api.response(201, "Spell successfully created")
    def post(self):
        spell = Spell(**api.payload).save()
        class_to_update = Class.objects.get(classname=api.payload["classname"])
        class_to_update.modify(push__spells=spell.id)
        return {"id": str(spell.id)}, 201
        abort(500, "crap it all went sideways")

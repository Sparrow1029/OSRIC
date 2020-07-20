from flask_restx import Resource, abort

# from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from ...core.auth import admin_required
from ...database.models import Spell, Class
from bson import ObjectId
from ..routes import dnd_api as api
from ..api_models import spell, spell_input

ns = api.namespace("spells", description="Database - Spells operations")


@ns.route("/")
class SpellsApi(Resource):
    @api.doc("list_spells")
    @api.marshal_list_with(spell, skip_none=True)
    def get(self):
        return list(Spell.objects())
        abort(500, "Something went horribly wrong.")


@ns.route("/<string:id>")
@ns.param("id", description="Mongodb ObjectId", _in="query")
class SpellApi(Resource):
    @api.marshal_with(spell, skip_none=True)
    @api.doc(responses={200: "OK", 404: "Spell not found"})
    def get(self, id):
        if ObjectId.is_valid(id):
            spell_obj = Spell.objects.get(id=id)
            if spell_obj:
                return spell_obj
        abort(400, error="Invalid ObjectId")

    @admin_required
    @api.response(204, "Spell deleted")
    @api.doc(responses={403: "Not Authorized"})
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    def delete(self, id):
        if ObjectId.is_valid(id):
            spell_obj = Spell.objects.get(id=id)
            spell_obj.delete()
            return "success", 201
        else:
            abort(400, error="Invalid ObjectId")

    @admin_required
    @api.expect(spell_input)
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    @api.doc(responses={403: "Not Authorized", 200: "Spell Updated"})
    def patch(self, id):
        if ObjectId.is_valid(id):
            obj = Spell.objects.get(id=id)
            obj.modify(**api.payload)
            return {"id": obj.id, "message": "success"}, 204
        abort(400, "bad endpoint", error="Invalid ObjectId")

    @admin_required
    @api.expect(spell_input)
    @api.marshal_list_with(spell, code=201, skip_none=True)
    @api.param("Authorization", description="Bearer <JWT>", _in="header", required=True)
    @api.doc(responses={201: "Spell successfully created", 403: "Admins Only"})
    def post(self):
        spell = Spell(**api.payload).save()
        class_to_update = Class.objects.get(name=api.payload["classname"])
        class_to_update.modify(push__spells=spell.id)
        return {"id": str(spell.id)}, 201
        abort(500, "crap it all went sideways")

from flask import Response, request
from database.object_models import Spell
from database.class_models import Class
from bson import ObjectId
from mongoengine.queryset.visitor import Q

from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .routes import dnd_api as api
from .api_models import spell, spell_delete

ns = api.namespace("spells", description="Database - Spells operations")


@ns.route("/")
class SpellsApi(Resource):
    @ns.doc("list_spells")
    @ns.marshal_list_with(spell)
    def get(self):
        return list(Spell.objects())
        # return Response(spells, mimetype="application/json", status=200)

    # @jwt_required
    @ns.doc("create_spell")
    @ns.expect(spell)
    @ns.marshal_list_with(spell, code=201)
    def post(self):
        # body = request.get_json()
        # spell = Spell(**body).save()
        del api.payload["id"]
        spell = Spell(**api.payload).save()
        class_to_update = Class.objects.get(classname=api.payload["classname"])
        class_to_update.modify(push__spells=spell.id)
        return {"id": str(spell.id)}, 201
        # id = spell.id
        # return {"id": str(id)}, 200

    @ns.doc("delete_spell")
    @ns.expect(spell_delete)
    @ns.marshal_with(spell_delete, skip_none=True)
    def delete(self):
        print(api.payload)
        spell_obj = Spell.objects.get(**api.payload)
        return spell_obj, 200


@ns.route("/<query>")
class SpellApi(Resource):
    @ns.doc("get_spell_by_id_or_spellname")
    @ns.marshal_with(spell, skip_none=True)
    def get(self, query):
        if ObjectId.is_valid(query):
            spell_obj = Spell.objects.get(id=id)
        # elif "spellname" in q and "classname" in q:
        #     spell_obj = Spell.objects(Q(spellname=q.get("spellname")) & Q(classname=q.get("classname")))
        # else:
        #     spell_obj = Spell.objects(Q(spellname=q.get("spellname")) | Q(classname=q.get("classname")))
        else:
            spell_obj = Spell.objects.get(spellname=query)
        return spell_obj
        # return Response(spell, mimetype="application/json", status=200)


@ns.route("/update/<string:id>")
class SpellUpdateApi(Resource):
    # @jwt_required
    @ns.doc("update_spell")
    @ns.expect(spell)
    @ns.marshal_with(spell)
    def put(self, id):
        # body = request.get_json()
        # if "id" in kwargs:
        #     Spell.objects.get(id=kwargs["id"]).update(**body)
        # elif "name" in kwargs:
        #     Spell.objects.get(classname=kwargs["name"]).update(**body)
        # return "Spell successfully updated", 204
        if ObjectId.is_valid(id):
            obj = Spell.objects.get(id=id)
        obj.update(api.payload)
        return "", 204

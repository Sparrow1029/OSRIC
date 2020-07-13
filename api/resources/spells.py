from flask import Response, request
from database.object_models import Spell

from flask_restx import Resource
from flask_jwt_extended import jwt_required


class SpellsApi(Resource):
    def get(self):
        spells = Spell.objects().to_json()
        return Response(spells, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        body = request.get_json()
        spell = Spell(**body).save()
        id = spell.id
        return {"id": str(id)}, 200


class SpellApi(Resource):
    @jwt_required
    def put(self, **kwargs):
        body = request.get_json()
        if "id" in kwargs:
            Spell.objects.get(id=kwargs["id"]).update(**body)
        elif "name" in kwargs:
            Spell.objects.get(classname=kwargs["name"]).update(**body)
        return "Spell successfully updated", 204

    def get(self, **kwargs):
        if "id" in kwargs:
            spell = Spell.objects.get(id=kwargs["id"]).to_json()
        elif "name" in kwargs:
            spell = Spell.objects.get(classname=kwargs["name"]).to_json()
        return Response(spell, mimetype="application/json", status=200)

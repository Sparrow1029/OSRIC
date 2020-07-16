# from flask import Response, request
from flask import request
from flask_restx import Resource, abort
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_claims
from ...core.auth import admin_required

from ...database.models import Class
from ..routes import dnd_api as api
from ..api_models import class_, class_input

ns = api.namespace("classes", description="Database classes operations")


@ns.route("/")
class ClassesApi(Resource):
    @api.marshal_list_with(class_)
    def get(self):
        print(get_jwt_claims())
        return list(Class.objects())
        abort(500, "Something went horribly wrong.")

    @admin_required
    @api.param("Authorization", description="Bearer Token", _in="header", required=True)
    @api.expect(class_input)
    @api.doc(responses={200: "Class Created", 403: "Admins Only"})
    def post(self):
        body = request.get_json()
        class_obj = Class(**body).save()
        id = class_obj.id
        return {'id': str(id)}


@ns.route("/<string:id>")
@ns.param("id", description="Mongodb ObjectId", _in="query")
class ClassApi(Resource):
    @api.marshal_with(class_)
    @api.response(404, "Class not found")
    def get(self, id):
        if ObjectId.is_valid(id):
            obj = Class.objects.get(id=id)
            return obj
        abort(400, "Bad request", error="Invalid object id")

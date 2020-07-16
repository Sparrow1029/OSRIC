# from flask import Response, request
from flask import request
from flask_restx import Resource, abort
from bson import ObjectId
from flask_jwt_extended import jwt_required

from ..database.models import Class
from .routes import dnd_api as api
from .api_models import clss

ns = api.namespace("classes", description="Database classes operations")


@ns.route("/")
class ClassesApi(Resource):
    @ns.doc("list_classes")
    @ns.marshal_list_with(clss)
    def get(self):
        # classes = Class.objects().to_json()
        return list(Class.objects())
        # return Response(classes, mimetype="application/json", status=200)

    @jwt_required
    @ns.doc("create_class")
    @ns.expect(clss)
    @ns.marshal_with(clss, code=201)
    def post(self):
        body = request.get_json()
        clss_ = Class(**body).save()
        id = clss_.id
        return {'id': str(id)}


@ns.route("/<string:search>")
@ns.response(404, "class not found")
@ns.param("search", "Class name or $oid")
class ClassApi(Resource):
    # @jwt_required
    @ns.doc("get_class")
    @ns.marshal_with(clss)
    def get(self, search):
        if ObjectId.is_valid(search):
            obj = Class.objects.get(id=search)
        else:
            obj = Class.objects.get(classname=search)
        return obj
        # return Response(, mimetype="application/json", status=200)


# class ClassesApi(Resource):
#     def get(self):
#         classes = Class.objects().to_json()
#         return Response(classes, mimetype="application/json", status=200)

#     @jwt_required
#     def post(self):
#         body = request.get_json()
#         clss = Class(**body).save()
#         id = clss.id
#         return {'id': str(id)}, 200


# class ClassApi(Resource):

#     @jwt_required
#     def get(self, **kwargs):
#         if "id" in kwargs:
#             clss = Class.objects.get(id=kwargs["id"]).to_json()
#         elif "name" in kwargs:
#             clss = Class.objects.get(classname=kwargs["name"]).to_json()
#         return Response(clss, mimetype="application/json", status=200)

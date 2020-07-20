import datetime
from mongoengine.errors import DoesNotExist, NotUniqueError

from flask_jwt_extended import create_access_token
from flask_restx import Resource, abort

from ...database.models import Player
from ..routes import dnd_api as api
from ..api_models import player_input as api_player
from ..api_models import login

ns = api.namespace("auth", description="Authorization resource endpoint")


@ns.route("/signup")
class SignupApi(Resource):
    @api.expect(api_player)
    @api.doc(responses={
        200: "Successfully Created User",
        400: "Bad Payload"})
    def post(self):
        try:
            body = api.payload
            print(body)
            player = Player(**body)
            player.hash_password()
            player.save()
            id = player.id
            return {"id": str(id)}, 200
        except NotUniqueError as e:
            abort(400, "Bad Payload", error=f"{e}")


@ns.route("/login")
class LoginApi(Resource):
    @api.expect(login, description="Username and password")
    @api.doc(responses={
        200: "Successful Login",
        404: "User Not Found",
        401: "Unauthorized"
    })
    def post(self):
        body = api.payload
        try:
            player = Player.objects.get(username=body["username"])
        except DoesNotExist:
            try:
                player = Player.objects.get(email=body["username"])
            except DoesNotExist:
                abort(404, "User Not Found", error="The username or email does not exist")
        authorized = player.check_password_hash(body["password"])
        if not authorized:
            abort(401, "Unauthorized", error="Invalid username/email password combination")
            # return {"error": "Invalid username/email password combination"}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(str(player.id), expires_delta=expires)
        return {"token": access_token}, 200

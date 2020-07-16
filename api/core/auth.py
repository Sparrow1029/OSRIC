from functools import wraps
from ..database.models import Player
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, get_jwt_claims
)

jwt = JWTManager()


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'admin' not in claims['roles']:
            return {"error": "Administrator access required"}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    claims = {"roles": []}  # , "chars": [], "dm": []}
    player = Player.objects.get(id=identity)
    if player.admin:
        claims["roles"].append("admin")
    # for character in player.characters:
    #     claims["chars"].append(character)
    # for campaign in player.campaigns:
    #     claims["dm"].append(campaign)
    return claims

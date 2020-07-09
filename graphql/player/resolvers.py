from flask_jwt_extended import get_jwt_claims, jwt_required
# from .models import Player


@jwt_required
def resolve_player_claims(info, query, player):
    return get_jwt_claims()

from models import Player

from graphene import (
    Mutation,
    Boolean,
    String,
    Field,
)
from flask_graphql_auth import (
    get_jwt_claims,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    mutation_jwt_required,
    mutation_jwt_refresh_token_required,
)


class AuthMutation(Mutation):
    class Input:
        username = String(required=True)
        password = String(required=True)

    authorized = Boolean()
    access_token = String()
    refresh_token = String()

    @classmethod
    def mutate(cls, _, info, username, password):
        player = Player.objects.get(username=username)

        if not player.check_password_hash(password):
            return AuthMutation(authorized=False)
        return AuthMutation(
            access_token=create_access_token(
                username, user_claims={"create": True}
            ),
            refresh_token=create_refresh_token(username),
            authorized=True
        )


class RefreshMutation(Mutation):
    class Arguments():
        refresh_token = String()

    new_token = String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user))

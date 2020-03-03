from graphene import (
    # ObjectType,
    # Union,
    Mutation,
    String,
)
from flask_graphql_auth import (
    # AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)


class AuthMutation(Mutation):
    class Arguments():
        username = String()
        password = String()

    access_token = String()
    refresh_token = String()

    @classmethod
    def mutate(cls, _, info, username, password):
        return AuthMutation(
            access_token=create_access_token(username),
            refresh_token=creat_refresh_token(username),
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

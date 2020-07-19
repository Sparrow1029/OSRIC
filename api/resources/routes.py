from flask_restx import Api
from mongoengine.errors import DoesNotExist
# from .classes import ClassesApi, ClassApi
# from .spells import SpellsApi, SpellApi
# from .player import PlayersApi, PlayerApi
# from .auth import SignupApi, LoginApi

dnd_api = Api(
    title="D&D Database API",
    version="1.0",
    default="dndb",
    ordered=True,
    prefix="/api"
)


@dnd_api.errorhandler(DoesNotExist)
def handle_does_not_exist(error):
    return {}, 404


def initialize_routes(api):
    from .namespaces import (
        ClassesApi, ClassApi, SpellsApi, SpellApi, SignupApi, LoginApi, CharactersApi,
        CreateCharacter,
    )
    api.add_resource(SpellsApi)
    api.add_resource(SpellApi)
    api.add_resource(ClassesApi)
    api.add_resource(ClassApi)
    api.add_resource(SignupApi)
    api.add_resource(LoginApi)
    api.add_resource(CharactersApi)
    api.add_resource(CreateCharacter)

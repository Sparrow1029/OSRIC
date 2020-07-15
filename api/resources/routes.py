from flask_restx import Api
from mongoengine.errors import DoesNotExist
# from .classes import ClassesApi, ClassApi
# from .spells import SpellsApi, SpellApi
# from .player import PlayersApi, PlayerApi
# from .auth import SignupApi, LoginApi

dnd_api = Api(default="dndb", default_label="DnD Database API")


@dnd_api.errorhandler(DoesNotExist)
def handle_does_not_exist(error):
    print(type(error))
    return {}, 404


def initialize_routes(api):
    from .classes import ClassesApi, ClassApi
    from .spells import SpellsApi, SpellApi
    # from .player import PlayersApi, PlayerApi
    # from .auth import SignupApi, LoginApi
    api.add_resource(ClassesApi)
    api.add_resource(ClassApi)

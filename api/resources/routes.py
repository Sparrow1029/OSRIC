from .classes import ClassesApi, ClassApi
from .spells import SpellsApi, SpellApi
# from .player import PlayersApi, PlayerApi
from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(ClassesApi, "/api/classes")
    api.add_resource(ClassApi, "/api/classes/<kwargs>")
    api.add_resource(SpellsApi, "/api/spells")
    api.add_resource(SpellApi, "/api/spells/<kwargs>")
    api.add_resource(SignupApi, "/api/auth/signup")
    api.add_resource(LoginApi, "/api/auth/login")

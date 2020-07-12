from .classes import ClassesApi, ClassApi
# from .player import PlayersApi, PlayerApi
from .auth import SignupApi

def initialize_routes(api):
    api.add_resource(ClassesApi, '/classes')
    api.add_resource(ClassApi, '/classes/<kwargs>')
    api.add_resource(SignupApi, '/api/auth/signup')

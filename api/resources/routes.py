from .classes import ClassesApi, ClassApi

def initialize_routes(api):
    api.add_resource(ClassesApi, '/classes')
    api.add_resource(ClassApi, '/classes/<kwargs>')

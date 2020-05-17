from graphene import Schema
# from .queries import (
from .graphene_models import (
    # Query,
    Campaign,
    Player,
    Character,
    Modifiers,
    Ability,
    Stats,
    Class,
    Race,
)
from .queries import Query
from .mutations import Mutations

schema = Schema(
    query=Query,
    mutation=Mutations,
    types=[
        Campaign,
        Character,
        Modifiers,
        Ability,
        Player,
        Stats,
        Class,
        Race,
    ])

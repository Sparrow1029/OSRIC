from queries import (
    Query,
    Campaign,
    Player,
    Character,
    Modifiers,
    Ability,
    Stats,
    Class,
    Race,
)
from mutations import Mutations
from graphene import Schema

schema = Schema(
    query=Query,
    mutation=Mutations,
    types=[
        Character,
        Modifiers,
        Ability,
        Player,
        Stats,
        Class,
        Race,
    ])

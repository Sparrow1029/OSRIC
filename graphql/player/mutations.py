from graphene import InputObjectType, Mutation, String, List, Field

from .models import Player, Character
from .types import PlayerType


class PlayerInput(InputObjectType):
    username = String(required=True)
    password = String(required=True)
    characters = List(String)
    real_name = String()


class CreatePlayer(Mutation):
    class Arguments:
        player_data = PlayerInput(required=True)

    player = Field(PlayerType)

    def mutate(self, info, player_data=None):
        char_ids = []
        if player_data.characters:
            char_ids = [Character.objects.get(name=char).id
                        for char in player_data.characters]
        player = Player(
            username=player_data.username,
            password=Player.set_password(player_data.password),
            characters=char_ids,
            real_name=player_data.real_name or 'anonymous'
        )
        player.save()

        return CreatePlayer(player=player)

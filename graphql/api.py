from graphene_federation import build_schema

from .player.schema import PlayerQueries, PlayerMutations
from .character.schema import CharacterQueries, CharacterMutations
from .dndclass.schema import ClassQueries
from .items.schema import ItemQueries, ItemMutations
from .common.schema import CampaignQueries, CampaignMutations

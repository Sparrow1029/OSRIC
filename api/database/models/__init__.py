import mongoengine
from .character_models import Stats, Inventory, ThiefChance
from .player_models import Character, Player
from .object_models import (
    Item, Weapon, Armor, Ability, Spell, Note, Session, Campaign
)
from .class_models import ClassRestrictions, SpellsByLevel, LevelAdvancement, Race, Class
from .npc_models import Npc, Monster

Player.register_delete_rule(Character, 'owner', mongoengine.CASCADE)

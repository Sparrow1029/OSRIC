from .models import Character


def resolve_get_character_inventory(char_id):
    character = Character.objects.get(id=char_id)
    return character.inventory

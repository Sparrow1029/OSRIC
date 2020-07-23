from .models import Character

def change_cur_stats(char, json):
    for field in json:
        if json[field] != char.cur_stats[field]:
            char.cur_stats[field] = json[field]

def manage_gold(char, amt):
    char.inventory.gold = amt

def remove_item_from_inventory(char, item_id):
    pass

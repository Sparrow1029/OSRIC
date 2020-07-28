import json
from functools import wraps
from .models import Character, InventoryItem, InventoryArmor, InventoryWeapon


def ignore_key_error(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyError as e:
            raise RuntimeError(f"{e.__class__.__name__}: {e}")
    return wrapper


# @ignore_key_error
def change_cur_stats(char, updates):
    print(updates["cur_stats"])
    cur_stats = updates["cur_stats"]
    print(cur_stats.keys())
    for key in cur_stats.keys():
        print(key, cur_stats[key])
        if cur_stats[key] != char.cur_stats[key]:
            char.cur_stats[key] = updates[key]


# @ignore_key_error
def manage_gold(char, updates):
    print(updates["inventory"]["gold"])
    char.inventory.gold += updates["inventory"]["gold"]


# @ignore_key_error
def manage_items(char, updates):
    inventory_ids = [item.ref for item in char.inventory.items]
    for item_id, amt in updates["inventory"]["items"].items():
        if item_id not in inventory_ids:
            new_item = InventoryItem(item_id, amount=amt)
            char.inventory.update(add_to_set__items=new_item)
        else:
            existing_item = char.inventory.items.get(ref=item_id)
            existing_item.amount += amt
            if existing_item.amount <= 0:
                char.inventory.update(pull__items={"ref": item_id})


def update_character(char, json_payload):
    change_cur_stats(char, json_payload)
    manage_gold(char, json_payload)
    manage_items(char, json_payload)
    print(char.cur_stats)
    print(char.inventory)
    char.save()
    return char

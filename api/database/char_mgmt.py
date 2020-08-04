import json
from bson import ObjectId
from functools import wraps
from .models import (
    Character, InventoryItem, InventoryArmor, InventoryWeapon, Item, Weapon, Armor
)

def ignore_key_error(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyError as e:
            return f"Missing key: {e}"
    return wrapper


def change_cur_stats(char, updates):
    set_stats = updates["cur_stats"]
    for key in set_stats.keys():
        if set_stats[key] != getattr(char.cur_stats, key):
            setattr(char.cur_stats, key, set_stats[key])


@ignore_key_error
def manage_gold(char, updates):
    print(updates["inventory"]["gold"])
    char.inventory.gold += updates["inventory"]["gold"]


def create_ref(obj, cls):
    obj["info"] = cls.objects.with_id(obj["info"])
    return obj


def update_inventory(payload):
    new_inventory = {
        "gold": payload["inventory"]["gold"],
        "items": [],
        "armor": [],
        "weapons": []
    }
    for item in payload["inventory"]["items"]:
        new_inventory["items"].append(create_ref(item, Item))
    for armor in payload["inventory"]["armor"]:
        new_inventory["armor"].append(create_ref(armor, Armor))
    for weapon in payload["inventory"]["weapons"]:
        new_inventory["weapons"].append(create_ref(weapon, Weapon))
    return new_inventory


@ignore_key_error
def manage_items(char, updates):
    inventory_ids = [item.ref for item in char.inventory.items]
    for item in updates["inventory"]["items"]:
        # action = item["action"]
        if item["ref"] not in inventory_ids:
            new_item = InventoryItem(item["ref"], amount=item["amt"])
            char.inventory.update(add_to_set__items=new_item)
        else:
            existing_item = char.inventory.items.get(ref=item["ref"])
            existing_item.amount += item["amount"]
            if existing_item.amount <= 0:
                char.inventory.update(pull__items={"ref": item["ref"]})


def update_character(char, json_payload):
    change_cur_stats(char, json_payload)
    manage_gold(char, json_payload)
    manage_items(char, json_payload)
    char.save()
    return char

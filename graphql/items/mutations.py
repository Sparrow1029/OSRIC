from graphene import InputObjectType, Mutation, Field, String, Float, Int
from .models import Item, Weapon, Armor
from .types import ItemType, WeaponType, ArmorType


class ItemInput(InputObjectType):
    name = String(required=True)
    weight = Float()
    cost = Float()
    special = String()


class WeaponInput(InputObjectType):
    name = String(required=True)
    category = String(required=True)
    dmg_sm_md = String(required=True)
    dmg_lg = String(required=True)
    encumbrance = Float(required=True)
    rate_of_fire = Float()
    rng = Int()


class ArmorInput(InputObjectType):
    material = String(required=True)
    encumbrance = Int(required=True)
    max_move = Int()
    ac = Int(required=True)
    cost = Float()


class CreateItem(Mutation):
    class Arguments:
        item_data = ItemInput(required=True)

    item = Field(ItemType)

    def mutate(self, info, item_data=None):
        special = item_data.special or "None"
        item = Item(
            name=item_data.name,
            weight=item_data.weight,
            cost=item_data.cost,
            special=special
        )
        item.save()

        return CreateItem(item=item)


class CreateWeapon(Mutation):
    class Arguments:
        weapon_data = WeaponInput(required=True)

    weapon = Field(WeaponType)

    def mutate(self, info, weapon_data=None):
        rate_of_fire = weapon_data.rate_of_fire or '-'
        rng = weapon_data.rate_of_fire or '-'
        magic = weapon_data.magic or '-'

        weapon = Weapon(
            name=weapon_data.name,
            type=weapon_data.type,
            dmg_sm_md=weapon_data.dmg_sm_md,
            dmg_lg=weapon_data.dmg_lg,
            encumbrance=weapon_data.encumbrance,
            cost=weapon_data.cost,
            rate_of_fire=rate_of_fire,
            rng=rng,
            magic=magic
        )
        weapon.save()

        return CreateWeapon(weapon=weapon)


class CreateArmor(Mutation):
    class Arguments:
        armor_data = ArmorInput(required=True)

    armor = Field(ArmorType)

    def mutate(self, info, armor_data=None):
        max_move = armor_data.max_move or '-'
        cost = armor_data.cost or 0.0
        armor = Armor(
            name=armor_data.name,
            material=armor_data.material,
            weight=armor_data.weight,
            max_move=max_move,
            cost=cost,
        )
        armor.save()

        return CreateItem(armor=armor)

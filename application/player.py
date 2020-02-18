#!/usr/bin/env python3
"""Player class and related functions"""
from utils.char_creation import CreateCharacter
# from pprint import pprint as pp

cc = CreateCharacter()


class Player():
    def __init__(self, scores: dict, char_name, player_name, class_type, race):
        """Scores is a dict of str, dex, con, int, wis, cha"""
        self.char_name = char_name
        self.player_name = player_name
        self.race = race
        self.class_type = class_type
        self.base_scores = scores
        self.str_mods = cc.get_strength_mods(scores["str"])
        self.dex_mods = cc.get_dex_mods(scores["dex"])
        self.con_mods = cc.get_const_mods(scores["con"], self.class_type)
        self.cha_mods = cc.get_charisma_mods(scores["cha"])

        self.strength = scores["str"]
        self.dexterity = scores["dex"]
        self.constitution = scores["con"]
        self.wisdom = scores["wis"]
        self.intelligence = scores["int"]
        self.charisma = scores["cha"]

        self.max_addl_langs = cc.get_max_addl_langs(self.intelligence)
        self.mental_save = cc.get_mental_save(self.wisdom)

    def __repr__(self):
        string = f"""
        Player: {self.player_name}\tCharacter: {self.char_name}
        Race: {self.race}\t  Class: {self.class_type}
        {'='*50}
        Str: {self.strength}\tDex: {self.dexterity}\t Con: {self.constitution}
        Wis: {self.wisdom}\tInt: {self.intelligence}\t Cha: {self.charisma}
        Mods:
          {self.str_mods}
          {self.dex_mods}
          {self.con_mods}
          {self.cha_mods}
        """
        return string


scores = {
    "str": 12,
    "dex": 17,
    "con": 13,
    "int": 11,
    "wis": 10,
    "cha": 8
}

p = Player(scores, 'Haldir', 'Alex', 'Thief', 'Half-elf')
print(p)

#!/usr/bin/env python3
from collections import namedtuple

StrMods = namedtuple('StrMods', 'hit_bonus dmg_bonus encumb_adj minor_tests major_tests')
DexMods = namedtuple('DexMods', 'surprise to_hit ac')
ConMods = namedtuple('ConMods', 'hit_per_die survive_dead survive_sys_shock')
ChaMods = namedtuple('ChaMods', 'max_henchmen loyalty_bonus reaction_bonus')

strength_table = {
    3:  [-3, -1, -35, '1', '0'],
    4:  [-2, -1, -25, '1', '0'],
    5:  [-2, -1, -25, '1', '0'],
    6:  [-1, 0, -15, '1', '0'],
    7:  [-1, 0, -15, '1', '0'],
    8:  [0, 0, 0, '1-2', '1'],
    9:  [0, 0, 0, '1-2', '1'],
    10: [0, 0, 0, '1-2', '2'],
    11: [0, 0, 0, '1-2', '2'],
    12: [0,  0, 10, '1-2', '4'],
    13: [0,  0, 10, '1-2', '4'],
    14: [0,  0, 20, '1-2', '7'],
    15: [0,  0, 20, '1-2', '7'],
    16: [0,  1, 35, '1-3', '10'],
    17: [1,  1, 50, '1-3', '13'],
    18: [1,  2, 75, '1-3', '13'],
}

dex_table = {
    9: [0, 0, 0],
    10: [0, 0, 0],
    11: [0, 0, 0],
    12: [0, 0, 0],
    13: [0, 0, 0],
    14: [0, 0, 0],
    15: [0, 0, -1],
    16: [1, 1, -2],
    17: [2, 2, -3],
    18: [3, 3, -4],
    19: [3, 3, -4],
}

const_table = {
    3: [-2, 40, 35],
    4: [-1, 45, 40],
    5: [-1, 50, 45],
    6: [-1, 55, 50],
    7: [0, 60, 55],
    8: [0, 65, 60],
    9: [0, 70, 65],
    10: [0, 75, 70],
    11: [0, 80, 75],
    12: [0, 85, 80],
    13: [0, 90, 85],
    14: [0, 92, 88],
    15: [1, 94, 91],
    16: [2, 96, 95],
    17: [2, 98, 97],
    18: [2, 100, 99],
    19: [2, 100, 99],

}

intel_table = {
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 1,
    9: 1,
    10: 2,
    11: 2,
    12: 3,
    13: 3,
    14: 4,
    15: 4,
    16: 5,
    17: 6,
    18: 7,
    19: 8,
}

wis_table = {
    3: -3,
    4: -2,
    15: 1,
    16: 2,
    17: 3,
    18: 4,
    19: 5
}

cha_table = {
    3: [1, -30, -25],
    4: [1, -25, -20],
    5: [2, -20, -15],
    6: [2, -15, -10],
    7: [3, -10, -5],
    8: [3, -5, 0],
    9: [4, 0, 0],
    10: [4, 0, 0],
    11: [4, 0, 0],
    12: [5, 0, 0],
    13: [5, 0, 5],
    14: [6, 5, 10],
    15: [7, 15, 15],
    16: [8, 20, 25],
    17: [10, 30, 30],
    18: [15, 40, 35],
    19: [20, 50, 40]
}


class CreateCharacter():
    def __init__(self):
        pass

    def get_strength_mods(self, score):
        mod_list = strength_table[score]
        return StrMods(*mod_list)

    def get_dex_mods(self, score):
        mod_list = dex_table[score]
        return DexMods(*mod_list)

    def get_const_mods(self, score, char_class):
        if char_class in ['fighter', 'paladin', 'ranger']:
            if score >= 17:
                table = {
                    17: [3, 98, 97],
                    18: [4, 100, 99],
                    19: [5, 100, 99],
                }
                return ConMods(*table[score])
        return ConMods(*const_table[score])

    def get_max_addl_langs(self, score):
        return intel_table[score]

    def get_mental_save(self, score):
        if score in range(5, 8):
            return -1
        elif score in range(8, 15):
            return 0
        else:
            return wis_table[score]

    def get_charisma_mods(self, score):
        return ChaMods(*cha_table[score])

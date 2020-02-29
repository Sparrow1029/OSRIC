from collections import namedtuple

SavingThrows = namedtuple(
    "SavingThrows",
    [
        "aimed_magic_items",
        "breath_weapons",
        "death",
        "paralysis",
        "poison",
        "petrifaction",
        "polymorph",
        "unlisted"
    ]
)


class Assassin():
    alignments = ['lawful evil', 'neutral evil', 'chaotic evil']
    exp_bonus = None
    lvl_adv = {
        1: 0,
        2: 1600,
        3: 3000,
        4: 5750,
        5: 12250,
        6: 24750,
        7: 50000,
        8: 99000,
        9: 200500,
    }
    saving_throws = {
        range(1, 5): SavingThrows(14, 16, 13, 13, 13, 12, 12, 15),
        range(5, 9): SavingThrows(12, 15, 12, 12, 12, 11, 11, 13),
        range(9, 13): SavingThrows(10, 14, 11, 11, 11, 10, 10, 11),
        range(13, 25): SavingThrows(8, 13, 10, 10, 10, 9, 9, 9),
    }


if __name__ == "__main__":
    a = Assassin
    for i in [3, 7, 12, 14]:
        for rng in a.saving_throws:
            if i in rng:
                print(a.saving_throws[rng])

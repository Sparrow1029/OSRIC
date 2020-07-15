# Race information as series of dicts

DWARF = {
    "name": "dwarf",
    "base_stat_mods": {
        "str": 0, "dex": 0, "con": 1,
        "int": 0, "wis": 0, "cha": -1
    },
    "bonuses": [
        "+1 to hit against goblins, half-orcs, hobgoblins, and orcs",
        "+1 bonus per 3.5 points of Con to saves against magic and poison",
        "-4 penalty to any attacks made against the dwarf by giants, ogres, ogre mages, titans and trolls."
    ],
    "abilities": {
        "infravision": 60,
        "other": "Within 10 ft, a dwarf can detect certain facts concerning engineering, "
        "stonework, etc. Although no significant time is required, the character must deliberately "
        "observe his or her surroundings (i.e., the player must state that the dwarf is using this "
        "particular talent in order to gain information).\n"
        "- Detect the existence of slopes or grades: 75%\n"
        "- Detect the existence of new construction: 75%\n"
        "- Detect sliding or shifting rooms or walls: 66%\n"
        "- Detect traps involving stonework: 50%\n"
        "- Determine depth underground: 50%"
    },
    "languages": ["dwarfish", "gnomish", "goblin", "kobold", "orcish"],
    "max_addl_languages": 2,
    "permitted_classes": [
        "assassin", "cleric", "fighter", "thief",
        # "fighter/thief"
    ],
    "movement_rate": 90,
    "starting_age": {
        "cleric": "250+2d20",
        "fighter": "40+5d4",
        "thief": "75+3d6",
    },
    "score_limits": {
        "min_str": 8, "max_str": 18,
        "min_dex": 3, "max_dex": 17,
        "min_con": 12, "max_con": 19,
        "min_int": 3, "max_int": 18,
        "min_wis": 3, "max_wis": 18,
        "min_cha": 3, "max_cha": 16
    },
}

ELF = {
    "name": "elf",
    "base_stat_mods": {
        "str": 0, "dex": 1, "con": -1,
        "int": 0, "wis": 0, "cha": 0
    },
    "bonuses": ["90% resistance to sleep and charm spells"],
    "abilities": {
        "any_pulled_bow": "+1 to hit",
        "longsword_and_short_sword": "+1 to hit",
        "infravision": 60,
        "detect_secret_doors": "1 in 6 chance to notice secret doors when passing within 10 ft, "
        "2 in 6 chance to discover secret doors when searching, and 3 in 6 chance to discover "
        "concealed doors when searching.",
        "surprise": "4 in 6 chance to surprise when travelling in nonmetal armour and alone, "
        "or more than 90 ft in advance of others, or with a party entirely consisting of elves "
        "and/or halflings. If a door must be opened (or some similar task), "
        "the chance of surprise drops to 2 in 6.",
    },
    "languages": ["common", "elven", "gnoll", "gnomish", "goblin", "halfling", "hobgoblin", "orcish"],
    "max_addl_languages": 3,
    "permitted_classes": [
        "assassin", "cleric", "fighter", "magic_user", "thief",
        # "fighter/magic_user", "fighter/thief", "magic_user/thief", "fighter/magic_user/thief"
    ],
    "movement_rate": 120,
    "starting_age": {
        "cleric": "500+10d10",
        "fighter": "130+5d6",
        "magic_user": "150+5d6",
        "thief": "100+5d6"
    },
    "score_limits": {
        "min_str": 3, "max_str": 18,
        "min_dex": 7, "max_dex": 19,
        "min_con": 8, "max_con": 17,
        "min_int": 8, "max_int": 18,
        "min_wis": 3, "max_wis": 18,
        "min_cha": 8, "max_cha": 18
    },
}

GNOME = {
    "name": "gnome",
    "base_stat_mods": {
        "str": 0, "dex": 0, "con": 0,
        "int": 0, "wis": 0, "cha": 0
    },
    "bonuses": [
        "+1 bonus per 3.5 points of Con to saves against magic and poison",
        "+1 to hit kobolds and goblins",
        "-4 to attack rolls by bugbears, giants, gnolls, ogres, ogre mages, titans, and trolls."
    ],
    "languages": ["common", "dwarfish", "gnomish", "goblin", "halfling", "kobold"],
    "max_addl_languages": 2,
    "abilities": {
        "infravision": 60,
        "speak_with_animals": "Gnomes may communicate with any normal burrowing animal.",
        "other": "Within 10 ft, a gnome can detect certain facts concerning engineering, stonework, etc. Although no significant time is required, the character must deliberately observe his or her surroundings (i.e., the player must state that the dwarf is using this particular talent in order to gain information).\n- Detect the existence of slopes or grades: 80%\n- Detect the existence of unsafe wall, ceiling, floor: 70%\n- Determine depth underground: 60%\n- Determine direction of north underground: 50%"
    },
    "permitted_classes": [
        "assassin", "cleric", "fighter", "illusionist", "thief",
        # "fighter/illusionist", "fighter/thief", "illusionist/thief""
    ],
    "movement_rate": 90,
    "starting_age": {
        "cleric": "300+3d12",
        "fighter": "60+5d4",
        "magic_user": "100+2d12",
        "thief": "80+5d4"
    },
    "score_limits": {
        "min_str": 6, "max_str": 18,
        "min_dex": 3, "max_dex": 18,
        "min_con": 8, "max_con": 18,
        "min_int": 7, "max_int": 18,
        "min_wis": 3, "max_wis": 18,
        "min_cha": 3, "max_cha": 18
    },
}

HALF_ELF = {
    "name": "half_elf",
    "base_stat_mods": {
        "str": 0, "dex": 0, "con": 0,
        "int": 0, "wis": 0, "cha": 0
    },
    "bonuses": [
        "30% resistance to sleep and charm spells"
    ],
    "abilities": {
        "secret_doors": "When searching, a half-elf character can detect secret doors on a 2 in 6 and concealed doors on a 3 in 6. When passing within 10ft of a concealed door, a half-elf will notice it on a 1 in 6.",
        "infravision": 60,
    },
    "languages": ["common", "elven", "gnoll", "gnome", "goblin", "halfling", "hobgoblin", "orcish"],
    "max_addl_languages": 0,
    "permitted_classes": [
        "assassin", "cleric", "fighter", "magic_user", "ranger", "thief",
        # "cleric/fighter", "cleric/ranger", "cleric/magic_user", "fighter/magic_user",
        # "fighter/thief", "magic_user/thief", "cleric/fighter/magic_user", "fighter/magic_user/thief"
    ],
    "movement_rate": 90,
    "starting_age": {
        "cleric": "40+2d4",
        "fighter": "22+3d4",
        "magic_user": "30+2d8",
        "thief": "22+3d8"
    },
    "score_limits": {
        "min_str": 3, "max_str": 18,
        "min_dex": 6, "max_dex": 18,
        "min_con": 6, "max_con": 18,
        "min_int": 4, "max_int": 18,
        "min_wis": 3, "max_wis": 18,
        "min_cha": 3, "max_cha": 18
    },
}

HALFLING = {
    "name": "halfling",
    "base_stat_mods": {
        "str": -1, "dex": 1, "con": 0,
        "int": 0, "wis": 0, "cha": 0
    },
    "bonuses": [
        "+1 bonux per 3.5 points of Con to saves against magic (both aimed magic items and spells) and poison",
        "+3 bonus to attacks with a bow or sling",
    ],
    "abilities": {
        "surprise": "4 in 6 chance to surprise when travelling in nonmetal armour and alone, "
        "or more than 90 ft in advance of others, or with a party entirely consisting of elves "
        "and/or halflings.  If a door must be opened (or some similar task), "
        "the chance of surprise drops to 2 in 6.",
        "infravision": 60,
    },
    "languages": ["common", "dwarfish", "gnome", "goblin", "halfling", "orcish"],
    "max_addl_languages": 2,
    "permitted_classes": [
        "fighter", "druid", "thief",
        # "fighter/thief"
    ],
    "movement_rate": 90,
    "starting_age": {
        "fighter": "20+3d4",
        "druid": "40+3d4",
        "thief": "40+2d4"
    },
    "score_limits": {
        "min_str": 6, "max_str": 17,
        "min_dex": 8, "max_dex": 19,
        "min_con": 10, "max_con": 18,
        "min_int": 6, "max_int": 18,
        "min_wis": 3, "max_wis": 17,
        "min_cha": 3, "max_cha": 18
    },
}

HALF_ORC = {
    "name": "half_orc",
    "base_stat_mods": {
        "str": 1, "dex": 0, "con": 1,
        "int": 0, "wis": 0, "cha": -2
    },
    "bonuses": [],
    "abilities": {
        "infravision": 60,
    },
    "languages": ["common", "orcish"],
    "max_addl_languages": 2,
    "permitted_classes": [
        "assassin", "cleric", "fighter", "thief",
        # "cleric/fighter", "cleric/thief", "cleric/assassin", "fighter/thief", "fighter/assassin"
    ],
    "movement_rate": 120,
    "starting_age": {
        "fighter": "20+1d4",
        "druid": "13+1d4",
        "thief": "20+2d4"
    },
    "score_limits": {
        "min_str": 6, "max_str": 18,
        "min_dex": 3, "max_dex": 17,
        "min_con": 13, "max_con": 19,
        "min_int": 3, "max_int": 17,
        "min_wis": 3, "max_wis": 14,
        "min_cha": 3, "max_cha": 12
    },
}


HUMAN = {
    "name": "human",
    "base_stat_mods": {
        "str": 0, "dex": 0, "con": 0,
        "int": 0, "wis": 0, "cha": 0
    },
    "bonuses": [],
    "abilities": {},
    "languages": ["common"],
    "max_addl_languages": 10,
    "permitted_classes": [
        "assassin", "cleric", "fighter", "thief",
        # "cleric/fighter", "cleric/thief", "cleric/assassin", "fighter/thief", "fighter/assassin"
    ],
    "movement_rate": 120,
    "starting_age": {
        "fighter": "20+1d4",
        "druid": "13+1d4",
        "thief": "20+2d4"
    },
    "score_limits": {
        "min_str": 6, "max_str": 18,
        "min_dex": 3, "max_dex": 17,
        "min_con": 13, "max_con": 19,
        "min_int": 3, "max_int": 17,
        "min_wis": 3, "max_wis": 14,
        "min_cha": 3, "max_cha": 12
    },
}

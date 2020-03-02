from mongoengine import connect

from models import Character, Stats, Race, Class, Ability, Modifiers

connect("dnd-graphene-mongo-test", host="mongomock://localhost", alias="default")


def init_db():
    # Create classes
    assassin = Class(name="assassin")
    druid = Class(name="druid")
    cleric = Class(name="cleric")
    for class_ in [assassin, druid, cleric]:
        class_.save()

    # Create some abilities
    infravision = Ability(name="infravision", description="60ft")
    detect_stonework = Ability(name="detect_stonework", description="Recognize stonework")

    # Race Mods
    elf_mods = [Modifiers(type_="dex", value=1), Modifiers(type_="con", value=-1)]
    dwarf_mods = [Modifiers(type_="con", value=1), Modifiers(type_="cha", value=-1)]

    # Create races
    dwarf = Race(
        name="dwarf",
        mods=dwarf_mods,
        abilities=[infravision, detect_stonework],
        permitted_classes=['assassin', 'cleric', 'fighter', 'thief'],
    )
    elf = Race(
        name="elf",
        mods=elf_mods,
        abilities=[infravision],
        permitted_classes=['assassin', 'cleric', 'fighter', 'magic_user', 'thief']
    )
    dwarf.save()
    elf.save()

    # Create some damn characters
    dude = Character(
        name="Dude",
        stats=Stats(
            str_=12,
            dex=12,
            con=13,
            int_=15,
            wis=12,
            cha=14,
        ),
        class_=assassin,
        race=elf,
        cur_campaign="Darkness comes",
        align="neutral_evil",
    )
    guyette = Character(
        name="Guyette",
        stats=Stats(
            str_=12,
            dex=13,
            con=10,
            int_=13,
            wis=15,
            cha=17,
        ),
        class_=druid,
        race=dwarf,
        cur_campaign="Darkness comes",
        align="neutral_neutral"
    )
    dude.save()
    guyette.save()
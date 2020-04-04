from mongoengine import connect

from .models import (
    Character,
    Player,
    Stats,
    Race,
    Class,
    Ability,
    Modifiers,
)

db = connect("dnd-graphene-mongo-test", host="mongomock://localhost", alias="default")



def init_db():
    # Create classes
    assassin = Class(name="assassin")
    druid = Class(name="druid")
    cleric = Class(name="cleric")
    for clss in [assassin, druid, cleric]:
        clss.save()

    # Create some abilities
    infravision = Ability(name="infravision", description="60ft")
    detect_stonework = Ability(name="detect_stonework", description="Recognize stonework")

    # Race Mods
    elf_mods = [Modifiers(type="dex", value=1), Modifiers(type="con", value=-1)]
    dwarf_mods = [Modifiers(type="con", value=1), Modifiers(type="cha", value=-1)]

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
            str=12,
            dex=12,
            con=13,
            int=15,
            wis=12,
            cha=14,
        ),
        clss=assassin,
        race=elf,
        cur_campaign="Darkness comes",
        align="neutral_evil",
    )
    dudette = Character(
        name="Dudette",
        stats=Stats(
            str=12,
            dex=13,
            con=10,
            int=13,
            wis=15,
            cha=17,
        ),
        clss=druid,
        race=dwarf,
        cur_campaign="Darkness comes",
        align="neutral_neutral"
    )
    dude.save()
    dudette.save()

    # Create some damn players
    alex = Player(
        username="sparrow",
        password=Player.set_password("password"),
        characters=[dude],
        real_name="Alex"
    )
    alex.save()
    # print(alex.pk)
    # print(db.__dict__)

    nikki = Player(
        username="pillowprincess",
        password=Player.set_password("dollybear"),
        characters=[dudette],
        real_name="Nikki"
    )
    # print(nikki.list_indexes())
    nikki.save(force_insert=True)

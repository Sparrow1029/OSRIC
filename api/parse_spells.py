import os
import re
from csv import DictReader

from database.object_models import Spell, db

db.connect('dnd_database', host='127.0.0.1', port=27017)


working_dir = os.path.dirname(os.path.abspath(__file__))

spell_file = os.path.join(working_dir, "database", "seed_data", "all_spells.csv")
embed_rgx = re.compile(r"\$[^\$]*@", re.S | re.M)


class EmbeddedTable:
    def __init__(self, text):
        self.data = text
        self.title = None
        self.headers = None
        self.rows = []
        self.format_embedded_table()

    @staticmethod
    def get_tables(orig):
        tables = []
        capturing = False
        cur_table = []
        for i in range(len(orig)):
            char = orig[i]
            if char == '@':
                capturing = False
                tables.append(''.join(cur_table))
                cur_table = []
            if capturing:
                cur_table.append(char)
            elif char == '$':
                capturing = True
        return tables

    def format_embedded_table(self):
        data = self.data.splitlines()
        if data[0]:
            title, headstr = data[0].split(':')
            self.title = title
            if headstr:
                t_headers = headstr.split('|')
                self.headers = t_headers
        for tbl_row in data[1:]:
            self.rows.append(tbl_row.split('|'))

    def pprint(self):
        if self.headers:
            fmt_str = " {:-^30} |"*len(self.headers)
            headers = fmt_str.format(*self.headers)
        else:
            headers = ''
        if self.title:
            title = "{:^60}".format(self.title)
        else:
            title = ''
        num_fields = len(self.rows[0])
        fmt_row = " {:^30} |"*num_fields
        formatted = [
            title, headers,
            *[fmt_row.format(*row) for row in self.rows]
        ]

        return '\n'.join(formatted)


def parse_spells(csv_file):
    with open(csv_file, 'r') as f:
        reader = DictReader(f)
        for row in reader:
            embedded_tables = []
            orig_description = row['description']
            if '$' in orig_description:
                new_description = re.sub(embed_rgx, '', orig_description)
                tables = EmbeddedTable.get_tables(orig_description)
                embedded = [EmbeddedTable(data) for data in tables]

                embedded_tables = [
                    {"title": e.title,
                     "headers": e.headers,
                     "rows": e.rows} for e in embedded]

            spell = Spell(
                classname=row["classname"].lower(),
                spellname=row["spellname"].lower(),
                level=row["level"],
                range=row["range"],
                duration=row["duration"],
                aoe=row["aoe"],
                components=row["components"].split(),
                casting_time=row["casting_time"],
                saving_throw=row["saving_throw"],
                description=orig_description,
            )
            if embedded_tables:
                spell.embedded_tables = embedded_tables
                spell.description = new_description

            spell.save()


if __name__ == "__main__":
    parse_spells(spell_file)

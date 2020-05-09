import os
from csv import DictReader
# from collections import defaultdict
from pymongo import MongoClient
import re

client = MongoClient('localhost', 27017)
db = client.spells

working_dir = os.path.dirname(os.path.abspath(__file__))
spell_files = [os.path.join(working_dir, f)
               for f in os.listdir(working_dir) if f.endswith('.csv')]


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
            headers, title,
            *[fmt_row.format(*row) for row in self.rows] 
        ]

        return '\n'.join(formatted)


for csv_file in spell_files:
    with open(csv_file, 'r') as fh:
        reader = DictReader(fh)
        for i in range(len(reader.fieldnames)):
            reader.fieldnames[i] = reader.fieldnames[i].replace(" ", "_")
        for row in reader:
            if '$' in row['description']:
                orig = row['description']
                tables = EmbeddedTable.get_tables(orig)
                embedded = [EmbeddedTable(data) for data in tables]
                new = ''.join(re.sub(embed_rgx, "!!", orig, re.M | re.S))
                for e in embedded:
                    new = new.replace("!!", e.pprint(), 1)
                print(new)

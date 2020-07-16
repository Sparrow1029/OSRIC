from flask_restx import fields

class MongoId(fields.Raw):
    def __init__(self, *args, **kwargs):
        self.desc = "Mongodb ObjectId ($oid)"
        super().__init__(description=self.desc, *args, **kwargs)

    def format(self, value):
        return str(value)

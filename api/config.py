class Config:
    DEBUG = False
    TESTING = False
    MONGO_URI = "mongodb://localhost:27017/dnd_database"


class DebugConfig:
    DEBUG = True
    TESTING = False
    MONGO_DBNAME = "dnd_database"
    MONGO_URI = "mongodb://localhost:27017/dnd_database"

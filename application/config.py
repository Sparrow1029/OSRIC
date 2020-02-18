import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-get-this")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" +
                                            os.path.join(basedir, "app.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

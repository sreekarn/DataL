import os
from pathlib import Path

class Development(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
    SECRET_KEY = 'my precious'
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))

    TEMP_DIR = os.path.join(BASE_DIR, 'TEMP')
     

class Production(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
    SECRET_KEY = 'my precious'
    HOST = 'localhost'
    PORT = int(os.environ.get('PORT', 5000))


Config = Development

def init_config():
    if not Path(Config.TEMP_DIR).is_dir():
        Path(Config.TEMP_DIR).mkdir(parents=True, exist_ok=True)
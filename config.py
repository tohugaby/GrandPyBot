import os
import random
import string

base_dir = os.path.abspath(os.path.dirname(__file__))


try:
    api_key_file_path = os.path.join(base_dir,'api_keys.txt')
    with open(api_key_file_path) as keys_file:
        from_file_key = keys_file.readlines()[0]
except FileNotFoundError:
    from_file_key = str()

GOOGLE_MAP_API_KEY = os.environ.get('GOOGLE_MAP_API_KEY') or from_file_key

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "change_me"

    # custom variables
    DATA_FOLDER = "data_files"
    DATA_PATH = os.path.join(base_dir, DATA_FOLDER)

    DATA_LOAD_CONFIG = {
        "stop_words": {
            "files": [os.path.join(DATA_PATH, "stop_words/stop_words.txt")],
            "handler": "insert_stop_words"
        },
        "french_words": {
            "files": [os.path.join(DATA_PATH, "french_words/liste_de_mots_francais_frgut.txt")],
            "handler": "insert_french_words"
        },
        "cities": {
            "files": [
                os.path.join(DATA_PATH, "cities/cities1000.txt"),
                os.path.join(DATA_PATH, "cities/cities5000.txt"),
                os.path.join(DATA_PATH, "cities/cities15000.txt")
            ],
            "handler": "insert_cities"
        },
        "countries": {
            "files": [os.path.join(DATA_PATH, "countries/sql-pays.csv")],
            "handler": "insert_countries"
        }
    }


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = "change_me"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, "test.db")

    # custom variables
    DATA_FOLDER = "data_files_test"
    DATA_PATH = os.path.join(base_dir, DATA_FOLDER)

    DATA_LOAD_CONFIG = {
        "stop_words": {
            "files": [os.path.join(DATA_PATH, "stop_words/stop_words_sample.txt")],
            "handler": "insert_stop_words"
        },
        "french_words": {
            "files": [os.path.join(DATA_PATH, "french_words/french_words_sample.txt")],
            "handler": "insert_french_words"
        },
        "cities": {
            "files": [
                os.path.join(DATA_PATH, "cities/cities_sample.txt"),
            ],
            "handler": "insert_cities"
        },
        "countries": {
            "files": [os.path.join(DATA_PATH, "countries/countries_sample.csv")],
            "handler": "insert_countries"
        }
    }


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, "grandpy.db")


class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    if not os.path.exists('secret.txt'):
        with open('secret.txt', 'w') as secret_file:
            new_secret = "".join(
                [random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(24)])
            secret_file.write(new_secret)
    with open('secret.txt', 'r') as secret_file:
        SECRET_KEY = "".join(secret_file.readlines())

    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, "grandpy.db")
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "change_me"
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/grandpybot"

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

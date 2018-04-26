from project import app


def insert_stop_words():
    words = list()
    for file in app.config["DATA_LOAD_CONFIG"]["stop_words"]["files"]:
        with open(file, "r") as word_file:
            words += word_file.read().split("\n")
    return words


def insert_french_words():
    words = list()
    for file in app.config["DATA_LOAD_CONFIG"]["french_words"]["files"]:
        with open(file, "r") as word_file:
            words += word_file.read().split("\n")
    return words


def insert_cities():
    cities = list()
    words = list()
    for file in app.config["DATA_LOAD_CONFIG"]["cities"]["files"]:
        with open(file, 'r') as word_file:
            l = word_file.read()
            line_list = l.split("\n")
            cities += [city.split("\t") for city in line_list if len(city) > 1]

    words += [city[2] for city in cities]
    return words


def insert_countries():
    words = list()
    countries = list()
    for file in app.config["DATA_LOAD_CONFIG"]["countries"]["files"]:
        with open(file, "r") as word_file:
            line = word_file.read().replace('"', "")
            line_list = line.split("\n")
            countries += [country.split(",") for country in line_list if len(country) > 1]
    words += sorted([country[4] for country in countries] + [country[5] for country in countries])
    return words

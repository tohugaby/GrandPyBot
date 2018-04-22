import os
import re

from config import data_files_path


class LegacyParser:

    def __init__(self, in_string):
        self.in_string = in_string
        self.out_list = self._parse_string()

    def _parse_string(self):
        return self._apply_parsing(self._get_compare_list())

    def _get_compare_list(self):
        return self._split_string()

    def _apply_parsing(self, compare_list, contained=True):
        if contained:
            return [word for word in self._split_string() if word in compare_list and word != str()]
        return [word for word in self._split_string() if word not in compare_list and word != str()]

    def _split_string(self):
        return self.in_string.split(" ")


class NotContainedInListParserMixin:
    def _parse_string(self):
        return self._apply_parsing(self._get_compare_list(), contained=False)


class NonLettersParser(LegacyParser):
    def _split_string(self):
        tmp_out_list = re.split(" +|'+|\?+|!+|\.+|-+", self.in_string)
        return tmp_out_list


class StopWordsParser(NotContainedInListParserMixin, NonLettersParser):

    def _get_compare_list(self):
        with open(os.path.join(data_files_path, "stop_words/stop_words.txt")) as stop_words_files:
            stop_words = stop_words_files.read().split("\n")
        return stop_words


class FrenchWordsParser(NotContainedInListParserMixin, NonLettersParser):

    def _get_compare_list(self):
        with open(os.path.join(data_files_path, "french_words/liste_de_mots_francais_frgut.txt"), "r") as french_dico:
            french_words = french_dico.read().split("\n")
        return french_words


class CitiesParser(NonLettersParser):

    def _get_compare_list(self):
        city_list = list()
        files_list = [
            os.path.join(data_files_path, "cities/cities1000.txt"),
            os.path.join(data_files_path, "cities/cities5000.txt"),
            os.path.join(data_files_path, "cities/cities15000.txt")
        ]

        for city_file in files_list:
            with open(city_file, 'r') as f:
                l = f.read()
                line_list = l.split("\n")
                city_list += [city.split("\t") for city in line_list if len(city) > 1]

        city_name_list = [city[2] for city in city_list]
        return city_name_list


class CountriesParser(NonLettersParser):
    def _get_compare_list(self):
        country_list = list()
        with open(os.path.join(data_files_path, "countries/sql-pays.csv")) as file:
            line = file.read().replace('"', "")
            line_list = line.split("\n")
            country_list += [country.split(",") for country in line_list if len(country) > 1]
        country_name_list = sorted([country[4] for country in country_list] + [country[5] for country in country_list])
        return country_name_list

import re

from project.parser.models import WordType, Word


class LegacyParser:
    """A parser that take an in string and return a list of word after comparing this string with another list of
    words"""

    def __init__(self, in_string):
        self.in_string = in_string
        self.out_list = self._parse_string()

    def _parse_string(self):
        return self._apply_parsing(self._get_compare_list())

    def _get_compare_list(self):
        return self._split_string()

    def _apply_parsing(self, compare_list, contained=True):
        """
        Compare provided list with comparing list of word and generate a new list containing intersection of both list
        if contained parameter is True (default usage) or the opposite if contained is False
        :param compare_list: list of words used to compare with initial string words
        :param contained: define what to return.
        :return: a list of words
        """
        if contained:
            return [word for word in self._split_string() if word in compare_list and word != str()]
        return [word for word in self._split_string() if word not in compare_list and word != str()]

    def _split_string(self):
        return self.in_string.split(" ")


class NotContainedInListParserMixin:
    """
    Mixin reverses parsing default usage by returning words of initial string which are not contained in compare list
    """

    def _parse_string(self):
        return self._apply_parsing(self._get_compare_list(), contained=False)


class FromDatabaseCompareListMixin:
    """
    Mixin allows to get compare list from table Word of database
    """

    def _get_compare_list(self):
        """
        get compare list from database according provided key which represent a word category in Word table
        :return: a list of words.
        """
        if self.key:
            words = Word.query.join(WordType).filter(WordType.type_name == self.key)
            return [word.word for word in words.all()]
        return []


class NonLettersParser(LegacyParser):
    """
    Mixin allows cleaning string before comparison
    """

    def _split_string(self):
        """
        Transform string to list by removing useless symbols, space...
        :return: a list of words
        """
        tmp_out_list = re.split(" +|'+|\?+|!+|\.+|-+", self.in_string)
        return tmp_out_list


class StopWordsParser(NotContainedInListParserMixin, FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of stop words"""
    key = "stop_words"


class FrenchWordsParser(NotContainedInListParserMixin, FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of french words"""
    key = "french_words"


class CitiesParser(FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of cities"""
    key = "cities"


class CountriesParser(FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of countries"""
    key = "countries"

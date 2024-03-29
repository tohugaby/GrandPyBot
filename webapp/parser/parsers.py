"""
All the parsers used to parse user question.
"""
import logging
import re

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class LegacyParser:
    """A parser that take an in string and return a list of word
    after comparing this string with another list of words"""

    def __init__(self, in_string, database_extract):
        self.in_string = in_string
        self.database_extract = database_extract
        self.out_list = self._parse_string()
        LOGGER.debug(" %s: %s", self.__class__, self.out_list)

    def _parse_string(self):
        return self._apply_parsing(self._get_compare_list())

    def _get_compare_list(self):
        return self._split_string()

    def _apply_parsing(self, compare_list, contained=True):
        """
        Compare provided list with comparing list of word and
        generate a new list containing intersection of both list
        if contained parameter is True (default usage) or
        the opposite if contained is False
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
    Mixin reverses parsing default usage by returning words of initial string
    which are not contained in compare list
    """

    def _parse_string(self):
        return self._apply_parsing(self._get_compare_list(), contained=False)


class FromDatabaseCompareListMixin:
    """
    Mixin allows to get compare list from table Word of database
    """

    def _get_compare_list(self):
        """
        get compare list from database according provided key
        which represent a word category in Word table
        :return: a list of words.
        """
        if self.key:
            if self.key in self.database_extract:
                # words = Word.query.join(WordType).filter(WordType.type_name == self.key)
                # return [word.word for word in words.all()]
                return self.database_extract[self.key]
        return []


class NonLettersParser(LegacyParser):
    """
    Class allows cleaning string before comparison
    """

    def _split_string(self):
        """
        Transform string to list by removing useless symbols, space...
        :return: a list of words
        """
        tmp_out_list = re.split(r" +|'+|\?+|!+|\.+|_+", self.in_string)
        return tmp_out_list


class UniqueLetterParser(NonLettersParser):
    """
    Parser to remove unique letters
    """

    def _split_string(self):
        """
        Transform string to list by removing useless symbols, space...
        :return: a list of words
        """
        tmp_out_list = re.split(r" +|'+|\?+|!+|\.+|_+", self.in_string)
        tmp_out_list = [word for word in tmp_out_list if len(word) > 1]
        return tmp_out_list


class BeforeLinkWorkParser(LegacyParser):
    """
    words before a link word are sometimes important. This parser will parse them.
    """

    def _split_string(self):
        link_words = ('à', 'chez', 'au', 'en')
        tmp_out_list = re.split(r" +|'+|\?+|!+|\.+|_+", self.in_string)
        link_words_indexes = [index for index, word in enumerate(tmp_out_list)
                              if word in link_words]
        tmp_out_list = [tmp_out_list[index - 1] for index in link_words_indexes]
        return tmp_out_list


class AfterLinkWorkParser(LegacyParser):
    """parse word after a link word"""

    def _split_string(self):
        link_words = ('à', 'chez', 'au', 'en')
        tmp_out_list = re.split(r" +|'+|\?+|!+|\.+|_+", self.in_string)
        link_words_indexes = [index for index, word in enumerate(tmp_out_list)
                              if word in link_words]
        tmp_out_list = [tmp_out_list[index + 1] for index in link_words_indexes
                        if index + 1 <= len(tmp_out_list)]
        return tmp_out_list


class StopWordsParser(NotContainedInListParserMixin, FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of stop words"""
    key = "stop_words"

    def _split_string(self):
        """
        Transform string to list by removing useless symbols, space...
        :return: a list of words
        """
        symbols = ('.', '!', '?')
        tmp_list = self.in_string.split()
        index_list = [0] + [index + 1 for index, value in enumerate(tmp_list) if value in symbols]
        for i in index_list:
            if i + 1 <= len(tmp_list):
                tmp_list[i] = tmp_list[i].lower()
        tmp_out_list = re.split(r" +|'+|\?+|!+|\.+|_+", " ".join(tmp_list))
        return tmp_out_list


class FrenchWordsParser(NotContainedInListParserMixin, FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of french words"""
    key = "french_words"

    def _split_string(self):
        """
        Transform string to list by removing useless symbols, space...
        :return: a list of words
        """
        symbols = ('.', '!', '?')
        tmp_list = self.in_string.split()
        index_list = [0] + [index + 1 for index, value in enumerate(tmp_list) if value in symbols]
        for i in index_list:
            if i + 1 <= len(tmp_list):
                tmp_list[i] = tmp_list[i].lower()
        tmp_out_list = re.split(r" +|'+|\?+|!+|\.+|_+", " ".join(tmp_list))
        return tmp_out_list


class CitiesParser(FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of cities"""
    key = "cities"


class CountriesParser(FromDatabaseCompareListMixin, NonLettersParser):
    """A parser which compare provided string with a list of countries"""
    key = "countries"


class ExpressionParser(LegacyParser):
    """"""

    def _parse_string(self):
        return self._apply_parsing(self._get_compare_list())

    def _get_compare_list(self):
        return self._split_string()

    def _apply_parsing(self, compare_list, contained=True):
        """
        Compare provided list with comparing list of word and
        generate a new list containing intersection of both list
        if contained parameter is True (default usage) or
        the opposite if contained is False
        :param compare_list: list of words used to compare with initial string words
        :param contained: define what to return.
        :return: a list of words
        """
        if contained:
            return [word for word in self._split_string() if word in compare_list and word != str()]
        return [word for word in self._split_string() if word not in compare_list and word != str()]

    def _split_string(self):
        result = list()
        sub_list = list()
        tmp_list = self.in_string.split(" ")
        tmp_string = str()
        for e, word in enumerate(tmp_list):
            if word.lower() in ['rue', 'place', 'avenue', 'impasse', 'route', 'lotissement', 'lieu-dit', 'quartier',
                                'tour', 'château', 'parc', 'basilique', 'église', 'abbaye', 'chemin', 'carrefour',
                                'site', 'musée', 'chapelle', 'cimetière', 'passage', 'synagogue', 'mosquée',
                                'théâtre', 'cathédrale', 'cour']:
                tmp_string += word
                sub_list = tmp_list[e + 1:]
                break
        for e, word in enumerate(sub_list):
            tmp_string += " " + word
            if word.lower() not in ["du", "de", "la", "de"]:
                break
        print(tmp_string)

        result.append(tmp_string)
        print(result)
        return result

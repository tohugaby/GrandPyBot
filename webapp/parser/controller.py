"""
Controller module that calls all parser
"""

from collections import OrderedDict

import logging
import re

from webapp.models import Word, WordType
from webapp.parser.parsers import BeforeLinkWorkParser, AfterLinkWorkParser, NonLettersParser, \
    UniqueLetterParser, StopWordsParser, FrenchWordsParser, CountriesParser, CitiesParser

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class ParsingController:
    """
    Controller that launch all parser and define by weight ordered list results
    """
    parsers = [
        (BeforeLinkWorkParser, 2),
        (AfterLinkWorkParser, 0.3),
        (NonLettersParser, 1),
        (UniqueLetterParser, 1.1),
        (StopWordsParser, 1.1),
        (FrenchWordsParser, 1.2),
        (CountriesParser, 1.3),
        (CitiesParser, 1.4),
    ]

    def __init__(self, in_string, parsers=None):
        self.in_string = in_string
        if parsers:
            self.parsers = parsers
        LOGGER.info(" Start parsing: %s", self.in_string)
        self.database_extract = self.ask_database()
        self.out_list = self._compile_results()
        LOGGER.info(" Parsing finished: %s", self.out_list)

    def ask_database(self):
        word_in_db = dict()
        tmp_list = self.in_string.split()
        splited_string = re.split(r" +|'+|\?+|!+|\.+|_+", " ".join(tmp_list))
        results = Word.query.join(WordType, Word.category == WordType.id).filter(Word.word.in_(splited_string)).all()
        for res in results:
            if res.word_type.type_name not in word_in_db.keys():
                word_in_db[res.word_type.type_name] = list()
            word_in_db[res.word_type.type_name].append(res.word)
        return word_in_db

    def _parser_launcher(self, parser):
        """
        launch a parser
        :param parser: parser class
        :return: a list
        """
        return parser(self.in_string, self.database_extract).out_list

    def _paralize_parsing(self):
        parsers_output = []
        for parser, weight in self.parsers:
            partial_result = self._parser_launcher(parser)
            parsers_output.append((partial_result, weight))
        return parsers_output

    def _compile_results(self):
        """
        count number of times a word appear in list
        multiply with parser weight and position index
        higher score is better
        :return:
        """
        tmp_dict = dict()
        results = []
        for partial_result in self._paralize_parsing():
            for i, value in enumerate(partial_result[0]):

                if value in tmp_dict.keys():
                    tmp_dict[value] *= (i + 1) * partial_result[1]
                else:
                    tmp_dict[value] = (i + 1) * partial_result[1]
        tmp_dict = OrderedDict(sorted(tmp_dict.items(), key=lambda x: x[1], reverse=True))
        LOGGER.debug(" words grades: %s", tmp_dict)
        if len(tmp_dict):
            grade_average = sum([value for value in tmp_dict.values()]) / len(tmp_dict)
            results = [key for key, value in tmp_dict.items() if value >= grade_average]
            LOGGER.debug(" %s", results)

        return results

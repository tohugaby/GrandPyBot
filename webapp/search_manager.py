"""
module to manage all actions to do when a search is done
"""
from webapp.api_connectors.controller import ApiController
from webapp.parser.controller import ParsingController


class SearchConductor:
    """
    Conducts all action between search parsing, api calls and return of json response
    """

    def __init__(self, in_string, parsing_controller=ParsingController, api_controller=ApiController):
        self.in_string = in_string
        self.parsing_controller = parsing_controller
        self.api_controller = api_controller

    def _parse_string(self):
        return self.parsing_controller(self.in_string).out_list

    def _call_all_api(self, searched_terms):
        if searched_terms:
            return self.api_controller(searched_terms[0]).get_results()
        return self.api_controller("").get_results()


    def make_full_search(self):
        parsed_string = self._parse_string()
        return self._call_all_api(parsed_string)

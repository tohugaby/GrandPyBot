"""
Module that contains all api connectors
"""
import logging

import requests

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

try:
    from api_keys import GOOGLE_MAP_API_KEY
except ImportError as import_error:
    LOGGER.error("""%s : You need API keys to use API Connectors !
    Create an api_keys.py module in project root and store your api keys""", import_error)


class ApiConnector(object):
    """
    Default class to represent element for calling an API
    """
    root_url = ""

    def __init__(self, search_term):
        self.search_term = search_term

    def search(self):
        """
        call api with search url
        :return: api response
        """
        response = requests.get(self.get_search_url())
        return response.json()

    def get_search_url(self):
        """
        Use search term, api key and other parameters to construct search url
        :return: search url
        """
        return self.root_url


class GoogleMapsApiConnector(ApiConnector):
    """
    Google Maps Api connector
    """
    root_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s"

    def search(self):
        """
        call api with search url
        :return: api json response
        """
        LOGGER.info(" Getting Google maps data for %s", self.search_term)
        return super(GoogleMapsApiConnector, self).search()

    def get_search_url(self):
        """
        Use search term, api key and other parameters to construct search url
        :return: search url
        """
        return self.root_url % (self.search_term, GOOGLE_MAP_API_KEY)

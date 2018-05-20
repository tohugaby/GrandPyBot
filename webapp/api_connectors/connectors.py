"""
Module that contains all api connectors
"""
import logging

import requests
from bs4 import BeautifulSoup

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

    def get_search_url(self, **kwargs):
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
        response = super(GoogleMapsApiConnector, self).search()
        new_response = {
            "formatted_address": response["results"][0]["formatted_address"],
            "location": response["results"][0]["geometry"]["location"]
        }
        return new_response

    def get_search_url(self, **kwargs):
        """
        Use search term, api key and other parameters to construct search url
        :return: search url
        """
        return self.root_url % (self.search_term, GOOGLE_MAP_API_KEY)


class WikipediaApiConnector(ApiConnector):
    """
    Wikipedia Api Connector
    """
    opensearch_url = "https://fr.wikipedia.org/w/api.php?action=opensearch&search=%s&format=json"
    root_url = "https://fr.wikipedia.org/w/api.php?action=query&titles=%s&prop=extracts&format=json"

    def get_search_url(self, **kwargs):
        """
        Use search term and root url to get first search url
        :return: search url
        """
        if "query_term" in kwargs:
            return self.root_url % kwargs["query_term"]
        else:
            return self.opensearch_url % self.search_term

    def _opensearch(self):
        """
        launch opensearch on wikipedia api to get the best query term to get a pertinent result
        :return: a new search term
        """
        LOGGER.info("Launch opensearch of %s in wikipedia api", self.search_term)
        result = requests.get(self.get_search_url()).json()
        return result[1][0], result[3][0]

    def search(self):
        """
        launch query on wikipedia api
        :return: query result as a dict
        """

        query_term, article_url = self._opensearch()
        LOGGER.info("Launch query of %s in wikipedia api", query_term)
        response = requests.get(self.get_search_url(query_term=query_term)).json()
        pages = response['query']['pages']
        page = [p for p in pages.keys()][0]
        soup = BeautifulSoup(pages[page]['extract'], "html.parser")
        description = [p for p in soup.find_all("p")][0]

        new_response = {
            "title": pages[page]['title'],
            "description": str(description),
            "url": str(article_url)
        }
        return new_response

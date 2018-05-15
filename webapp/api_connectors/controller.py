"""
module to manage api connectors
"""
from webapp.api_connectors.connectors import GoogleMapsApiConnector, WikipediaApiConnector


class ApiController:
    api_list = [
        (GoogleMapsApiConnector, "google_maps_api_results"),
        (WikipediaApiConnector, "wikipedia_api_results")
    ]

    def __init__(self, search_term):
        self.search_term = search_term

    def get_results(self):
        results = dict()
        for connector in self.api_list:
            results[connector[1]] = connector[0](self.search_term).search()

        print(results)
        return results

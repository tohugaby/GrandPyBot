"""
module to test search conductor
"""
import json
import requests_mock
from flask_testing import TestCase

from api_keys import GOOGLE_MAP_API_KEY
from webapp import app
from webapp.models import db
from webapp.word_files_handler.initial_data_handlers import FiletoDbHandler
from webapp.search_manager import SearchConductor


class TestSearchConductor(TestCase):
    def create_app(self):
        app.config.from_object("config.TestConfig")
        return app

    def setUp(self):
        self.in_string = "Salut GrandPy ! Est-ce que tu connais l'adresse d'Openclassrooms à Paris ?"
        db.create_all()
        for key in app.config["DATA_LOAD_CONFIG"].keys():
            FiletoDbHandler(db, key)()
        self.parsing_results = ['Openclassrooms', 'Paris']
        search_term = 'Openclassrooms'
        self.google_map_api_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (
            search_term, GOOGLE_MAP_API_KEY)
        self.wikipedia_api_opensearch_url = "https://fr.wikipedia.org/w/api.php?action=opensearch&search=%s&format=json" % search_term
        self.wikipedia_api_query_url = "https://fr.wikipedia.org/w/api.php?action=query&titles=%s&prop=extracts&format=json" % search_term
        self.google_map_api_results = [
            {
                'results': [
                    {
                        'formatted_address': '7 Cité Paradis, 75010 Paris, France',
                        'geometry': {
                            'location': {
                                'lat': 48.8747578, 'lng': 2.350564700000001
                            },
                            'location_type': 'ROOFTOP',
                            'viewport': {
                                'northeast': {
                                    'lat': 48.87610678029149, 'lng': 2.351913680291502
                                },
                                'southwest': {
                                    'lat': 48.87340881970849, 'lng': 2.349215719708499
                                }
                            }
                        },
                        'place_id': 'ChIJIZX8lhRu5kcRGwYk8Ce3Vc8',
                        'types': [
                            'establishment',
                            'point_of_interest'
                        ]
                    }
                ],
                'status': 'OK'
            }
        ]

        self.wikipedia_api_opensearch_results = ["OpenClassrooms", ["OpenClassrooms"],
                                                 ["OpenClassrooms est une école en ligne"],
                                                 ["https://fr.wikipedia.org/wiki/OpenClassrooms"]]

        self.wikipedia_api_query_results = {
            'pages': {
                '4338589': {
                    'pageid': 4338589,
                    'ns': 0,
                    'title': 'OpenClassrooms',
                    'extract': '<p><b>OpenClassrooms</b> est une école en ligne...</p>'
                }
            }
        }

        self.json_results = {
            'google_maps_api_results': [
                {
                    'results': [
                        {
                            'formatted_address': '7 Cité Paradis, 75010 Paris, France',
                            'geometry': {
                                'location': {
                                    'lat': 48.8747578,
                                    'lng': 2.350564700000001
                                },
                                'location_type': 'ROOFTOP',
                                'viewport': {
                                    'northeast': {
                                        'lat': 48.87610678029149,
                                        'lng': 2.351913680291502
                                    },
                                    'southwest': {
                                        'lat': 48.87340881970849,
                                        'lng': 2.349215719708499
                                    }
                                }
                            },
                            'place_id': 'ChIJIZX8lhRu5kcRGwYk8Ce3Vc8',
                            'types': ['establishment', 'point_of_interest']}],
                    'status': 'OK'}
            ],
            'wikipedia_api_results': {
                'pages': {
                    '4338589': {
                        'pageid': 4338589,
                        'ns': 0,
                        'title': 'OpenClassrooms',
                        'extract': '<p><b>OpenClassrooms</b> est une école en ligne...</p>'
                    }
                }
            }
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_parsing_results(self):
        search_conductor = SearchConductor(self.in_string)
        self.assertEqual(search_conductor.in_string, self.in_string)
        self.assertEqual(search_conductor._parse_string(), self.parsing_results)

    @requests_mock.Mocker(kw="mock")
    def test_get_json_results(self, **kwargs):
        search_conductor = SearchConductor(self.in_string)

        kwargs["mock"].get(self.google_map_api_url, text=json.dumps(self.google_map_api_results))
        kwargs["mock"].get(self.wikipedia_api_opensearch_url, text=json.dumps(self.wikipedia_api_opensearch_results))
        kwargs["mock"].get(self.wikipedia_api_query_url, text=json.dumps(self.wikipedia_api_query_results))

        api_results = search_conductor._call_all_api(self.parsing_results)
        self.assertIn("google_maps_api_results", api_results.keys())
        self.assertIn("wikipedia_api_results", api_results.keys())
        self.assertEqual(api_results, self.json_results)

    @requests_mock.Mocker(kw="mock")
    def test_make_full_search(self, **kwargs):
        search_conductor = SearchConductor(self.in_string)

        kwargs["mock"].get(self.google_map_api_url, text=json.dumps(self.google_map_api_results))
        kwargs["mock"].get(self.wikipedia_api_opensearch_url, text=json.dumps(self.wikipedia_api_opensearch_results))
        kwargs["mock"].get(self.wikipedia_api_query_url, text=json.dumps(self.wikipedia_api_query_results))

        full_search_result = search_conductor.make_full_search()
        self.assertIn("google_maps_api_results", full_search_result.keys())
        self.assertIn("wikipedia_api_results", full_search_result.keys())
        self.assertEqual(full_search_result, self.json_results)

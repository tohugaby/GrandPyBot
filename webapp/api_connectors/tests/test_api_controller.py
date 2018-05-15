"""
module to test api controller
"""
import json
import requests_mock

from api_keys import GOOGLE_MAP_API_KEY
from webapp.api_connectors.controller import ApiController


@requests_mock.Mocker(kw="mock")
def test_api_controller(**kwargs):
    search_term = "OpenClassrooms"
    google_map_api_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (
        search_term, GOOGLE_MAP_API_KEY)
    wikipedia_api_opensearch_url = "https://fr.wikipedia.org/w/api.php?action=opensearch&search=%s&format=json" % search_term
    wikipedia_api_query_url = "https://fr.wikipedia.org/w/api.php?action=query&titles=%s&prop=extracts&format=json" % search_term
    google_map_api_results = [
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

    wikipedia_api_opensearch_results = ["OpenClassrooms", ["OpenClassrooms"],
                                        ["OpenClassrooms est une école en ligne"],
                                        ["https://fr.wikipedia.org/wiki/OpenClassrooms"]]

    wikipedia_api_query_results = {
        'pages': {
            '4338589': {
                'pageid': 4338589,
                'ns': 0,
                'title': 'OpenClassrooms',
                'extract': '<p><b>OpenClassrooms</b> est une école en ligne...</p>'
            }
        }
    }

    kwargs["mock"].get(google_map_api_url, text=json.dumps(google_map_api_results))
    kwargs["mock"].get(wikipedia_api_opensearch_url, text=json.dumps(wikipedia_api_opensearch_results))
    kwargs["mock"].get(wikipedia_api_query_url, text=json.dumps(wikipedia_api_query_results))

    results = ApiController(search_term).get_results()
    assert isinstance(results, dict)
    assert "google_maps_api_results" in results.keys()
    assert "wikipedia_api_results" in results.keys()

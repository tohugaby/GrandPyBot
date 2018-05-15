"""
tests for api connectors
"""
import json
import requests_mock

from webapp.api_connectors.connectors import GoogleMapsApiConnector


@requests_mock.Mocker(kw='mock')
def test_google_api_return(**kwargs):
    """
    mock to test google maps api connector
    :param kwargs: contains mock instance among others kwargs
    :return:
    """
    search_term = "OpenClassrooms"
    api_connector_instance = GoogleMapsApiConnector(search_term)
    search_url = api_connector_instance.get_search_url()
    results = [
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

    kwargs["mock"].get(search_url, text=json.dumps(results))
    fake_results = api_connector_instance.search()
    assert fake_results == results
    assert isinstance(fake_results, list)

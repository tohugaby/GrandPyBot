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
    api_results = {'results': [
        {
            'address_components': [
                {
                    'long_name': '7',
                    'short_name': '7',
                    'types': ['street_number']
                },
                {
                    'long_name': 'Cité Paradis',
                    'short_name': 'Cité Paradis',
                    'types': ['route']
                },
                {
                    'long_name': 'Paris',
                    'short_name': 'Paris',
                    'types': ['locality', 'political']
                },
                {
                    'long_name': 'Paris',
                    'short_name': 'Paris',
                    'types': ['administrative_area_level_2', 'political']
                },
                {
                    'long_name': 'Île-de-France',
                    'short_name': 'Île-de-France',
                    'types': ['administrative_area_level_1', 'political']
                },
                {
                    'long_name': 'France',
                    'short_name': 'FR',
                    'types': ['country', 'political']
                },
                {
                    'long_name': '75010',
                    'short_name': '75010',
                    'types': ['postal_code']
                }
            ],
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
            'types': ['establishment', 'point_of_interest']
        }
    ],
        'status': 'OK'
    }

    method_call_results = {'formatted_address': '7 Cité Paradis, 75010 Paris, France',
                           'location': {'lat': 48.8747578, 'lng': 2.350564700000001}}

    kwargs["mock"].get(search_url, text=json.dumps(api_results))
    fake_results = api_connector_instance.search()
    assert fake_results == method_call_results
    assert isinstance(fake_results, dict)


@requests_mock.Mocker(kw='mock')
def test_google_api_not_found_return(**kwargs):
    """
    mock to test google maps api connector
    :param kwargs: contains mock instance among others kwargs
    :return:
    """
    search_term = "stgsdfhrjdrfhdgcshrtjuetrfdrth"
    api_connector_instance = GoogleMapsApiConnector(search_term)
    search_url = api_connector_instance.get_search_url()
    api_results = {'results': [],
                   'status': 'ZERO_RESULTS'
                   }

    method_call_results = {
        "formatted_address": "",
        "location": {
            "lat": 0,
            "lng": 0
        }
    }

    kwargs["mock"].get(search_url, text=json.dumps(api_results))
    fake_results = api_connector_instance.search()
    assert fake_results == method_call_results
    assert isinstance(fake_results, dict)

"""
tests for wikipedia api connector
"""
import json
import requests_mock

from webapp.api_connectors.connectors import WikipediaApiConnector


@requests_mock.Mocker(kw="mock")
def test_wikipedia_api_return(**kwargs):
    """
    mock to test wikipedia api connector return
    :param kwargs: contains mock instance among others kwargs
    :return:
    """
    search_term = "OpenClassrooms"
    api_connector_instance = WikipediaApiConnector(search_term)
    opensearch_url = api_connector_instance.get_search_url()
    search_url = api_connector_instance.get_search_url(query_term="OpenClassrooms")
    opensearch_results = ["OpenClassrooms", ["OpenClassrooms"], ["OpenClassrooms est une école en ligne"],
                          ["https://fr.wikipedia.org/wiki/OpenClassrooms"]]
    query_results = {
        'pages': {
            '4338589': {
                'pageid': 4338589,
                'ns': 0,
                'title': 'OpenClassrooms',
                'extract': '<p><b>OpenClassrooms</b> est une école en ligne...</p>'
            }
        }
    }

    kwargs["mock"].get(opensearch_url, text=json.dumps(opensearch_results))
    kwargs["mock"].get(search_url, text=json.dumps(query_results))
    fake_results = api_connector_instance.search()
    assert fake_results == query_results
    assert isinstance(fake_results, dict)

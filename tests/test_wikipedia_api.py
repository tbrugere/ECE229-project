''' This file tests the functions in predction.py
To generate a html coverage report, run
pytest --cov-report html:cov_html
        --cov=carsreco'''
import pytest
from carsreco import wikipedia_api as wiki

def test_make_wikimedia_request_bad_request(requests_mock):
    """test api call raises error when status code is not 200
    """   
    with pytest.raises(AssertionError):
        requests_mock.get('http://test.com', status_code=404)
        resp = wiki.make_wikimedia_request(api_url='http://test.com')

def test_wikipedia_query_search(requests_mock):
    """ test response is read properly
    """   
    requests_mock.get('https://en.wikipedia.org/w/api.php', json= {'query': {"searchinfo": {"totalhits" : 10 }, "search": "abc"}})
    assert wiki.wikipedia_query_search('q') == 'abc'
    

def test_wikipedia_query_firstpage(requests_mock):
    """ test if only first result is returned
    """    
    requests_mock.get('https://en.wikipedia.org/w/api.php', json= {'query': {"searchinfo": {"totalhits" : 10 }, "search": ["abc", "def"]}})
    r = wiki.wikipedia_query_firstpage('q')
    assert r == 'abc'

def test_wikipediapage_class_methods(requests_mock):
    requests_mock.get('https://en.wikipedia.org/w/api.php', json= {'query': {"searchinfo": {"totalhits" : 10 }, "pages": {"original": {}}, 
                        "search": [{"title":"abc", "pageid":1, "ns":100, "size": 24, "wordcount": 50, "snippet": 'test', "timestamp": '06/06/2021'}]}})
    page = wiki.WikipediaPage.from_query('q')
    assert page.title == "abc"
    # when there is no image, return None and don't display thumbnail
    assert page.get_thumbnail() is None
    assert page.get_quicktext() is None

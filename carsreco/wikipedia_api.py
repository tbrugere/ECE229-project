"""Get images and descriptions of things from wikipedia
"""

from typing import Optional

from dataclasses import dataclass, field
from datetime import datetime
import dateutil

import requests

def make_wikimedia_request(api_url="https://en.wikipedia.org/w/api.php", **parameters):
    """make a request to wikimedia api

    Uses the requests library to make a post request to the wikimedia api with sensible defaults

    Args:
        api_url: the url of the api. The default is to use wikipedia
        parameters: keword args passed to the wikimedia api

    Returns:
        the deserialized json response to the request
    """
    r =  requests.get(api_url, params = dict(format="json", **parameters))
    assert r.status_code == 200, "Bad request made to wikipedia"
    return r.json()

def wikipedia_query_search(query, **parameters):
    """searches on wikipedia

    uses the query api call to perform a fuzzy search for a page on wikipedia

    Args:
        query: a string query which will be used to perform the search
        parameters: additional parameters to pass to the api
    """
    r = make_wikimedia_request(
        action="query", 
        list="search",
        srsearch=query,
        redirects=1,
        #redirect=1,
        **parameters
        )
    #display(d)
    result = r["query"]
    if result["searchinfo"]["totalhits"] == 0:
        return None 
    return result["search"]

def wikipedia_query_firstpage(query, **parameters):
    """returns the first result from wikipedia

    uses the query api call to perform a fuzzy search for a page on wikipedia, and
    returns the first result

    You should not use this function but the :func:`WikipediaPage.from_query` constructor instead.

    Args:
        query: a string query which will be used to perform the search
        parameters: additional parameters to pass to the api
    """
    r = wikipedia_query_search(query, **parameters)
    return r[0] if r is not None else r


@dataclass
class WikipediaPage():
    """class representing a wikipedia page
    
    The result of searching for a page on wikipedia and taking the first result
    
    Attributes:
        ns: the namespace of the page (see `wikipedia namespaces`_ )
        title: the title of the page
        size: the size of the page
        wordcount: the number of words on the page
        snippet: a piece of text from the page (not necessarily the beginning, for this see :func:`get_quicktext`)
        timestamp: the time the page was last edited


    .. _wikipedia namespaces: https://en.wikipedia.org/wiki/Wikipedia:Namespace
    """
    ns: int
    title: str
    pageid: int
    size: int
    wordcount: int
    snippet: str = field(repr=False)
    timestamp: datetime
        
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = dateutil.parser.parse(self.timestamp)

    @classmethod
    def from_query(cls, q:str) -> Optional["WikipediaPage"]:
        """search on wikipedia

        generates a WikipediaPage object from a query string by using fuzzy searching
        in wikipedia

        Args:
            q: the query string

        Returns:
            a WikipediaPage object
        """
        r = wikipedia_query_firstpage(q)
        if r is None:
            return None
        return cls(**r)
    
   
    def get_thumbnail(self) -> Optional[dict]:
        """get the page thumbnail
        
        get the main image of the page (thumbnail)

        Returns:
            None if there is no such image. Otherwise a dictionary::
                {"source":  the url of the image
                  "width": the width of the image
                  "height": the height of the image}
        """
        r = make_wikimedia_request(action="query", 
                                   prop="pageimages", 
                                   piprop="original", 
                                   pageids=self.pageid,
                                  pilicense="free")
        pages = r["query"]["pages"]
        _, onlypage = pages.popitem()
        file = onlypage.get("original", None)
        return file
    
    def display_thumbnail(self):
        """Displays the thumbnail in a jupyter notebook

        used for hand-testing, needs to run in a jupyter notebook. Displays the image returned
        by :func:`get_thumbnail`

        will do nothing if there is no thumbnail to display
        """
        from Ipython.display import display, Image
        thumbnail = self.get_thumbnail()
        if thumbnail is None:
            return
        display(Image(thumbnail["source"]))
        
    def get_quicktext(self) -> str:
        """get the page quickstext

        Returns:
            the first paragraphs of the page, in HTML format
        """
        r = make_wikimedia_request(action="query", 
                           prop="extracts",
                            exintro="true", 
                           pageids=self.pageid,
                          pilicense="free")
        pages = r["query"]["pages"]
        _, onlypage = pages.popitem()
        extract = onlypage.get("extract", None)

        return extract

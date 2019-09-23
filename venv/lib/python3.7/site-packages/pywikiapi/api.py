from . import AttrDict
from . import Site


def wikipedia(language='en', site='wikipedia', scheme='https', **kwargs):
    """
    Create a Site object for Wikipedia or one of the sister sites, using the URL
        [scheme]://[language].[site].org/w/api.php

    All API results are wrapped with AttrDict helper, simplifying property access:
    response.allpages[0].title  instead of  response['allpages'][0]['title']

    See Site object for the parameter documentation
    """
    url = scheme + '://' + language + '.' + site + '.org/w/api.php'
    return Site(url, json_object_hook=AttrDict, **kwargs)

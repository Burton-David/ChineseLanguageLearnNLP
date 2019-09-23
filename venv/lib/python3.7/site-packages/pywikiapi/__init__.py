"""Minimalistic MediaWiki API library by the author of the MediaWiki API itself.  See README.md"""

from pywikiapi.utils import ApiError, ApiPagesModifiedError, AttrDict, to_datetime, to_timestamp
from pywikiapi.Site import Site
from pywikiapi.api import wikipedia

__version__ = "3.1.0"

import logging
import time
from typing import Union, Tuple
import json
import os
import sys
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime

from .utils import ApiError, ApiPagesModifiedError

PY3 = sys.version_info[0] == 3
if PY3:
    string_types = str,
    unicode = str
else:
    # noinspection PyUnresolvedReferences
    string_types = basestring,

try:
    import urllib.parse as urlparse
except ImportError:
    # noinspection PyUnresolvedReferences
    import urlparse


class Site:
    """
    This object represents a MediaWiki API endpoint, e.g. https://en.wikipedia.org/w/api.php
    * url: Full url to site's api.php
    * session: current request.session object
    * log: an object that will be used for logging. ConsoleLog is created by default
    """

    def __init__(self, url, headers=None, session=None, logger=None, json_object_hook=None):
        """
        Create a new Site object with a given MediaWiki API endpoint.
        You should always set a `User-Agent` header to identify your bot and allow
        site owner to contact you in case your bot misbehaves.
        By default, User-Agent is set to the dir name + script name of your bot.
        :param str url: API endpoint URL, e.g. https://en.wikipedia.org/w/api.php
        :param Union[dict, CaseInsensitiveDict] headers: Optional headers as a dictionary.
        :param requests.Session session: Allows user-supplied custom Session parameters, e.g. retries
        :param logging.Logger logger: Optional logger object for custom log output
        :param object json_object_hook: use this param to set a custom json object creator,
            e.g. pywikiapi.AttrDict. AttrDict allows direct property access to the result,
            e.g response.query.allpages in addition to response['query']['allpages']
        """
        if logger is None:
            self.logger = logging.getLogger('pywikiapi')
            self.logger.setLevel(logging.INFO)
        else:
            self.logger = logger

        self.json_object_hook = json_object_hook
        self.session = session if session else requests.Session()
        self.url = url
        self.tokens = {}
        self.no_ssl = False  # For non-ssl sites, might be needed to avoid HTTPS
        self.maxlag = 5  # See https://www.mediawiki.org/wiki/Manual:Maxlag_parameter
        self.auto_post_min_size = 2000  # If request is bigger than this, use POST instead

        # Number of retries to do in case of the lag error. 0 - don't retry. negative - infinite.
        self.retry_on_lag_error = 10

        # This var will contain (username,password) after the .login() in case of the login-on-demand mode
        self._loginOnDemand = False  # type: Union[Tuple[unicode, unicode], bool]
        self.logged_in = False

        self.headers = CaseInsensitiveDict()
        if headers:
            self.headers.update(headers)
        if u'User-Agent' not in self.headers:
            try:
                script = os.path.abspath(sys.modules['__main__'].__file__)
            except (KeyError, AttributeError):
                script = sys.executable
            path, f = os.path.split(script)
            self.headers[u'User-Agent'] = u'%s-%s pywikiapi/0.1' % (os.path.basename(path), f)

    def __call__(self, action, **kwargs):
        """
            Make an API call with any arguments provided as named values:

                data = site('query', meta='siteinfo')

            By default uses GET request to the default URL set in the Site constructor.
            In case of an error, ApiError exception will be raised
            Any warnings will be logged via the logging interface

            :param unicode action : any of the MW API actions, e.g. 'query' and 'login'

            Several special "magic" parameters could be used to customize api call.
            Special parameters must be all CAPS to avoid collisions with the server API:
            :param POST: Use POST method when calling server API. Value is ignored.
            :param HTTPS: Force https (ssl) protocol for this request. Value is ignored.
            :param SSL: Same as HTTPS
            :param EXTRAS: Any extra parameters as passed to requests' session.request(). Value is a dict()
        """
        method, request_kw = self._prepare_call(action, kwargs)

        if self._loginOnDemand and action != 'login':
            self.login(self._loginOnDemand[0], self._loginOnDemand[1])

        try_count = 0
        while True:
            try_count += 1
            response = self.request(method, **request_kw)
            data = self.parse_json(response)
            if 0 <= self.retry_on_lag_error < try_count:
                break
            try:
                if data['error']['code'] != 'maxlag':
                    break
                retry_after = float(response.headers.get('Retry-After', 5))
                # X-Database-Lag: The number of seconds of lag of the most lagged slave
                self.logger.info('maxlag-retry', {
                    'retry-after': retry_after,
                    'lag': data['error']['lag'] if 'lag' in data['error'] else None,
                    'x-database-lag': response.headers.get('X-Database-Lag', 5)
                })
                time.sleep(retry_after)
            except KeyError:
                break

        # Handle success and failure
        if 'error' in data:
            raise ApiError('Server API Error', data['error'])
        if 'warnings' in data:
            self.logger.warning('server-warnings', {'warnings': data['warnings']})
        return data

    def _prepare_call(self, action, kwargs):
        """
        Prepares parameters before calling MW API
        :param unicode action: which MW API action to do
        :param dict kwargs: key-value parameters as passed to the self.__call__()
        :return:
        """
        # Magic CAPS parameters
        method = 'POST' if 'POST' in kwargs or action in ['login', 'edit'] else 'GET'
        request_kw = dict() if 'EXTRAS' not in kwargs else kwargs['EXTRAS']
        request_kw['force_ssl'] = not self.no_ssl and (action == 'login' or 'SSL' in kwargs or 'HTTPS' in kwargs)
        # Clean up magic CAPS params as they shouldn't be passed to the server
        for k in ['POST', 'SSL', 'HTTPS', 'EXTRAS']:
            if k in kwargs:
                del kwargs[k]

        def update_value(value):
            if value is None:
                return None
            if isinstance(value, datetime):
                # .isoformat() wouldn't work because it sometimes produces +00:00 that MW does not support
                # Also perform sanity check here to make sure this is a UTC time
                if value.tzinfo is not None and value.tzinfo.utcoffset(value):
                    raise ValueError('datetime value has a non-UTC timezone')
                return value.strftime('%Y-%m-%dT%H:%M:%SZ')
            if isinstance(value, bool):
                return '1' if value else None
            return unicode(value)

        for k, val in list(kwargs.items()):
            # Only support the well known types.
            # Everything else should be client's responsibility
            if isinstance(val, list) or isinstance(val, tuple) or isinstance(val, set):
                val = [update_value(v) for v in val]
                kwargs[k] = u'|'.join(filter(lambda v: v is not None, val))
            else:
                val = update_value(val)
                if val is not None:
                    kwargs[k] = val
                else:
                    del kwargs[k]
        # Make server call
        kwargs['action'] = action
        kwargs['format'] = 'json'
        if 'formatversion' not in kwargs:
            kwargs['formatversion'] = 2
        if self.maxlag is not None and 'maxlag' not in kwargs:
            kwargs['maxlag'] = self.maxlag
        if sum(len(str(k)) + len(str(v)) + 2 for k, v in kwargs.items()) > self.auto_post_min_size:
            method = 'POST'

        if method == 'POST':
            request_kw['data'] = kwargs
        else:
            request_kw['params'] = kwargs

        return method, request_kw

    def login(self, user, password, on_demand=False):
        """
        :param str user: user login name
        :param str password: user password
        :param bool on_demand: if True, will postpone login until an actual API request is made
        """
        self.tokens = {}
        if on_demand:
            self._loginOnDemand = (user, password)
            return
        res = self('login', lgname=user, lgpassword=password)['login']
        if res['result'] == 'NeedToken':
            res = self('login', lgname=user, lgpassword=password, lgtoken=res['token'])['login']
        if res['result'] != 'Success':
            raise ApiError('Login failed', res)
        self._loginOnDemand = False
        self.logged_in = True

    def query(self, **kwargs):
        """
        Call Query API with given parameters, and yield all results returned
        by the server, properly handling result continuation.
        """
        return self.iterate('query', **kwargs)

    def iterate(self, action, **kwargs):
        """
        Call any "continuation" style MW API with given parameters, such as the 'query' API.
        Yields all results returned by the server, properly handling result continuation.
        Use generator.send({...}) to dynamically adjust next request's parameters with the new parameters.
        :param str action: MW API action, e.g. 'query'
        :param kwargs: any API parameters
        :return: yields each response from the server
        """
        if 'rawcontinue' in kwargs:
            raise ValueError("rawcontinue is not supported with query() function, use object's __call__()")
        if 'formatversion' in kwargs:
            raise ValueError("version is not supported with query() function, use object's __call__()")
        if 'continue' not in kwargs:
            kwargs['continue'] = ''
        req = kwargs
        req['formatversion'] = 2
        while True:
            result = self(action, **req)
            if action in result:
                adjustments = yield result[action]
            else:
                adjustments = None
            if 'continue' not in result:
                break
            # re-send all continue values in the next call
            req = kwargs.copy()
            req.update(result['continue'])
            if adjustments:
                req.update(adjustments)

    def query_pages(self, **kwargs):
        """
        Query the server and yield all page objects one by one.
        This method makes sure that results received in multiple responses are
        correctly merged together.
        If any of the pages change during iteration, ApiPagesModifiedError(list) will be thrown
        after all other pages have been processed and yielded.
        """
        incomplete = {}  # A dict with incomplete page objects
        modified = set()  # A set of page ids that we will ignore because they have been modified during iteration
        missing = set()
        for result in self.query(**kwargs):
            if 'pages' not in result:
                raise ApiError('Missing pages element in query result', result)

            new_incomplete = {}
            for page in result['pages']:
                if 'missing' in page:
                    if page['title'] not in missing:
                        yield page
                        missing.add(page['title'])
                    continue
                page_id = page['pageid']
                if page_id in modified:
                    continue
                if page_id in incomplete:
                    p = incomplete[page_id]
                    del incomplete[page_id]
                    if 'lastrevid' in page and p['lastrevid'] != page['lastrevid']:
                        # someone else modified this page, it must be requested separately in a new query
                        modified.add(page_id)
                        continue
                    # Merge additional page data into the same dict
                    self._merge_page(p, page)
                else:
                    p = page
                new_incomplete[page_id] = p

            # Yield all pages that have not been mentioned in the last response
            for page_id, page in incomplete.items():
                yield page

            incomplete = new_incomplete

        # Iteration is done, all incomplete are thus complete
        for page_id, page in incomplete.items():
            yield page

        if modified:
            # some pages have been modified between api calls, notify caller
            raise ApiPagesModifiedError(list(modified))

    def _merge_page(self, a, b):
        """
        Recursively merge two page objects
        """
        for k in b:
            val = b[k]
            if k in a:
                if isinstance(val, dict):
                    self._merge_page(a[k], val)
                elif isinstance(val, list):
                    a[k] = a[k] + val
                else:
                    a[k] = val
            else:
                a[k] = val

    def token(self, token_type='csrf'):
        """
        Get an api token.
        :param str token_type:
        :return: str
        """
        if token_type not in self.tokens:
            self.tokens[token_type] = next(self.query(meta='tokens', type=token_type))['tokens'][token_type + 'token']
        return self.tokens[token_type]

    def request(self, method, force_ssl=False, headers=None, **request_kw):
        """Make a low level request to the server"""
        url = self.url
        if force_ssl:
            parts = list(urlparse.urlparse(url))
            parts[0] = 'https'
            url = urlparse.urlunparse(parts)
        if headers:
            h = self.headers.copy()
            h.update(headers)
            headers = h
        else:
            headers = self.headers

        r = self.session.request(method, url, headers=headers, **request_kw)
        if not r.ok:
            raise ApiError('Call failed', r)
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('server-response', {'url': r.request.url, 'headers': headers})
        return r

    def parse_json(self, value):
        """
        Utility function to convert server reply into a JSON object.
        By default, JSON objects support direct property access (JavaScript style)
        """
        if isinstance(value, string_types):
            return json.loads(value, object_hook=self.json_object_hook)
        elif hasattr(value.__class__, 'json'):
            return value.json(object_hook=self.json_object_hook)
        else:
            # Our servers still have requests 0.8.2 ... :(
            return json.loads(value.content, object_hook=self.json_object_hook)

    def __str__(self):
        res = self.url
        if self.logged_in:
            res += ' (logged in)'
        return res

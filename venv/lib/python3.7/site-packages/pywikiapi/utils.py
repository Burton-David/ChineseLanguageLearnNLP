import json
from datetime import datetime


class ApiError(Exception):
    """
    Any error reported by the API is included in this exception
    """

    def __init__(self, message, data):
        self.message = message
        self.data = data

    def __str__(self):
        return self.message + ': ' + json.dumps(self.data)


class ApiPagesModifiedError(ApiError):
    """
    This error is thrown by queryPage() if revision of some pages was changed between calls.
    """

    def __init__(self, data):
        super(ApiError, self).__init__('Pages modified during iteration', data)


class AttrDict(dict):
    """
    Taken from http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python/25320214
    But it seems we should at some point switch to https://pypi.python.org/pypi/attrdict
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def to_timestamp(value):
    """
    Convert datetime to a timestamp string MediaWiki would understand.
    :type value: datetime
    :rtype str
    """
    # datetime.isoformat() wouldn't work because it sometimes produces +00:00 that MW does not support
    # Also perform sanity check here to make sure this is a UTC time
    if value.tzinfo is not None and value.tzinfo.utcoffset(value):
        raise ValueError('datetime value has a non-UTC timezone')
    return value.strftime('%Y-%m-%dT%H:%M:%SZ')


def to_datetime(timestamp):
    """
    Convert MediaWiki timestamp to a datetime object.
    Assumes the format to be in "MW" ISO with "Z" instead of +00:00 for timezone.
    :type timestamp: str
    :rtype datetime
    """
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

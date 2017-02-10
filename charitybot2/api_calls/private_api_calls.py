import json

from charitybot2.private_api.private_api import private_api_full_url
from charitybot2.sources.url_call import UrlCall


class PrivateApiCalls:
    v1_url = private_api_full_url + 'api/v1/'

    def __init__(self, timeout=2):
        self._timeout = timeout

    def get_index(self):
        return json.loads(UrlCall(url=self.v1_url, timeout=self._timeout).get().content.decode('utf-8'))

    def get_event_existence(self, identifier):
        url = self.v1_url + 'event/{}/'.format(identifier)
        return json.loads(UrlCall(url=url, timeout=self._timeout).get().content.decode('utf-8'))['event_exists']

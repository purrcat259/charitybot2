import json

from charitybot2.models.donation import Donation
from charitybot2.sources.url_call import UrlCall


class DonationsApiWrapper:
    def __init__(self, base_url, timeout=2, maximum_retry_attempts=3):
        self._base_url = base_url + 'api/v1/'  # TODO: Use path resolving function instead of string concat
        self._timeout = timeout
        self._maximum_retry_attempts = maximum_retry_attempts

    def get_index(self):
        return json.loads(UrlCall(url=self._base_url, timeout=self._timeout).get().content.decode('utf-8'))

    def get_donations(self, event_identifier, lower_bound=None, upper_bound=None, limit=None):
        url = self._base_url + 'event/{}/donations/'.format(event_identifier)
        query_parameters = {
            'lower': lower_bound,
            'upper': upper_bound,
            'limit': limit
        }
        response = UrlCall(url=url, params=query_parameters, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)['donations']
        donations = [Donation.from_dict(donation) for donation in converted_content]
        return donations

    def get_latest_donation(self, event_identifier):
        return self.get_donations(event_identifier=event_identifier, limit=1)[0]

    def get_number_of_donations(self, event_identifier, lower_bound=None, upper_bound=None):
        url = self._base_url + 'event/{}/donations/count/'.format(event_identifier)
        query_parameters = {
            'lower': lower_bound,
            'upper': upper_bound
        }
        response = UrlCall(url=url, params=query_parameters, timeout=self._timeout).get()
        decoded_content = response.content.decode('utf-8')
        converted_content = json.loads(decoded_content)['count']
        return converted_content

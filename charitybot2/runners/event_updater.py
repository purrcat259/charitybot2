import time
from charitybot2.api.donations_api import full_url as donations_api_url
from charitybot2.api.events_api import full_url as events_api_url
from charitybot2.api_calls.donations_api_wrapper import DonationsApiWrapper
from charitybot2.api_calls.events_api_wrapper import EventsApiWrapper

donations_api_wrapper = DonationsApiWrapper(base_url=donations_api_url)
events_api_wrapper = EventsApiWrapper(base_url=events_api_url)

"""
An event updater does the following:
> Retrieve a set of events
> If they are upcoming events and 5 minutes have passed since the last check:
    > Update details (target amount, times, etc)
    > Update total raised
    > Update donations
    > Cache last seen donation ID   // donations service retrieval?
    > Log that the update has happened
> If they are ongoing events and 10 seconds have passed since the last check:
    > Update target amount, or all details if available
    > Update total raised
    > Update donations
    > Cache last seen donation ID  // donations service retrieval?
    > Log that the update has happened

A persistent update log should ideally be created, one with a schema similar to this:
event_identifier, time_of_last_update
Last seen donation ID can be retrieved from the donation service rather than locally cached
"""


class EventUpdater:
    def __init__(self, minimum_time_for_update_in_seconds, update_delay_in_seconds):
        self._minimum_time_for_update_in_seconds = minimum_time_for_update_in_seconds
        self._update_delay_in_seconds = update_delay_in_seconds

    # Run this method if running the event updater outside of a test environment
    def run(self):
        pass

    # This method must be overridden in the child objects, depending on whether it is for upcoming or ongoing events
    def retrieve_events(self):
        pass

    def event_needs_to_be_updated(self, event_identifier, time_last_checked):
        time_for_update = time_last_checked + self._minimum_time_for_update_in_seconds
        current_time = int(time.time())
        if current_time >= time_for_update:
            return True

    def get_event_update_details(self, event_identifier):
        pass

    def update_event_details(self, event_identifier):
        pass

    def update_event_donations(self, event_identifier):
        pass




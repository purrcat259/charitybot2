import random
import time
from faker import Faker

from charitybot2.creators.event_creator import EventRegister
from charitybot2.models.donation import Donation
from charitybot2.paths import test_repository_db_path
from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository
from charitybot2.persistence.event_sqlite_repository import EventSQLiteRepository
from tests.integration.test_event_register import get_test_event_configuration
from tests.mocks import WipeSQLiteDB


current_time = int(time.time())
# 2 hours long
start_time = current_time - 3600
end_time = current_time + 3600

updated_values = {
    'start_time': start_time,
    'end_time': end_time
}


def setup_test_database(event_values=None, donation_count=10, donation_amount=None):
    print('--- SETTING UP TEST DATABASE ---')
    wipe_database()
    if event_values is None:
        event_values = updated_values
    event_configuration = get_test_event_configuration(updated_values=event_values)
    register_event(event_configuration)
    register_donations(
        event_configuration=event_configuration,
        donation_count=donation_count,
        donation_amount=donation_amount)
    print('--- TEST DATABASE SETUP COMPLETE ---')


def wipe_database():
    print('Wiping old database')
    WipeSQLiteDB(db_path=test_repository_db_path).wipe_db()


def register_event(event_configuration):
    print('Registering event: {}'.format(event_configuration.identifier))
    event_repository = EventSQLiteRepository(db_path=test_repository_db_path)
    event_register = EventRegister(
        event_configuration=event_configuration,
        event_repository=event_repository)
    event_register.get_event()


def register_donations(event_configuration, donation_count, donation_amount):
    # TODO: Refactor this!
    randomise_donations = False
    if donation_amount is None:
        randomise_donations = True
    print('Recording donations')
    donations_repository = DonationSQLiteRepository(db_path=test_repository_db_path)
    shifting_time = start_time + 5
    fake = Faker()
    print('Adding {} donations'.format(donation_count))
    for i in range(0, donation_count):
        shifting_time += random.randint(5, 60)
        donor_name = fake.name()
        if randomise_donations:
            donation_amount = round(random.uniform(1.0, 100.0), 2)
        donation = Donation(
            amount=donation_amount,
            timestamp=shifting_time,
            event_identifier=event_configuration.identifier,
            external_reference='N/A',
            notes='N/A',
            donor_name=donor_name)
        donations_repository.record_donation(donation=donation)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        setup_test_database(donation_count=int(sys.argv[1]))
    else:
        setup_test_database()

import requests
from charitybot2.paths import external_api_path
from charitybot2.reporter.external_api import api_full_url
from flask import json
from tests.tests import TestFilePath, ServiceTest

donations_db_path = TestFilePath().get_db_path('donations.db')
donations_db_init_script_path = TestFilePath().get_db_path('donations.sql')

status_service = ServiceTest(
    service_name='External API',
    service_url=api_full_url,
    service_path=external_api_path,
    enter_debug=True,
    db_path=donations_db_path,
    sql_path=donations_db_init_script_path)


def setup_module():
    status_service.start_service()


def teardown_module():
    status_service.stop_service()


paths = ['events']


class TestGET:
    def test_index_route_returns_information_object(self):
        response = requests.get(api_full_url)
        content = json.loads(response.content)
        assert 200 == response.status_code
        assert isinstance(content['paths'], list)

    def test_information_object_contains_all_paths(self):
        response = requests.get(api_full_url)
        content = json.loads(response.content)
        assert sorted(paths) == sorted(content['paths'])


import unittest
import unittest.mock as mock

from historical.api import ApiRequestor
from requests import PreparedRequest


class TestApiConnectionPool(unittest.TestCase):

    def setUp(self):
        self.expected_url = 'https://bitcoincharts.com/charts/chart.json?m=coinbaseUSD&r=5&i=15-min&m1=10'

        self.request_exchange = 'coinbaseUSD'
        self.request_day = '5'
        self.request_interval = '15-min'

        self.request_method = 'GET'
        self.request_url = 'localhost:8080'
        self.request_headers = {}

    def tearDown(self):
        pass

    def test_api_connection_pool_creates_sess(self):
        api = ApiRequestor()
        self.assertIsNotNone(api.session)

    def test_generate_headers_exists(self):
        api = ApiRequestor()
        self.assertIsNotNone(api._generate_headers)

    def test_generate_headers_returns_same_object(self):
        api = ApiRequestor()
        self.assertEqual(api._generate_headers(), api._generate_headers())

    def test_generate_headers_returns_user_agent(self):
        api = ApiRequestor()
        self.assertIn('User-Agent', api._generate_headers())

    def test_generate_headers_returns_same_object_between_instances(self):
        api = ApiRequestor()
        api2 = ApiRequestor()
        self.assertEqual(
            api._generate_headers()['User-Agent'],
            api2._generate_headers()['User-Agent']
        )

    def test_prepare_request_exists(self):
        api = ApiRequestor()
        self.assertIsNotNone(api.prepare_request)

    def test_prepare_request_returns_preparedrequest_object(self):
        api = ApiRequestor()
        self.assertIsInstance(api.prepare_request(
            self.request_method,
            self.request_url,
            self.request_headers
        ), PreparedRequest)

    def test_generate_url_exists(self):
        api = ApiRequestor()
        self.assertIsNotNone(api.generate_url)

    def test_generate_url_returns_string(self):
        api = ApiRequestor()
        self.assertIsInstance(api.generate_url(
            self.request_exchange,
            self.request_day,
            self.request_interval
        ), str)

    def test_generate_url_returns_formatted_url(self):
        api = ApiRequestor()
        url = api.generate_url(
            self.request_exchange, self.request_day, self.request_interval)
        self.assertEqual(url, expected_url)

    def test_send_request_exists(self):
        api = ApiRequestor()
        self.assertIsNotNone(api.send_request)

    def test_send_request_calls_prepare_request(self):
        api = ApiRequestor()
        with mock.patch.object(api, 'prepare_request',
                               wraps=api.prepare_request) as monkey:
            api.send_request()
            monkey.assert_called()

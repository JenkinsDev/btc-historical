import unittest
import unittest.mock as mock

from historical.api import ApiRequestor, ApiResponse
from requests import PreparedRequest


def mocked_json_loads(*args, **kwargs):
    return args[0]


class TestApiRequestor(unittest.TestCase):

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
        self.assertEqual(url, self.expected_url)

    def test_send_request_exists(self):
        api = ApiRequestor()
        self.assertIsNotNone(api.send_request)


class TestApiResponse(unittest.TestCase):

    def setUp(self):
        self.request_code = 200
        self.request_status = 'status'
        self.request_data = 'request message'

    def tearDown(self):
        pass

    def test_has_code(self):
        api_response = ApiResponse(
            self.request_code,
            None,
            None
        )
        self.assertIsNotNone(api_response.code)
        self.assertEqual(api_response.code, self.request_code)

    def test_has_status(self):
        api_response = ApiResponse(
            self.request_code,
            self.request_status,
            None
        )
        self.assertIsNotNone(api_response.status)
        self.assertEqual(api_response.status, self.request_status)

    def test_has_message(self):
        api_response = ApiResponse(
            self.request_code,
            self.request_status,
            self.request_data
        )
        self.assertIsNotNone(api_response.data)
        self.assertEqual(api_response.data, self.request_data)

    def test_is_error_returns_true_if_not_200_code(self):
        api_response = ApiResponse(
            400,
            self.request_status,
            self.request_data
        )
        self.assertTrue(api_response.is_error())

        api_response2 = ApiResponse(
            200,
            self.request_status,
            self.request_data
        )
        self.assertFalse(api_response2.is_error())

    def test_is_success_returns_true_if_200_code(self):
        api_response = ApiResponse(
            400,
            self.request_status,
            self.request_data
        )
        self.assertFalse(api_response.is_success())

        api_response2 = ApiResponse(
            200,
            self.request_status,
            self.request_data
        )
        self.assertTrue(api_response2.is_success())

    @mock.patch('historical.api.json.loads', side_effect=mocked_json_loads)
    def test_make_calls_json_loads_on_raw_message(self, json_loads):
        ApiResponse.make(
            self.request_code,
            self.request_status,
            '[[]]'
        )
        json_loads.assert_called_with('[[]]')

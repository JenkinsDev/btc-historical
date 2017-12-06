import json

from requests import Session, Request
from fake_useragent import UserAgent


DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
user_agent = UserAgent(fallback=DEFAULT_USER_AGENT).random


class ApiRequestor:

    ENDPOINT = 'https://bitcoincharts.com/charts/chart.json'

    def __init__(self):
        self.session = Session()

    @staticmethod
    def _generate_headers():
        return {
            'User-Agent': user_agent
        }

    def generate_url(self, exchange, day, interval):
        return '{}?m={}&r={}&i={}&m1=10'.format(
            self.ENDPOINT, exchange, day, interval)

    def prepare_request(self, method, url, headers):
        req = Request(method, url, headers=headers)
        return self.session.prepare_request(req)

    def send_request(self, exchange, day, interval):
        url = self.generate_url(exchange, day, interval)
        prepped_req = self.prepare_request('GET', url, self._generate_headers())
        response = self.session.send(prepped_req)
        return ApiResponse.make(response.status_code, response.text)


class ApiResponse:

    def __init__(self, code, data):
        self.code = code
        self.data = data

    @classmethod
    def make(cls, code, raw_message):
        return cls(
            code,
            json.loads(raw_message)
        )

    def is_error(self):
        return self.code != 200

    def is_success(self):
        return self.code == 200

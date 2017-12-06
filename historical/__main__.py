import csv
import click

from datetime import datetime
from api import ApiRequestor
from export import to_csv


# Day => r
DAY_OPTS = ['1', '3', '5', '10', '30', '60', '90', '120', '150', '180',
            '360', '730', '1460', '2920']

# Interval => i
INTERVAL_OPTS = ['1-min', '5-min', '15-min', '30-min', 'Hourly', '2-hour',
                 '6-hour', '12-hour', 'Daily', 'Weekly']


@click.command()
@click.option('--day', type=click.Choice(DAY_OPTS))
@click.option('--interval', type=click.Choice(INTERVAL_OPTS))
@click.argument('save_file', type=click.File('w'))
def get_historical_pricing(day, interval, save_file):
    api = ApiRequestor()
    response = api.send_request('coinbaseUSD', day, interval)

    # Dirty but whatever, for now
    for ind, datum in enumerate(response.data):
        dt = datetime.fromtimestamp(response.data[ind]['Timestamp'])
        response.data[ind]['Datetime'] = dt.strftime('%Y-%m-%d %H:%M:%S')

    to_csv(save_file, response.data)


if __name__ == "__main__":
    get_historical_pricing()

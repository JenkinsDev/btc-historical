import csv
import click

from .api import ApiRequestor
from .export import to_csv


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
    fields = ['Timestamp', 'Open', 'Low', 'Close', 'Volume (BTC)',
              'Volume (Currency)', 'Weighted Price']
    save_writer = csv.DictWriter(save_file, fieldnames=fields)
    save_writer.writeheader()
    save_writer.writerows([
        {
            'Timestamp': datum[0],
            'Open': datum[1],
            'Low': datum[2],
            'Close': datum[3],
            'Volume (BTC)': datum[4],
            'Volume (Currency)': datum[5],
            'Weighted Price': datum[6]
        } for datum in pricing_raw_data
    ])


if __name__ == "__main__":
    get_historical_pricing()

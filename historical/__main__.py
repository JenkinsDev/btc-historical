import csv
import json
import click
import requests


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
    # TODO: Remove coinbaseUSD hardcode
    exchange = 'coinbaseUSD'

    URL = 'https://bitcoincharts.com/charts/chart.json?m={}&r={}&i={}&m1=10'.format(
        exchange, day, interval)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    resp = requests.get(URL, verify=False, headers=headers)
    pricing_raw_data = json.loads(resp.text)
    resp.close()

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
import requests
from datetime import datetime, timedelta

def lastDay():
    pair = 'BTC'
    start_date = datetime.now() - timedelta(days=1)
    start_timestamp = int(start_date.timestamp())
    end_date = datetime.now()
    end_timestamp = int(end_date.timestamp())
    url = f'https://www.mercadobitcoin.net/api/{pair}/trades/{start_timestamp}/{end_timestamp}/'
    response = requests.get(url)
    data = response.json()
    for trade in data:
        return float(trade['price'])
    return 0


print(lastDay())
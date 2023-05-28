from eth_data_requests import ApiDataFetcher
import os
from datetime import datetime

data_fetcher = ApiDataFetcher(os.getenv('etherscan_key'))

def homepage_data(followed_wallets: list):
    data = []
    for wallet in followed_wallets:
        data.extend(data_fetcher.wallet_transactions(wallet))
    
    formatted_data = [{'time': datetime.strptime(d['time'], '%H:%M, %d-%m-%Y'), 'from': d['from'], 'to': d['to'], 'value': d['value'], 'way': d['way']} for d in data]
    
    sorted_data = sorted(formatted_data, key=lambda x: x['time'])
    
    formatted_data_strings = [{'time': d['time'].strftime('%H:%M, %d-%m-%Y'), 'from': d['from'], 'to': d['to'], 'value': d['value'], 'way': d['way']} for d in sorted_data]
        
    f_data = [txn for txn in reversed(formatted_data_strings)]

    return f_data




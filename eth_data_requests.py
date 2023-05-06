import requests 
from datetime import datetime 

WEI_PER_ETHER = 10**18
URL = 'https://api.etherscan.io/api'

class ApiDataFetcher:

    def __init__(self, apikey):
        self.apikey = apikey
        
    def convert_to_eth(self, wei_val):
        eth_val = wei_val / WEI_PER_ETHER
        return round(eth_val, 3)
    

    def wallet_balance(self,  wallet: str):
        params = {
            "module" : "account",
            "action" : "balance",
            "tag" : "latest",
            "address" : wallet,
            "apikey" : self.apikey
        }
        response = requests.get(url=URL, params=params)
        wei_value = int(response.json()['result'])
        return self.convert_to_eth(wei_val=wei_value)


    def wallet_transactions(self, wallet: str):
        
        params = {
            "module" : "account",
            "action" : "txlist",
            "address": wallet,
            "startblock" : 0,
            "endblock" : 99999999,
            "page" : 1,
            "offset" : 10,
            "sort" : "desc",
            "apikey" : self.apikey #didn't work with the apikey passed in header idk why
        }
        response = requests.get(url=URL, params=params)
        response_data = response.json()['result']

        transactions = []

        for item in response_data:

            timestamp = item["timeStamp"]
            dt_object = datetime.fromtimestamp(int(timestamp))
            date_and_time = dt_object.strftime("%H:%M, %d-%m-%Y")
            source = item["from"]
            target = item["to"]
            value = int(item["value"])

            if value != 0: #ensures that this is ETH transaction, not any other erc-20 token
                transaction = {
                    "time" : date_and_time,
                    "from" : source,
                    "to" : target,
                    "value" : self.convert_to_eth(value) 
                }

                transactions.append(transaction)

        return transactions

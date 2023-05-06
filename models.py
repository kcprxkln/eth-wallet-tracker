
class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.followed_wallets = []
        self.is_logged = False 

    def add_new_wallet(self, wallet):
        self.followed_wallets.append(wallet)

    def remove_wallet(self, wallet):
        self.followed_wallets.remove(wallet)

    
class Wallet():
    def __init__(self, id, transactions):
        self.id = id
        self.transactions = transactions

    def new_transaction(self, Transaction):
        self.transactions.append(Transaction)

class Transaction:
    def __init__(self, source, target, amount):
        self.id = id
        self.source = source
        self.target = target
        self.amount = amount
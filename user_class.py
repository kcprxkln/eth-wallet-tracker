
class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.followed_wallets = []
        self.is_logged = False 

    def add_new_wallet(self, wallet):
        self.followed_wallets.append(wallet)

    def remove_wallet(self, wallet):
        self.followed_wallets.remove(wallet)

    
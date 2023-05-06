from flask import Flask, render_template, request, redirect, url_for
from forms import Login, Register
from models import User
import db_operations
from eth_data_requests import ApiDataFetcher
import os

ETHERSCAN_APIKEY = os.getenv('etherscan_key')

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'justaplaceholder'

eth_data_r = ApiDataFetcher(ETHERSCAN_APIKEY)

@app.route('/')
def home():
    return 'homepage'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # FORM IS FINALLY WORKING PROPERLY
    # -----------------------------
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        print(username)
        password = form.password.data
        print(password) 
        if db_operations.log_in(f"{username}", f"{password}") ==  True:
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials.'
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     if db_operations.log_in(f"{username}", f"{password}") ==  True:
    #         return redirect(url_for('home'))
    #     else:
    #         error = 'Invalid credentials.'
    
    return render_template('login_website.html', error=error, form=form) 

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    form = Register()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if db_operations.register(f"{username}", f"{password}") == False:
            return f'The user {username} already exists'
        else:
            user_id = db_operations.get_id(username)
            user = User(id=user_id,username=username, password=password)
            user.is_logged = True
            return f"user {username} created succesfully"

    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     if db_operations.register(f"{username}", f"{password}") == False:
    #         return f'The user {username} already exist.'
    #     else:
    #         user_id = db_operations.get_id(username)
    #         user = User(id=user_id,username=username, password=password)
    #         user.is_logged = True
    #         return f"user {username} created succesfully"
    else:
        return render_template('register_website.html', form=form, error=error)
    
@app.route('/wallet/<address>', methods=['GET', 'POST'])
def wallet_page(address):
    wallet_balance = eth_data_r.wallet_balance(address)
    wallet_transactions = eth_data_r.wallet_transactions(address)
    return render_template('wallet_page.html', page=address, balance=wallet_balance , transactions=wallet_transactions)

if __name__ == '__main__':
    app.run()
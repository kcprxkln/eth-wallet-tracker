from flask import Flask, render_template, request, redirect, url_for, flash
from forms import Login, Register
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Wallet
from db_operations import db
from eth_data_requests import ApiDataFetcher
import homepage_wallet_data
import os
import string

ETHERSCAN_APIKEY = os.getenv('etherscan_key')
DB_NAME = "database"

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'justaplaceholder'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:postgres@localhost:5432/{DB_NAME}"
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def check_if_wallet_exists(wallet_address):
    for letter in wallet_address:
        if letter not in all_digits_and_letters:
            return False
        
    if len(wallet_address) != 42:
        return False
    
    return True

with app.app_context():
    db.create_all()

eth_data_r = ApiDataFetcher(ETHERSCAN_APIKEY)

all_digits_and_letters = list(string.digits + string.ascii_letters)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'search_wallet' in request.form:
            wallet_address = request.form.get('wallet_address')

            if not check_if_wallet_exists(wallet_address=wallet_address):
                return render_template('bad_address.html')
            
            wallet = Wallet.query.filter_by(name=wallet_address).first() 
            
            if wallet:
                return redirect(url_for("wallet_page", address=wallet_address))
            
            else:
                new_wallet = Wallet(name=new_wallet)
                db.session.add(new_wallet)
                db.session.commit()
                return redirect(url_for("wallet_page", address=wallet_address))
            
    all_followed_wallets = []
    for wallet in current_user.followed_wallets:
        all_followed_wallets.append(wallet.name)
    
    wallets_data = homepage_wallet_data.homepage_data(all_followed_wallets)

    return render_template('home.html', user=current_user, wallets_data=wallets_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        
        if user: 
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Wrong password, please try again', category='error')
                return render_template('login_website.html', error=error, form=form) 

        else:
            flash('There is no such a user', category='error')
            return render_template('login_website.html', error=error, form=form) 
    
    return render_template('login_website.html', error=error, form=form) 


@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    form = Register()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if user: 
            flash('The username is already used', category='error')   
            return render_template('register_website.html', form=form, error=error)
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user,remember=True)
            return redirect(url_for('home'))
        
    else:
        return render_template('register_website.html', form=form, error=error)
    

@app.route('/logout')
@login_required
def logout():
    flash('Successfully logged out', category='success')
    logout_user()
    return redirect(url_for('login'))
    

@app.route('/wallet/<address>', methods=['GET', 'POST'])
def wallet_page(address):

    if not check_if_wallet_exists(wallet_address=address):
                return render_template('bad_address.html')

    is_followed = False
    for wallet in current_user.followed_wallets:
        if wallet.name == address:
            is_followed = True

    if request.method == 'POST':
        if 'search_wallet' in request.form:
            wallet_address = request.form.get('wallet_address')

            if not check_if_wallet_exists(wallet_address=wallet_address):
                return render_template('bad_address.html')
            
            wallet = Wallet.query.filter_by(name=wallet_address).first() 

            if wallet:
                return redirect(url_for("wallet_page", address=wallet_address))
            else:
                new_wallet = Wallet(name=new_wallet)
                db.session.add(new_wallet)
                db.session.commit()
                return redirect(url_for("wallet_page", address=wallet_address))
        
        else:
            if is_followed:
                wallet = Wallet.query.get(wallet.id)
                if wallet:
                    if wallet.user_id == current_user.id:
                        db.session.delete(wallet)
                        db.session.commit()
                        flash(f'Wallet {address} removed from the followed', category='success')
            else: 
                new_followed_wallet = Wallet(name=address, user_id=current_user.id)
                db.session.add(new_followed_wallet)
                db.session.commit()
                flash(f'Wallet {address} added to followed!', category='success')

    wallet_balance = eth_data_r.wallet_balance(address)
    wallet_transactions = eth_data_r.wallet_transactions(address)
    
    return render_template('wallet_page.html', page=address, balance=wallet_balance , transactions=wallet_transactions, user=current_user, is_f=is_followed)


@app.route('/profile/followed_wallets', methods=['GET', 'POST'])
def followed_wallets_page():
    if request.method == 'POST':
        if 'search_wallet' in request.form:
            wallet_address = request.form.get('wallet_address')
            
            if not check_if_wallet_exists(wallet_address=wallet_address):
                return render_template('bad_address.html')
            
            wallet = Wallet.query.filter_by(name=wallet_address).first() 
            
            if wallet:
                return redirect(url_for("wallet_page", address=wallet_address))
            else:
                new_wallet = Wallet(name=new_wallet)
                db.session.add(new_wallet)
                db.session.commit()
                return redirect(url_for("wallet_page", address=wallet_address))
                
    all_followed_wallets = []
    for wallet in current_user.followed_wallets:
        all_followed_wallets.append(wallet.name)
    
    followed_wallets_qty = len(all_followed_wallets)

    return render_template('followed_wallets_page.html', all_followed_wallets=all_followed_wallets, followed_wallets_qty=followed_wallets_qty)


if __name__ == '__main__':
    app.run()
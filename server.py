from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import Login, Register
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users, Wallets
from db_operations import db
from eth_data_requests import ApiDataFetcher
import os

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
    return Users.query.get(int(id))

with app.app_context():
    db.create_all()

eth_data_r = ApiDataFetcher(ETHERSCAN_APIKEY)

@app.route('/')
@login_required
def home():
    # followed_wallet = session['user'].followed_wallets[0]
    # return followed_wallet
    return "This is the Homepage :)"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
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
        
        user = Users.query.filter_by(username=username).first()
        if user: 
            flash('The username is already used', category='error')   
            return render_template('register_website.html', form=form, error=error)
        else:
            new_user = Users(username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(user,remember=True)
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
    if request.method == 'POST':
         if 'search_wallet' in request.form:
            wallet_address = request.form.get('wallet_address')
            wallet = Wallets.filter_by(name=wallet_address)
            if wallet:
                return redirect(url_for("wallet_page", address=wallet_address))
            else:
                new_wallet = Wallets(name=new_wallet)
                db.session.add(new_wallet)
                db.session.commit()
                return redirect(url_for("wallet_page", address=wallet_address))

    wallet_balance = eth_data_r.wallet_balance(address)
    wallet_transactions = eth_data_r.wallet_transactions(address)
    return render_template('wallet_page.html', page=address, balance=wallet_balance , transactions=wallet_transactions)


if __name__ == '__main__':
    app.run()
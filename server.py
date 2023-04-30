from flask import Flask, render_template, request, redirect, url_for
import db_operations
from user_class import User

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return 'homepage'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if db_operations.log_in(f"{username}", f"{password}") ==  True:
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials.'
    
    return render_template('login_website.html', error=error) 

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db_operations.register(f"{username}", f"{password}")
        user_id = db_operations.get_id(username)
        user = User(id=user_id,username=username, password=password)
        user.is_logged = True
        return f"user {username} created succesfully"
    else:
        return render_template('register_website.html')
    
if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request
import db_operations
from user_class import User

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    # if user.is_logged == False:
    #   redirect to /login
    # else show the website
    pass 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return db_operations.log_in(f"{username}", f"{password}")
    else:
        return render_template('login_website.html') 

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db_operations.register(f"{username}", f"{password}")
        user_id = db_operations.get_id(username)
        user = User(id=user_id,username=username)
        return f"user {username} created succesfully"
    else:
        return render_template('register_website.html')


if __name__ == '__main__':
    app.run()
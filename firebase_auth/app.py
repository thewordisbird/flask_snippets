"""Firebase Authentication and Login

Login and manage users with firebase authentication.
"""
import os
import json
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.security import generate_password_hash

# Flask-WTF/WTForms library
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo

# Pyrebase - Firebase API python wrapper
import pyrebase

# Build web form with flask-wtf
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Password", validators=[DataRequired(), EqualTo('password')])

# User class:
class User:
    def __init__(self, name, email, id=None):
        self.name = name
        self.email = email
        self.id = id

    def set_password(self, password):
        return generate_password_hash(password)

    @classmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

# Initialize pyrebase
config = {
  "apiKey": os.environ.get('WEB_API_KEY'),
  "authDomain": "flask_snippets.firebaseapp.com",
  "databaseURL": "https://flask-snippets.firebaseio.com",
  "storageBucket": "flask-snippets.appspot.com",
  "serviceAccount": os.environ.get('FIREBASE_APPLICATION_CREDENTIALS')
}

firebase = pyrebase.initialize_app(config)

app = Flask(__name__)
app.config.from_mapping({
    'SECRET_KEY': 'my_secret'
})

@app.route('/', methods=['GET'])
def index():
    return "<h4>Index</h4>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        auth = firebase.auth()
        
        try:
            user = auth.sign_in_with_email_and_password(form.data['email'], form.data['password'])
            print(user)
            return redirect(url_for('profile'))
        except Exception as e:
           json_data = json.loads(e.args[1])
           print(json_data['error']['message'])



    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        auth = firebase.auth()
        database = firebase.database()
                
        try:
            auth_user = auth.create_user_with_email_and_password(form.data['email'], form.data['password'])
            auth.send_email_verification(auth_user['idToken'])
            print(auth_user)
            
            return redirect(url_for('login'))
        except Exception as e:
            json_data = json.loads(e.args[1])
            print(json_data['error']['message'])
            
        

    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET'])
def profile():
    return '<h4>Profile</h4'
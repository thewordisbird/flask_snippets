"""Firebase Authentication and Login

Login and manage users with firebase authentication.
"""
import os
import datetime
import json
from functools import wraps

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify, abort, make_response
from werkzeug.security import generate_password_hash

# Flask-WTF/WTForms library
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.csrf import CSRFProtect

# Firebase API
import firebase_admin
from firebase_admin import credentials, auth


# Build web form with flask-wtf
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    id_token = StringField(validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Password", validators=[DataRequired(), EqualTo('password')])

# Initialize Firebase
firebase_admin.initialize_app()

app = Flask(__name__)
app.config.from_mapping({
    'SECRET_KEY': 'my_secret'
})

csrf = CSRFProtect(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('Wrapper')
        session_cookie = request.cookies.get('firebase')
        print(f'Wrapper - Session Cookie Val: {session_cookie}')
        if not session_cookie:
            # Session cookie is unavailable. Force user to login.
            print('Wrapper - Session cookie unavailable')
            return redirect(url_for('login', next=request.url))

        # Verify the session cookie. In this case an additional check is added to detect
        # if the user's Firebase session was revoked, user deleted/disabled, etc.
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
            print('Wrapper - Yielding to funciton')
            return f(*args, **kwargs)
        except auth.InvalidSessionCookieError:
            # Session cookie is invalid, expired or revoked. Force user to login.
            print("Wrapper - Session cookie invalid")
            return redirect(url_for('login', next=request.url))
    return decorated_function


@app.route('/', methods=['GET'])
def index():
    return "<h4>Index</h4>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():  
        try:
            user = auth.create_user(
                email=form.data['email'],
                password=form.data['password'],
                display_name= form.data['name'])
            return redirect(url_for('login'))
        except Exception as e:
            flash(e.args[0])
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('in login')
    form = LoginForm()
    
    return render_template('login.html', form=form)


@app.route('/profile', methods=['GET'])
@login_required
def access_restricted_content():
    return render_template('profile.html')
     

@app.route('/test', methods=['GET'])
def test():
    return render_template('login2.html')

@app.route('/sessionLogin', methods=['POST'])
def session_login():
    print('In SessionLogin')
    
    id_token = request.form.get('idToken')
    expires_in = datetime.timedelta(days=5)
    try:
        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        resp = jsonify({'status': 'success'})
        expires = datetime.datetime.now() + expires_in
        resp.set_cookie('firebase', session_cookie, expires=expires, httponly=True, secure=False)
        print(f'SessionLogin - returning resp: {resp}')
        return resp
    except Exception as e:
        print(f'error: {e.args}')
        return abort(401, 'SessionLogin - Failed to create a session cookie')

@app.route('/sessionLogout', methods=['POST'])
@csrf.exempt
def session_logout():
    print('in session logout')
    resp = jsonify({'status': 'success'})
    resp.set_cookie('firebase', expires=0)
    return resp

@app.route('/set')
def set_cookie():
    resp = make_response(redirect(url_for('endpoint')))
    resp.set_cookie('name', 'sam')
    return resp

@app.route('/get')
def get_cookie():
    name = request.cookies.get('name')
    return f'Name is {name}'

@app.route('/endpoint')
def endpoint():
    name = request.cookies.get('name')
    print(f'cookie name: {name}')
    return render_template('profile.html')
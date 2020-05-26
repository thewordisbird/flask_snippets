import os
import datetime


from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify, abort, make_response, current_app, Blueprint

from .forms import LoginForm, RegisterForm
from flask_wtf.csrf import CSRFProtect

from firebase_auth import login_required, create_session_cookie

# Try moving this into factory
csrf = CSRFProtect(current_app)

bp = Blueprint('auth', __name__, static_folder='static')


@bp.route('/', methods=['GET'])
def index():
    return "<h4>Index</h4>"

@bp.route('/register', methods=['GET', 'POST'])
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


@bp.route('/login', methods=['GET', 'POST'])
def login():
    print('in login')
    form = LoginForm()
    
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        expires_in = datetime.timedelta(days=5)
        session_cookie =  create_session_cookie(id_token, expires_in)
        if session_cookie:
            resp = jsonify({'status': 'success'})
            expires = datetime.datetime.now() + expires_in
            resp.set_cookie('firebase', session_cookie, expires=expires, httponly=True, secure=False)
            print(f'SessionLogin - returning resp: {resp}')
            return resp
        else:
            abort(401, 'Failed to create a session cookie')
    return render_template('login.html', form=form)


@bp.route('/profile', methods=['GET'])
@login_required
def access_restricted_content():
    session_cookie = request.cookies.get('firebase')
    #decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
    #uid = decoded_claims.get('user_id')
    #email = decoded_claims.get('email')
    return render_template('profile.html')


@bp.route('/sessionLogin', methods=['POST'])


@bp.route('/sessionLogout', methods=['POST'])
@csrf.exempt
def session_logout():
    print('in session logout')
    resp = jsonify({'status': 'success'})
    resp.set_cookie('firebase', expires=0)
    return resp

@bp.route('/set')
def set_cookie():
    resp = make_response(redirect(url_for('endpoint')))
    resp.set_cookie('name', 'sam')
    return resp

@bp.route('/get')
def get_cookie():
    name = request.cookies.get('name')
    return f'Name is {name}'

@bp.route('/endpoint')
def endpoint():
    name = request.cookies.get('name')
    print(f'cookie name: {name}')
    return render_template('profile.html')

@bp.route('/login_test')
def login_test():
    form = LoginForm()
    return render_template('login_test.html', form=form)
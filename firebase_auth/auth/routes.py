import os
import datetime

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify, abort, make_response, current_app, Blueprint, session

from .forms import LoginForm, RegisterForm, ResetPasswordForm
from flask_wtf.csrf import CSRFProtect

from firebase_auth import login_required, create_session_cookie, create_new_user, send_password_reset_email

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
        email = form.data['email']
        password = form.data['password']
        display_name = form.data['name']
        user = create_new_user(email, password, display_name)
        # TODO: connect to firestore db to store additional user info by uid
        return redirect(url_for('auth.login'))        
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        expires_in = datetime.timedelta(days=5)
        try:
            session_cookie =  create_session_cookie(id_token, expires_in)
        except Exception:
            # TODO: respond with error to display message to user
            # see create_session_cookie function for info on possible errors
            abort(401, 'Failed to create a session cookie')
        else:
            # Create Flask User session to store uid for user information lookup
            session['_user_id'] = request.form.get('uid')
            # Create response to client
            resp = jsonify({'status': 'success'})
            expires = datetime.datetime.now() + expires_in
            # CHANGE TO SECURE FOR PRODUCTION!!
            resp.set_cookie('firebase', session_cookie, expires=expires, httponly=True, secure=False)
            return resp
    return render_template('login.html', form=form, title="Login")


@bp.route('/profile', methods=['GET'])
@login_required
def access_restricted_content():
    session_cookie = request.cookies.get('firebase')
    #decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
    #uid = decoded_claims.get('user_id')
    #email = decoded_claims.get('email')
    return render_template('profile.html')


@bp.route('/resetPassword', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        send_password_reset_email(form.data['email'])
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form, title='Reset Password')


@bp.route('/sessionLogout', methods=['POST'])
@csrf.exempt
def session_logout():
    print('in session logout')
    resp = jsonify({'status': 'success'})
    resp.set_cookie('firebase', expires=0)
    return resp



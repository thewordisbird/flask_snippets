from functools import wraps
import os
import json
import requests
from requests import HTTPError

# Firebase API
import firebase_admin
from firebase_admin import credentials, auth
from flask import request, redirect, url_for

def initialize_firebase():
    firebase_admin.initialize_app()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('Wrapper')
        session_cookie = request.cookies.get('firebase')
        print(f'Wrapper - Session Cookie Val: {session_cookie}')
        if not session_cookie:
            # Session cookie is unavailable. Force user to login.
            print('Wrapper - Session cookie unavailable')
            return redirect(url_for('auth.login', next=request.url))

        # Verify the session cookie. In this case an additional check is added to detect
        # if the user's Firebase session was revoked, user deleted/disabled, etc.
        try:
            decoded_claims = verify_session_cookie(session_cookie)
            print(decoded_claims)
            #print(decoded_claims)
            return f(*args, **kwargs)
        except auth.InvalidSessionCookieError:
            # Session cookie is invalid, expired or revoked. Force user to login.
            print("Wrapper - Session cookie invalid")
            return redirect(url_for('auth.login', next=request.url))
    return decorated_function


def create_session_cookie(id_token, expires_in):
    print('In SessionLogin')
    print(id_token)
    try:
        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        return session_cookie
    except Exception as e:
        print(f'error: {e.args}')
        return None

def verify_session_cookie(session_cookie):
    return auth.verify_session_cookie(session_cookie, check_revoked=True)


def create_new_user(email, password, display_name):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name)
        return user
    except Exception as e:
        raise e

def generate_email_verification_link(user_email):
    return auth.generate_email_verification_link

def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except HTTPError as e:
        # raise detailed error message
        # TODO: Check if we get a { "error" : "Permission denied." } and handle automatically
        raise HTTPError(e, request_object.text)

def send_email_varification(id_token):
    endpoint = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={os.environ.get('WEB_API_KEY')}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
    request_object = requests.post(endpoint, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_password_reset_email(email):
    endpoint = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={os.environ.get('WEB_API_KEY')}"
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
    request_object = requests.post(endpoint, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()


"""Firebase Authentication and Login

Login and manage users with firebase authentication.
"""




app = Flask(__name__)
app.config.from_mapping({
    'SECRET_KEY': 'my_secret'
})

csrf = CSRFProtect(app)


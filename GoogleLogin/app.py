from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Generate a nonce value
def generate_nonce():
    return os.urandom(16).hex()

# Configure Google OAuth
oauth = OAuth(app)
nonce = generate_nonce()
google = oauth.register(
    name='google',
    client_id='ID',
    client_secret='SECRET',
    authorize_params={'nonce': nonce},
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

# Routes
@app.route('/')
def index():
    return '<a href="/google-login">Login with Google</a>'

@app.route('/google-login')
def google_login():
    return google.authorize_redirect(redirect_uri=url_for('google_callback', _external=True), nonce=nonce)

@app.route('/google-login/callback')
def google_callback():
    token = google.authorize_access_token()
    user = google.parse_id_token(token, nonce=nonce)
    session['user'] = user
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return f'Logged in as {user["name"]} ({user["email"]}) <br><a href="/logout">Logout</a>'
    return 'Not logged in'

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

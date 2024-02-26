# The user details get print in the console.
# so you can do whatever you want to do instead
# of printing it

from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = 'secret'

oauth = OAuth(app)

@app.route('/')
def index():
	print(os.environ.get('957714069027669'))
	return render_template('index.html')

@app.route('/google/')
def google():

	# Google Oauth Config
	# Get client_id and client_secret from environment variables
	# For developement purpose you can directly put it here inside double quotes
	GOOGLE_CLIENT_ID = os.environ.get('1097921833162-pap1q095mk8r61d4jk8ga04pl0mvu71h.apps.googleusercontent.com')
	GOOGLE_CLIENT_SECRET = os.environ.get('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')
	CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
	oauth.register(
		name='google',
		client_id=GOOGLE_CLIENT_ID,
		client_secret=GOOGLE_CLIENT_SECRET,
		server_metadata_url=CONF_URL,
		client_kwargs={
			'scope': 'openid email profile'
		}
	)
	
	# Redirect to google_auth function
	redirect_uri = url_for('google_auth', _external=True)
	return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
	token = oauth.google.authorize_access_token()
	user = oauth.google.parse_id_token(token)
	print(" Google User ", user)
	return redirect('/')

@app.route('/test')
def test():
	print(os.environ.get('957714069027669'))
	return redirect('/')

@app.route('/facebook/')
def facebook():

	# Facebook Oauth Config
	FACEBOOK_CLIENT_ID = '957714069027669'
	FACEBOOK_CLIENT_SECRET = 'f68dce1ebb6e7a8329fe4d0ffdfe5e06'
	oauth.register(
		name='facebook',
		client_id=FACEBOOK_CLIENT_ID,
		client_secret=FACEBOOK_CLIENT_SECRET,
		access_token_url='https://graph.facebook.com/oauth/access_token',
		access_token_params=None,
		authorize_url='https://www.facebook.com/dialog/oauth',
		authorize_params=None,
		api_base_url='https://graph.facebook.com/',
		client_kwargs={'scope': 'email'},
	)
	redirect_uri = url_for('facebook_auth', _external=True)
	return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/facebook/auth/')
def facebook_auth():
	token = oauth.facebook.authorize_access_token()
	resp = oauth.facebook.get(
		'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
	profile = resp.json()
	print("Facebook User ", profile)
	return redirect('/')

if __name__ == "__main__":
	app.run(debug=True)

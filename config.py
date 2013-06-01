import os
from oauth2client.client import flow_from_clientsecrets

API_KEY = 'your apikey'

MONGO_URI = 'mongodb://server'

LOGIN_URL ='/google/login'

GOOGLE_KEY = 'you key'
GOOGLE_SECRET = 'your secret'
GOOGLE_SCOPE = 'name,email,language,username'
GOOGLE_CALLBACK = 'http://watchi.ap01.aws.af.cm/oauth2callback'

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '.', 'client_secrets.json')
FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope=[
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'],
    redirect_uri='http://watchi.ap01.aws.af.cm/oauth2callback')

try:
    from local_config import *
except:
    pass

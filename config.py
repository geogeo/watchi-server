import os
from oauth2client.client import flow_from_clientsecrets

MONGO_URI = 'mongodb://server'

LOGIN_URL ='/google/login'

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '.', 'your_client_secrets.json')
# FLOW = flow_from_clientsecrets(
#     CLIENT_SECRETS,
#     scope=[
#         'https://www.googleapis.com/auth/userinfo.profile',
#         'https://www.googleapis.com/auth/userinfo.email'],
#     redirect_uri='http://watchi.ap01.aws.af.cm/oauth2callback')

try:
    from server_config import *
    from local_config import *
except:
    pass

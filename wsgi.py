import bottle
import os
from bottle import Bottle, route, run, get, post, request,redirect,response,view,static_file
import json
import urllib
import urllib2
import config
from pymongo import MongoClient
from database import get_db as db
from pprint import pformat
import httplib2
from apiclient.discovery import build

application = app = Bottle()
reg_ids = set()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@app.route('/google/login')
def google_login():
    authorize_url = config.FLOW.step1_get_authorize_url()
    # url = google.redirect(request.environ)
    redirect(authorize_url)

@app.route('/oauth2callback')
def google_callback():
    code = request.query.get('code')
    if not code:
        redirect('/google/login/error')

    credential = config.FLOW.step2_exchange(code)
    http = httplib2.Http()
    http = credential.authorize(http)
    user_info_service = build('oauth2','v2',http=http)
    user_info = user_info_service.userinfo().get().execute()
    # resp, content = http.request("https://www.googleapis.com/oauth2/v1/userinfo?alt=json", "GET")
   
    if user_info and user_info.get('id'):
        credential_dict = json.loads(credential.to_json())
        user_info.update({'access_token':credential_dict['access_token'],'token_hash':credential_dict['id_token']['token_hash']})
        db().user_info.insert(user_info)
        response.set_cookie('session_id', credential_dict['id_token']['token_hash'])
        redirect('/')
        
    else:
        return 'user auth error'
   
@app.post("/register")
def register():
    device_info = {request.forms.email:request.forms.reg_id}
    if db().device_info.find_one(device_info)!=None:
        db().device_info.insert(device_info)
    return "sucess"

@app.route("/")
@view("index")
def index():
    session_id = request.get_cookie('session_id')
    # from nose.tools import set_trace;set_trace()
    user_info = db().user_info.find_one({"token_hash":session_id})
    
    if user_info!=None:
        attached_devices = db().attached_devices.find_one({"id":user_info['id']})
        return {"attached_devices":attached_devices,"userinfo":user_info}
    else:
        redirect('/google/login')

@app.route("/user/:userid")
def userinfo(userid):
    session_id = request.get_cookie('session_id')
    from nose.tools import set_trace;set_trace()
    user_info = db().user_info.find_one({"token_hash":session_id})
    
    if user_info['id'] == userid:
        return user_info
    else:
        return "you are not this user"
    

@app.post('/send')
def send():
    """
      Sends a message to the devices.
      The message is specified by the 'msg' parameter.
      The devices are specified by the 'reg_id' parameter. If the request does
      not contain any registration ids, the message will be sent to all
      devices recorded by /register

      Sample request:
      curl -d "reg_id=test_id&msg=Hello" http://localhost:8080/sen
    """
    global reg_ids
    params = request.forms
    msg =  params.msg
    reg_id_list = []
    if 'reg_id' in params and len(params['reg_id']) > 0:
      reg_id_list.append(params['reg_id'])

    if reg_id_list is None:
      # sys.stderr.write('Sending message to all registered devices\n')
      reg_id_list = list(reg_ids)

    data = {
      'registration_ids' : reg_id_list,
      'data' : {
        'addr':"15349255920",
        'msg' : msg
      }
    }

    headers = {
      'Content-Type' : 'application/json',
      'Authorization' : 'key=' + config.API_KEY
    }

    url = 'https://android.googleapis.com/gcm/send'
    print data, headers
    gcm_req = urllib2.Request(url, json.dumps(data), headers)

    try:
      gcm_resp = urllib2.urlopen(gcm_req)
      return make_gcm_summary(data, gcm_resp)
    except urllib2.HTTPError, e:
      return "error",e.read()

def make_gcm_summary(data, response):
    """
      Helper function to display the result of a /send request.
    """
    json_string = response.read()
    json_response = json.loads(json_string)

    html = """
<html>
  <head>
    <title>GCM send result</title>
  </head>
  <body>
    <h2>Request</h2>
    <pre>%s</pre>
    <h2>Response</h2>
    <pre>%s</pre>
    <h3>Per device</h3>
    <ol>""" % (repr(data), json_string)

    reg_id_list = data['registration_ids']
    for i in xrange(len(reg_id_list)):
      reg_id = reg_id_list[i]
      result = json_response['results'][i]

      html += """
        <li>
          reg_id: <code>%s</code><br/>
          <pre>%s</pre>
        </li>""" % (reg_id, json.dumps(result))

      html += """
    </ol>
    <a href="/">Back</a>
  </body>
</html>"""
    return html
#run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), server='gunicorn')
if __name__ == '__main__':
    run(app, host='127.0.0.1', port=5000, reloader=True, debug=True)

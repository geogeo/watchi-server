import bottle
import os
from bottle import Bottle, route, run, get, post, request
import json
import urllib
import urllib2
import config
from pymongo import MongoClient
from database import db

application = app = Bottle()
reg_ids = set()

@app.post("/register")
def register():
    global reg_ids
    reg_ids.add(request.forms.reg_id)
    return "sucess"

@app.route("/")
def index():
    global reg_ids
    reg_id_list = list(reg_ids)

    html = """
<html>
    <head>
        <title>Sample GCM Server</title>
    </head>
    <body>
"""
    cltion = db.test_collection
    if len(reg_ids) == 0:
        html += "<h3>No registered devices</h3>"
        html += str(cltion.find_one())
    else:
        html += """<h3>Registered Ids</h3>
        <form action="/send" method="post">
            Message: <input name="msg" size="30" />
            <input type="submit" value="Send" />
            <br />
            Devices:
            <table>"""
        

        for reg_id in reg_id_list:
            html += """
                <tr>
                    <td>
                        <input type="checkbox" name="reg_id" value="%s" checked />%s
                    </td>
                </tr>
            """ % (reg_id, reg_id)

        html += """
        </table>
    </form>"""

    html += """
  </body>
</html>
"""
    return html

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

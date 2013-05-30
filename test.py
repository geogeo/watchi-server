from nose.tools import set_trace
from mock import MagicMock, patch,DEFAULT,Mock
from bottle import HTTPResponse,request
from pymongo.database import Database, Collection
from mongomock import *

from mock import patch, Mock
import bottle

# mock decorater view
v = patch("bottle.view",return_value = lambda x : x)
v.start()

# mock import config
import sys
config_mock = Mock(spec=['config'])
config_mock.__name__ = 'config'
sys.modules['config'] = config_mock
config_mock.LOGIN_URL = "/google/login"

# mock database
db = Database(Connection())
patch("database.get_db",return_value = db).start()

def setup():
    global db
    db.user_info.insert({'id':"12",'token_hash':"session","email":"oyanglulu@gmail.com"})
    db.attached_devices.insert({'email':"oyanglulu@gmail.com","attatched_devices":"nexus"})

def tear_down():
    global db
    db.drop_collection("user_info")
    db.drop_collection("attached_devicese")

import wsgi

def test_index_without_login():
    try:
        wsgi.index()
    except HTTPResponse as e:
        assert e._headers['Location']==['http://127.0.0.1/google/login']

@patch("wsgi.db")
@patch("wsgi.request")
def test_index_with_session(mock_request,mock_db):
    mock_request.get_cookie = MagicMock(return_value='session')
    global db
    mock_db.return_value = db
    mock_db.attached_devices = MagicMock(return_value="attached_devices")
    resp = wsgi.index()
    print resp
    for device in resp['attached_devices']:
        device.pop('_id')
    resp['userinfo'].pop('_id')
    assert resp =={u'attached_devices': [{u'email': u'oyanglulu@gmail.com', u'attatched_devices': u'nexus'}], u'userinfo': {u'token_hash': u'session', u'id': u'12', u'email': u'oyanglulu@gmail.com'}}

@patch("wsgi.request")
def test_access_my_own_userinfo(mock_request):
    mock_request.get_cookie = MagicMock(return_value="session")
    resp =wsgi.userinfo("12")
    assert resp['user_info']['id'] =="12"

@patch("wsgi.request")
def test_register_device(mock_request):
    forms = bottle.MultiDict()
    forms.append("email","oyanglulu@gmail.com")
    forms.append("reg_id","whatever from google")
    forms.append("phone_name","nexus4")
    mock_request.forms = bottle.FormsDict(forms)
    resp = wsgi.register()
    assert resp == "sucess"


# @patch("wsgi.request")
# def test_send_msg(mock_request):
#     forms = bottle.MultiDict()
#     forms.append("email", "oyanglulu@gmail.com")
#     forms.append("reg_id", "whatever from google")
#     forms.append("phone_name", "nexus10")
#     mock_request.forms = bottle.FormsDict(forms)
#     resp = wsgi.register()
#     assert resp == "success"

# @patch("wsgi.request")
# def test_send_msg(mock_request):

# v.stop()

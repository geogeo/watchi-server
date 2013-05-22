
from nose.tools import set_trace
from mock import MagicMock, patch,DEFAULT,Mock
from bottle import HTTPResponse,request
from pymongo.database import Database, Collection
from mongomock import *

from mock import patch, Mock
p = patch("bottle.view")
p.start()
import bottle
bottle.view.return_value = lambda x : x
import wsgi

mock = Mock()
views= {'wsgi':mock,'wsgi.view':mock.module}
import wsgi
db = Database(Connection())
def setup():
    global db
    db.user_info.insert({'id':"12",'token_hash':"session"})
    db.attached_devices.insert({'id':"12","attatched_devices":"nexus"})

def tear_down():
    global db
    db.drop_collection("user_info")
    db.drop_collection("attached_devicese")
    
def test_index_without_login():
    try:
        wsgi.index()
    except HTTPResponse as e:
        assert e._headers['Location']==['http://127.0.0.1/google/login']

@patch("wsgi.db")
@patch("wsgi.request")
def test_index_with_session(mock_request,mock_db):
    mock_view = lambda x:x
    mock_request.get_cookie = MagicMock(return_value='session')
    global db
    mock_db.return_value = db
    mock_db.attached_devices = MagicMock(return_value="attached_devices")
    resp = wsgi.index()
    print resp
    resp['attached_devices'].pop('_id')
    resp['userinfo'].pop('_id')
    assert resp == {'attached_devices': {'id': '12', 'attatched_devices': 'nexus'}, 'userinfo': {'token_hash': 'session', 'id': '12'}}

@patch("wsgi.db")
@patch("wsgi.request")
def test_access_my_own_userinfo(mock_request,mock_db):
    mock_request.get_cookie = MagicMock(return_value="session")
    global db
    mock_db.return_value = db
    resp =wsgi.userinfo("12")
    assert resp['id'] =="12"

@patch("wsgi.db")
@patch("wsgi.request")
def test_deny_access_other_peoples_userinfo(mock_request,mock_db):
    mock_request.get_cookie = MagicMock(return_value="session")
    global db
    mock_db.return_value = db
    resp =wsgi.userinfo("1")
    assert resp=="you are not this user"

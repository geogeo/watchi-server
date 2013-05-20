import wsgi
from nose.tools import set_trace
from mock import MagicMock, patch
from bottle import HTTPResponse,request
from pymongo.database import Database, Collection


def cut_off(*patches):    
    def decorator(meth):        
        def wrapper(self, *args):            
            return meth(self, *args[:-len(patches)])        
        for obj in patches:            
            wrapper = patch(obj)(wrapper)        
        return wrapper    
    return decorator


def test_index_without_login():
    try:
        wsgi.index()
    except HTTPResponse as e:
        assert e._headers['Location']==['http://127.0.0.1/google/login']

@patch("wsgi.db")
@cut_off("wsgi.view")
def test_index_with_session(mock_db,mock_view):
    request.get_cookie = MagicMock(return_value='1234')
    mock_db.user_info = MagicMock(return_value='userinfo')
    mock_db.attached_devices = MagicMock(return_value="attached_devices")
    assert wsgi.index() == {"attached_devices":"attached_devices","userinfo":"userinfo"}
        

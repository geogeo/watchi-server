<html>
 %include header_template title='nima'
    <body>
      <div class="navbar">
        <div class="navbar-inner">
          <a class="brand" href="#">Watchi</a>
          <ul class="nav pull-right">
            <li>
%if userinfo:
<a href="user/{{userinfo.get('id')}}">{{userinfo["id"]}}</a>
%else:
              <a   href="/google/login">Login Google</a>
%end
            </li>
          </ul>        

        </div>
      </div>

      <h1>Your attached devices</h1>
      
      %if attached_devices > 0:
      <h3>Registered Ids</h3>
      <form action="/send" method="post">
        Message: <input name="msg" size="30" />
        <input type="submit" value="Send" />
        <br />
        Devices:
        <table>
          <tr>
            <td>
              <input type="checkbox" name="reg_id" value="%s" checked />%s
            </td>
          </tr>
        </table>
      </form>
      %else:
<h3>      No Device Registed</h3>
      %end


      <script src="http://code.jquery.com/jquery.js"></script>
      <script src="static/js/bootstrap.min.js"></script>
    </body>
  </html>

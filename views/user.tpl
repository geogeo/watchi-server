<html>
%include header_template title='nima'
  <body>
    <div class=thumbnail>
      <img src="{{user_info['picture']}}" alt="{{user_info['name']}}" />
      <div class="caption">
        <h3>{{user_info['name']}}</h3>
        <p> email: {{user_info['email']}}</p>
      </div>
    </div>
    <table width="auto" class="table-striped">
      <thead>
        <th>#</th>
        <th>Device</th>
        <th>Checked</th>
      </thead>
      <tbody>
        %for device in attached_devices:
        <tr>
          <td>{{device.id}}</td>
          <td>{{device.name}}</td>
          <td>{{device.enable}}</td>
        </tr>
        %end
    </table>
    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
  </body>
</html>

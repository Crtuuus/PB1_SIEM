% rebase('base.tpl')

<h2>SIEM dogodki</h2>
<table border="1">
  <tr><th>ID</th><th>Čas</th><th>Tip</th><th>Resnost</th><th>Sporočilo</th><th>Asset ID</th></tr>
% for e in events:
  <tr>
    <td>{{e.event_id}}</td>
    <td>{{e.timestamp}}</td>
    <td>{{e.event_type}}</td>
    <td>{{e.severity}}</td>
    <td>{{e.message}}</td>
    <td>{{e.asset_id}}</td>
  </tr>
% end
</table>

% rebase('base.tpl')

<h2>Naprave (Assets)</h2>
<table border="1">
  <tr><th>ID</th><th>Hostname</th><th>IP</th><th>Tip</th><th>Lokacija</th></tr>
% for a in assets:
  <tr>
    <td>{{a.asset_id}}</td>
    <td>{{a.hostname}}</td>
    <td>{{a.ip_address}}</td>
    <td>{{a.device_type}}</td>
    <td>{{a.location}}</td>
  </tr>
% end
</table>
</table>
% if total > per_page:
<div class="pagination">
    % if page > 1:
        <a href="?page={{page-1}}">« Prejšnja</a>
    % end
    <span>Stran {{page}}</span>
    % if page * per_page < total:
        <a href="?page={{page+1}}">Naslednja »</a>
    % end
</div>
% end
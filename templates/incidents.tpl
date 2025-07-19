% rebase('base.tpl')

<h2>Incidenti</h2>
<table border="1">
  <tr><th>ID</th><th>Naslov</th><th>Opis</th><th>Status</th><th>Dodeljen</th><th>Datum</th></tr>
% for inc in incidents:
  <tr>
    <td>{{inc.incident_id}}</td>
    <td>{{inc.title}}</td>
    <td>{{inc.description}}</td>
    <td>{{inc.status}}</td>
    <td>{{inc.assigned_to.name if inc.assigned_to else "Nedodeljen"}}</td>
    <td>{{inc.created_date}}</td>
  </tr>
% end
</table>
% if total > per_page:
<div class="pagination">
    % if page > 1:
        <a href="/incidents?page={{page-1}}">« Prejšnja</a>
    % end
    <span>Stran {{page}}</span>
    % if page * per_page < total:
        <a href="/incidents?page={{page+1}}">Naslednja »</a>
    % end
</div>

% end

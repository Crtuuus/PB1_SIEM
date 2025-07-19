% rebase('base.tpl')

<h2>Uporabniki</h2>
<table border="1">
  <tr><th>ID</th><th>Ime</th><th>Vloga</th><th>Email</th></tr>
% for user in users:
  <tr>
    <td>{{user.user_id}}</td>
    <td>{{user.name}}</td>
    <td>{{user.role}}</td>
    <td>{{user.email}}</td>
  </tr>
% end
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

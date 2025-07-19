% rebase('base.tpl')

<h2>Ranljivosti</h2>
<table border="1">
  <tr><th>ID</th><th>CVE</th><th>Opis</th><th>Score</th><th>Status</th><th>Datum odkrite</th><th>Datum odprave</th></tr>
% for v in vulns:
  <tr>
    <td>{{v.vuln_id}}</td>
    <td>{{v.cve_id}}</td>
    <td>{{v.description}}</td>
    <td>{{v.score}}</td>
    <td>{{v.status}}</td>
    <td>{{v.discovered_date}}</td>
    <td>{{v.fixed_date}}</td>
  </tr>
% end
</table>

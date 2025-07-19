% rebase('base.tpl')
<h1>Incident Stats</h1>
<ul>
    % for title, count in title_stats.items():
        <li>{{ title }}: {{ count }}</li>
    % end
</ul>
<p>Resolved: {{ resolved_count }}</p>
<p>Unresolved: {{ unresolved_count }}</p>

% rebase('base.tpl')

<style>
.chart-container {
  max-width: 500px;
  margin: 2rem auto;
}
canvas {
  width: 100% !important;
  height: auto !important;
}
</style>

<h2>Statistika</h2>
<ul>
  <li>👤 Uporabniki: {{users_count}}</li>
  <li>💻 Naprave: {{assets_count}}</li>
  <li>📄 Dogodki: {{events_count}}</li>
  <li>⚠️ Ranljivosti: {{vulns_count}}</li>
</ul>

<h3>Distribucija incidentov (besedilno)</h3>
<ul>
% for k, v in incident_stats.items():
  <li>{{k}}: {{v}}</li>
% end
</ul>

<h3>Distribucija incidentov (grafično - Pie Chart)</h3>
<div class="chart-container">
  <canvas id="pieChart"></canvas>
</div>

<h3>Incidenti po mesecih (Histogram)</h3>
<div class="chart-container">
  <canvas id="barChart"></canvas>
</div>

<!-- Chart.js CDN -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Inicializacija grafov -->
<script>
window.onload = function() {
    const pieCtx = document.getElementById('pieChart').getContext('2d');
    const pieData = {{! json.dumps(dict(incident_stats)) }};
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(pieData),
            datasets: [{
                data: Object.values(pieData),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)',
                    'rgba(199, 199, 199, 0.6)'
                ]
            }]
        }
    });

    const barCtx = document.getElementById('barChart').getContext('2d');
    const monthlyData = {{! json.dumps(dict(monthly_stats)) }};
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(monthlyData),
            datasets: [{
                label: 'Incidenti po mesecih',
                data: Object.values(monthlyData),
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
</script>

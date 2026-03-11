from flask import Flask, render_template_string, jsonify
import storage
import subprocess
import json

app = Flask(__name__)

@app.route('/run-test', methods=['POST'])
def run_test():
    try:
        subprocess.run(["python3", "tester.py"], check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.route('/reset', methods=['POST'])
def reset_data():
    try:
        storage.reset_db()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.get("/")
def dashboard():
    runs = storage.get_recent_runs()
    chart_runs = runs[::-1]
    labels = [f"Test {r[0]}" for r in chart_runs] 
    data_points = [r[3] for r in chart_runs]
    
    total_tests = len(runs)
    avg_latency = round(sum(r[3] for r in runs) / total_tests, 1) if total_tests > 0 else 0
    success_rate = round((sum(1 for r in runs if r[4] == 1) / total_tests) * 100, 1) if total_tests > 0 else 0
    last_status = runs[0][4] if total_tests > 0 else 1

    json_data = []
    for r in runs:
        json_data.append({"id": r[0], "date": r[1], "api": r[2], "latency": r[3], "success": bool(r[4])})

    html_code = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Analyse Agify Pro</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #0f172a; margin: 0; padding: 40px; color: #f8fafc; }
            .container { max-width: 1000px; margin: auto; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            h1 { font-size: 26px; margin: 0; font-weight: 700; }
            
            .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
            .stat-label { color: #94a3b8; font-size: 11px; text-transform: uppercase; margin-bottom: 8px; font-weight: 600; }
            .stat-value { font-size: 20px; font-weight: 700; color: #f8fafc; }

            .chart-container-wrapper { background: #1e293b; border-radius: 12px; border: 1px solid #334155; padding: 20px; margin-bottom: 20px; overflow-x: auto; }
            .chart-area { min-width: 1000px; height: 300px; }

            .card { background: #1e293b; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px; overflow: hidden; }
            .actions { display: flex; gap: 10px; }
            .btn { border: none; padding: 10px 18px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; transition: 0.2s; }
            .btn-primary { background: #6366f1; color: white; }
            .btn-secondary { background: #334155; color: #f8fafc; }
            .btn-refresh { background: #10b981; color: white; }
            .btn-danger { background: #ef4444; color: white; }
            
            table { width: 100%; border-collapse: collapse; }
            th { text-align: left; font-size: 11px; color: #94a3b8; text-transform: uppercase; padding: 15px; }
            td { padding: 15px; border-top: 1px solid #334155; font-size: 14px; }
            .status-ok { color: #4ade80; font-weight: 600; }
            .status-err { color: #f87171; font-weight: 600; }

            ::-webkit-scrollbar { height: 8px; }
            ::-webkit-scrollbar-thumb { background: #4f46e5; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Analyse Agify</h1>
                <div class="actions">
                    <button class="btn btn-danger" onclick="resetData()">Reset</button>
                    <button class="btn btn-refresh" onclick="location.reload()">Actualiser</button>
                    <button class="btn btn-secondary" onclick="exportJSON()">Exporter JSON</button>
                    <button class="btn btn-primary" id="testBtn" onclick="triggerTest()">Lancer un test</button>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Etat Global</div>
                    <div class="stat-value" style="color: {{ '#4ade80' if last_status == 1 else '#f87171' }}">
                        {{ "OK" if last_status == 1 else "ERREUR" }}
                    </div>
                </div>
                <div class="stat-card"><div class="stat-label">Latence Moyenne</div><div class="stat-value">{{ avg_latency }} ms</div></div>
                <div class="stat-card"><div class="stat-label">Taux de Succes</div><div class="stat-value">{{ success_rate }}%</div></div>
                <div class="stat-card"><div class="stat-label">Total Tests</div><div class="stat-value">{{ total_tests }}</div></div>
            </div>
            
            <div class="chart-container-wrapper">
                <div class="chart-area"><canvas id="latencyChart"></canvas></div>
            </div>

            <div class="card">
                <table>
                    <thead>
                        <tr><th style="padding-left:20px">ID</th><th>Date</th><th>Latence</th><th>Statut</th></tr>
                    </thead>
                    <tbody>
                        {% for run in runs %}
                        <tr>
                            <td style="padding-left:20px">#{{ run[0] }}</td>
                            <td>{{ run[1] }}</td>
                            <td style="font-weight: 600;">{{ run[3] }} ms</td>
                            <td class="{{ 'status-ok' if run[4] == 1 else 'status-err' }}">
                                {{ "Operationnel" if run[4] == 1 else "Echec" }}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            function triggerTest() {
                const btn = document.getElementById('testBtn');
                btn.innerText = "En cours..."; btn.disabled = true;
                fetch('/run-test', { method: 'POST' }).then(() => location.reload());
            }

            function resetData() {
                if(confirm("Voulez-vous vraiment supprimer tout l'historique ?")) {
                    fetch('/reset', { method: 'POST' }).then(() => location.reload());
                }
            }

            function exportJSON() {
                const data = {{ json_data|tojson }};
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a'); a.href = url; a.download = 'export.json'; a.click();
            }

            const ctx = document.getElementById('latencyChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: {{ labels|tojson }},
                    datasets: [{
                        label: 'Latence (ms)',
                        data: {{ data_points|tojson }},
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.2)',
                        fill: true, tension: 0.3, pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    }
                }
            });
            const wrapper = document.querySelector('.chart-container-wrapper');
            wrapper.scrollLeft = wrapper.scrollWidth;
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code, runs=runs, labels=labels, data_points=data_points, 
                                 json_data=json_data, avg_latency=avg_latency, 
                                 success_rate=success_rate, total_tests=total_tests, last_status=last_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    

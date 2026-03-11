from flask import Flask, render_template_string, jsonify
import storage
import subprocess
import json

app = Flask(__name__)

@app.route('/run-test', methods=['POST'])
def run_test():
    try:
        # Lance le script de test manuellement
        subprocess.run(["python3", "tester.py"], check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.get("/")
def dashboard():
    runs = storage.get_recent_runs()
    chart_runs = runs[::-1]
    labels = [r[1].split()[1] for r in chart_runs]
    data_points = [r[3] for r in chart_runs]
    
    # Préparation des données pour l'export JSON
    json_data = []
    for r in runs:
        json_data.append({"id": r[0], "date": r[1], "api": r[2], "latency": r[3], "success": bool(r[4])})

    html_code = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Monitoring Agify</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f8fafc; margin: 0; padding: 40px; }
            .container { max-width: 900px; margin: auto; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
            h1 { font-size: 24px; color: #0f172a; margin: 0; }
            .actions { display: flex; gap: 10px; }
            .card { background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 20px; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th { text-align: left; font-size: 12px; color: #64748b; text-transform: uppercase; padding: 12px; }
            td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
            .btn { border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; transition: 0.2s; }
            .btn-primary { background: #4f46e5; color: white; }
            .btn-secondary { background: #e2e8f0; color: #475569; }
            .btn:hover { opacity: 0.8; }
            .status-ok { color: #15803d; font-weight: 600; }
            .status-err { color: #b91c1c; font-weight: 600; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Monitoring Agify</h1>
                <div class="actions">
                    <button class="btn btn-secondary" onclick="exportJSON()">Exporter JSON</button>
                    <button class="btn btn-primary" onclick="triggerTest()">Lancer un test</button>
                </div>
            </div>
            
            <div class="card">
                <canvas id="latencyChart" height="100"></canvas>
            </div>

            <div class="card">
                <table>
                    <thead>
                        <tr><th>Heure</th><th>Latence</th><th>Statut</th></tr>
                    </thead>
                    <tbody>
                        {% for run in runs %}
                        <tr>
                            <td>{{ run[1] }}</td>
                            <td>{{ run[3] }} ms</td>
                            <td class="{{ 'status-ok' if run[4] == 1 else 'status-err' }}">
                                {{ "Operationnel" if run[4] == 1 else "Erreur" }}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <script>
            function triggerTest() {
                const btn = document.querySelector('.btn-primary');
                btn.innerText = "En cours...";
                btn.disabled = true;
                fetch('/run-test', { method: 'POST' })
                    .then(() => location.reload())
                    .catch(() => { alert('Erreur'); btn.disabled = false; btn.innerText = "Lancer un test"; });
            }

            function exportJSON() {
                const data = {{ json_data|tojson }};
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'api_stats.json';
                a.click();
            }

            const ctx = document.getElementById('latencyChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: {{ labels|tojson }},
                    datasets: [{
                        label: 'Latence (ms)',
                        data: {{ data_points|tojson }},
                        borderColor: '#4f46e5',
                        backgroundColor: 'rgba(79, 70, 229, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code, runs=runs, labels=labels, data_points=data_points, json_data=json_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

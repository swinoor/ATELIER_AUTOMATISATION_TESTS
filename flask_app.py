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
        return jsonify({"status": "error", "message": str(e)}), 500

@app.get("/")
def dashboard():
    runs = storage.get_recent_runs()
    
    # On prépare les données pour le graphique (ordre chronologique)
    chart_runs = runs[::-1]
    
    # ICI : On récupère les ID des tests pour l'axe du bas
    labels = [f"Test {r[0]}" for r in chart_runs] 
    data_points = [r[3] for r in chart_runs]
    
    json_data = []
    for r in runs:
        json_data.append({
            "id": r[0], 
            "date": r[1], 
            "api": r[2], 
            "latency": r[3], 
            "success": bool(r[4])
        })

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
            .card { background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; }
            th { text-align: left; font-size: 12px; color: #64748b; text-transform: uppercase; padding: 12px; border-bottom: 1px solid #f1f5f9; }
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
                    <button class="btn btn-primary" id="testBtn" onclick="triggerTest()">Lancer un test</button>
                </div>
            </div>
            
            <div class="card">
                <canvas id="latencyChart" height="100"></canvas>
            </div>

            <div class="card" style="padding: 0;">
                <table>
                    <thead>
                        <tr>
                            <th style="padding-left: 20px;">ID</th>
                            <th>Date / Heure</th>
                            <th>Latence</th>
                            <th>Statut</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for run in runs %}
                        <tr>
                            <td style="padding-left: 20px; color: #64748b;">#{{ run[0] }}</td>
                            <td>{{ run[1] }}</td>
                            <td style="font-weight: 600;">{{ run[3] }} ms</td>
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
                const btn = document.getElementById('testBtn');
                btn.innerText = "En cours...";
                btn.disabled = true;
                fetch('/run-test', { method: 'POST' })
                    .then(response => {
                        if(response.ok) location.reload();
                        else alert('Erreur lors du test');
                    })
                    .catch(() => {
                        alert('Erreur réseau');
                        btn.disabled = false;
                        btn.innerText = "Lancer un test";
                    });
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
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: '#4f46e5'
                    }]
                },
                options: {
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: { 
                            beginAtZero: true,
                            title: { display: true, text: 'Latence (ms)' }
                        },
                        x: {
                            title: { display: true, text: 'Numero du test' }
                        }
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code, runs=runs, labels=labels, data_points=data_points, json_data=json_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

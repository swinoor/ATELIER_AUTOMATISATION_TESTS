from flask import Flask, render_template_string
import storage
import json

app = Flask(__name__)

@app.get("/")
def dashboard():
    runs = storage.get_recent_runs()
    
    # On inverse l'ordre pour que le graphique aille de gauche à droite (du plus vieux au plus récent)
    chart_runs = runs[::-1]
    labels = [r[1].split()[1] for r in chart_runs] # On ne garde que l'heure
    data_points = [r[3] for r in chart_runs] # La latence
    
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
            h1 { font-size: 24px; color: #0f172a; margin-bottom: 20px; }
            .card { background: white; border-radius: 12px; shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; padding: 20px; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th { text-align: left; font-size: 12px; color: #64748b; text-transform: uppercase; padding: 12px; border-bottom: 20px; }
            td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
            .status-ok { color: #15803d; font-weight: 600; }
            .status-err { color: #b91c1c; font-weight: 600; }
            .btn { background: #0f172a; color: white; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; float: right; }
        </style>
    </head>
    <body>
        <div class="container">
            <button class="btn" onclick="location.reload()">Actualiser</button>
            <h1>Monitoring Agify</h1>
            
            <div class="card">
                <canvas id="latencyChart" height="100"></canvas>
            </div>

            <div class="card">
                <table>
                    <thead>
                        <tr>
                            <th>Heure</th>
                            <th>Latence</th>
                            <th>Statut</th>
                        </tr>
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
                },
                options: {
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_code, runs=runs, labels=labels, data_points=data_points)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

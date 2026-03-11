from flask import Flask, render_template_string
import storage

app = Flask(__name__)

@app.get("/")
def dashboard():
    runs = storage.get_recent_runs()
    
    html_code = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard Agify</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f8fafc; margin: 0; padding: 40px; color: #1e293b; }
            .container { max-width: 800px; margin: auto; }
            .api-badge { background-color: #e0e7ff; color: #4338ca; padding: 4px 12px; border-radius: 6px; font-size: 14px; font-weight: 600; display: inline-block; margin-bottom: 10px; }
            h1 { margin: 0 0 30px 0; font-size: 28px; color: #0f172a; }
            .card { background: white; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); overflow: hidden; border: 1px solid #e2e8f0; }
            table { width: 100%; border-collapse: collapse; text-align: left; }
            th { background-color: #f1f5f9; padding: 16px; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }
            td { padding: 16px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
            .status { padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; text-transform: uppercase; }
            .status-ok { background-color: #dcfce7; color: #15803d; }
            .status-err { background-color: #fee2e2; color: #b91c1c; }
            .latency { font-weight: 600; color: #475569; }
            .refresh-area { text-align: right; margin-bottom: 15px; }
            .btn { background-color: #0f172a; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 14px; transition: opacity 0.2s; }
            .btn:hover { opacity: 0.8; }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="api-badge">Projet Atelier M1</span>
            <h1>Suivi de l'API : Agify</h1>
            
            <div class="refresh-area">
                <button class="btn" onclick="location.reload()">Actualiser</button>
            </div>

            <div class="card">
                <table>
                    <thead>
                        <tr>
                            <th>Horodatage</th>
                            <th>Latence</th>
                            <th>Etat du service</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for run in runs %}
                        <tr>
                            <td>{{ run[1] }}</td>
                            <td class="latency">{{ run[3] }} ms</td>
                            <td>
                                <span class="status {{ 'status-ok' if run[4] == 1 else 'status-err' }}">
                                    {{ "Operationnel" if run[4] == 1 else "Erreur" }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_code, runs=runs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

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
        <title>API Monitor - Agify</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f0f2f5; margin: 0; padding: 40px; color: #1a1a1a; }
            .container { max-width: 900px; margin: auto; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
            h1 { margin: 0; font-size: 24px; color: #111827; }
            .refresh-btn { background-color: #4f46e5; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: 600; transition: background 0.2s; }
            .refresh-btn:hover { background-color: #4338ca; }
            .card { background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); overflow: hidden; }
            table { width: 100%; border-collapse: collapse; text-align: left; }
            th { background-color: #f9fafb; padding: 15px; font-size: 12px; text-transform: uppercase; color: #6b7280; border-bottom: 1px solid #edf2f7; }
            td { padding: 15px; border-bottom: 1px solid #edf2f7; font-size: 14px; }
            .status { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
            .status-ok { background-color: #dcfce7; color: #166534; }
            .status-err { background-color: #fee2e2; color: #991b1b; }
            .latency { color: #6b7280; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 API Monitor : Agify</h1>
                <button class="refresh-btn" onclick="location.reload()">Actualiser</button>
            </div>
            <div class="card">
                <table>
                    <thead>
                        <tr>
                            <th>Date & Heure</th>
                            <th>API</th>
                            <th>Latence</th>
                            <th>Statut</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for run in runs %}
                        <tr>
                            <td>{{ run[1] }}</td>
                            <td><strong>{{ run[2] }}</strong></td>
                            <td class="latency">{{ run[3] }} ms</td>
                            <td>
                                <span class="status {{ 'status-ok' if run[4] == 1 else 'status-err' }}">
                                    {{ "OPÉRATIONNEL" if run[4] == 1 else "ÉCHEC" }}
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

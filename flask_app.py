from flask import Flask, render_template_string
import storage

app = Flask(__name__)

@app.get("/")
def dashboard():
    runs = storage.get_recent_runs()
    html_code = """
    <html>
        <head>
            <title>Dashboard API</title>
            <style>
                body { font-family: sans-serif; margin: 40px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 10px; }
                th { background-color: #f4f4f4; }
                .pass { color: green; }
                .fail { color: red; }
            </style>
        </head>
        <body>
            <h1>Historique des tests Agify</h1>
            <table>
                <tr><th>ID</th><th>Date</th><th>API</th><th>Latence (ms)</th><th>Statut</th></tr>
                {% for run in runs %}
                <tr>
                    <td>{{ run[0] }}</td><td>{{ run[1] }}</td><td>{{ run[2] }}</td><td>{{ run[3] }}</td>
                    <td class="{{ 'pass' if run[4] == 1 else 'fail' }}">
                        {{ "OK" if run[4] == 1 else "ERREUR" }}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """
    return render_template_string(html_code, runs=runs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

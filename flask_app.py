from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

from flask import Flask, render_template_string
import storage

app = Flask(__name__)

@app.get("/")
def dashboard():
    runs = storage.get_recent_runs()
    
    html_code = """
    <html>
        <head>
            <title>Mon Dashboard API</title>
            <style>
                body { font-family: sans-serif; margin: 20px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #f4f4f4; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .pass { color: green; font-weight: bold; }
                .fail { color: red; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Résultats des tests Agify</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Date</th>
                    <th>API</th>
                    <th>Latence (ms)</th>
                    <th>Résultat</th>
                </tr>
                {% for run in runs %}
                <tr>
                    <td>{{ run[0] }}</td>
                    <td>{{ run[1] }}</td>
                    <td>{{ run[2] }}</td>
                    <td>{{ run[3] }}</td>
                    <td class="{{ 'pass' if run[4] == 1 else 'fail' }}">
                        {{ "✅ PASS" if run[4] == 1 else "❌ FAIL" }}
                    </td>
                </tr>
                {% endfor %}
            </table>
            <br>
            <button onclick="location.reload()">Rafraîchir les données</button>
        </body>
    </html>
    """
    return render_template_string(html_code, runs=runs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

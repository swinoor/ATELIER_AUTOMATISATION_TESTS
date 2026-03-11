from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

from flask import Flask, render_template_string
import storage

Entendu, voici le code de ton fichier flask_app.py parfaitement propre, sans aucun commentaire (pas de #), avec la page du prof à l'accueil et tes résultats sur /dashboard.

Python

from flask import Flask, render_template, render_template_string
import storage

app = Flask(__name__)

@app.get("/")
def consignes():
    return render_template('consignes.html')

@app.get("/dashboard")
def dashboard():
    runs = storage.get_recent_runs()
    
    html_code = """
    <html>
        <head>
            <title>Mon Dashboard API</title>
            <style>
                body { font-family: sans-serif; margin: 40px; background-color: #f4f7f6; }
                .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #007bff; color: white; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .pass { color: green; font-weight: bold; }
                .fail { color: red; font-weight: bold; }
                .back-btn { display: inline-block; margin-bottom: 20px; text-decoration: none; color: #007bff; }
            </style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-btn">← Retour aux consignes</a>
                <h1>Resultats des tests Agify</h1>
                <table>
                    <tr><th>ID</th><th>Date</th><th>API</th><th>Latence (ms)</th><th>Statut</th></tr>
                    {% for run in runs %}
                    <tr>
                        <td>{{ run[0] }}</td>
                        <td>{{ run[1] }}</td>
                        <td>{{ run[2] }}</td>
                        <td>{{ run[3] }}</td>
                        <td class="{{ 'pass' if run[4] == 1 else 'fail' }}">
                            {{ "OK" if run[4] == 1 else "ERREUR" }}
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_code, runs=runs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

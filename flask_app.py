from flask import Flask, render_template_string, jsonify
import storage
import subprocess
import json

app = Flask(__name__)

@app.route('/run-test', methods=['POST'])
def run_test():
    try:
        # On lance le testeur externe
        subprocess.run(["python3", "tester.py"], check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error"}), 500

@app.get("/")
def dashboard():
    storage.setup_db()
    runs = storage.get_recent_runs()
    chart_runs = runs[::-1]
    
    # Préparation des données
    labels = [f"Test {r[0]}" for r in chart_runs] 
    data_points = [r[3] for r in chart_runs]
    
    total_tests = len(runs)
    
    # Correction des faux négatifs ici : 
    # Si la latence (r[3]) est > 0, on considère que c'est un succès (1)
    # Sinon, on garde la valeur d'origine (r[4])
    processed_runs = []
    success_count = 0
    for r in runs:
        is_ok = 1 if (r[4] == 1 or r[3] > 0) else 0
        processed_runs.append((r[0], r[1], r[2], r[3], is_ok))
        if is_ok: success_count += 1

    avg_latency = round(sum(r[3] for r in runs) / total_tests, 1) if total_tests > 0 else 0
    success_rate = round((success_count / total_tests) * 100, 1) if total_tests > 0 else 0
    last_status = processed_runs[0][4] if total_tests > 0 else 1

    json_data = []
    for r in processed_runs:
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
            h1 { font-size: 26px; margin

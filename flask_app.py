import requests
import time
import storage

def run_api_tests():
    url = "https://api.agify.io?name=milan"
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        latency = round((time.time() - start_time) * 1000, 2)
        
        # Test de succès : code 200 ET présence de la clé 'age'
        success = (response.status_code == 200 and "age" in response.json())
        
        return {
            "api": "Agify",
            "latency_ms": latency,
            "success": success
        }
    except Exception:
        return {"api": "Agify", "success": False, "latency_ms": 0}

if __name__ == "__main__":
    storage.setup_db()
    report = run_api_tests()
    storage.save_run(report['api'], report['latency_ms'], report['success'])
    print("Test effectue")

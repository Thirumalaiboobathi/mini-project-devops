from flask import Flask, jsonify
import requests
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')

@app.route('/')
def home():
    return jsonify(message="Welcome to the API Gateway!")


@app.route('/favicon.ico')
def favicon():
    return '', 204  # Prevents 404 from browser favicon requests

@app.route('/weather')
def proxy_weather():
    try:
        res = requests.get("http://weather-service:5001/weather", timeout=3)
        res.raise_for_status()
        return jsonify(res.json())
    except requests.RequestException as e:
        return jsonify(error="Weather service unavailable", details=str(e)), 502

@app.route('/alert')
def proxy_alert():
    try:
        res = requests.get("http://alert-service:5000/alert", timeout=3)
        res.raise_for_status()
        return jsonify(res.json())
    except requests.RequestException as e:
        return jsonify(error="Alert service unavailable", details=str(e)), 502

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

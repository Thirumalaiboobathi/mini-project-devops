from flask import Flask, jsonify
import requests
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')  # Track metrics by endpoint

@app.route('/')
def root():
    return 'WeatherService is up.', 200  # Avoids 404 on root path

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Prevents 404 from browser favicon requests

@app.route('/weather')
def get_weather():
    try:
        res = requests.get("https://api.openweathermap.org/data/2.5/weather?q=London&appid=demo")
        res.raise_for_status()
        data = res.json()
        return jsonify({
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"]
        })
    except requests.exceptions.RequestException as e:
        return jsonify(error="Failed to fetch weather data", details=str(e)), 500

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

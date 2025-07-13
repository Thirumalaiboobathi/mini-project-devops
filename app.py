from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')

# ✅ Define a Prometheus gauge for the heat alert
heat_alert_metric = Gauge('heat_alert_active', '1 if heat alert is active, else 0')

@app.route('/alert')
def get_alert():
    temp = 35  # Simulated temp
    if temp > 30:
        heat_alert_metric.set(1)  # Set metric to 1 for alert
        return jsonify(alert="Heat alert!"), 200
    else:
        heat_alert_metric.set(0)  # Set to 0 if no alert
        return jsonify(alert="Normal"), 200

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

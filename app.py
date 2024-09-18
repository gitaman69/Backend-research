from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if not file.filename.endswith('.csv'):
        return 'Invalid file type. Only CSV files are allowed.', 400

    try:
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    except Exception as e:
        return f"Error reading CSV file: {e}", 500

    matching_indices = []
    matching_values = []
    
    for i in range(0, len(df) - 3):
        if df.iloc[i, 0] == df.iloc[i + 1, 0] == df.iloc[i + 2, 0] == df.iloc[i + 3, 0]:
            matching_indices.append(i)
            matching_values.append(df.iloc[i, 0])  # Store the value of the matching rows

    chart_data = [{"index": i, "value": v} for i, v in enumerate(df.iloc[:, 0])]

    return jsonify({
        'chartData': chart_data,
        'matchingIndices': matching_indices,
        'matchingValues': matching_values,
    })

@app.route('/detect_anomalies', methods=['POST'])
def detect_anomalies():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if not file.filename.endswith('.csv'):
        return 'Invalid file type. Only CSV files are allowed.', 400

    try:
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    except Exception as e:
        return f"Error reading CSV file: {e}", 500

    values = df.iloc[:, 0]
    mean = values.mean()
    std = values.std()
    threshold_high = mean + 2 * std
    threshold_low = mean - 2 * std
    anomalies = values[(values > threshold_high) | (values < threshold_low)]
    
    anomaly_indices = anomalies.index.tolist()
    anomaly_values = anomalies.tolist()  # Store the actual anomaly values

    return jsonify({
        'anomalyIndices': anomaly_indices,
        'anomalies': anomaly_values,
        'thresholds': {'high': threshold_high, 'low': threshold_low},
        'allValues': values.tolist()
    })



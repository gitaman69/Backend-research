from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io

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
        # Read file content into a pandas DataFrame
        df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    except Exception as e:
        return f"Error reading CSV file: {e}", 500

    matching_indices = []
    for i in range(0, len(df) - 3):
        if df.iloc[i, 0] == df.iloc[i + 1, 0] == df.iloc[i + 2, 0] == df.iloc[i + 3, 0]:
            matching_indices.append(i)

    chart_data = [{"index": i, "value": v} for i, v in enumerate(df.iloc[:, 0])]

    return jsonify({
        'chartData': chart_data,
        'matchingIndices': matching_indices
    })

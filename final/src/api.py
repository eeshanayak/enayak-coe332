import json
from flask import Flask, request
import jobs
import requests
import pandas as pd
import uuid

app = Flask(__name__)

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job['store_input'], job['start_date'], job['end_date']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

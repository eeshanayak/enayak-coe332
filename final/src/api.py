import json
from flask import Flask, request
import jobs
import requests
import pandas as pd
import uuid

app = Flask(__name__)

#response = request.get('https://data.austintexas.gov/resource/48iy-4sbg.json')
#data = json.loads(response.text)

@app.route('/', methods=['GET'])
def get_data():
    uri = 'https://data.austintexas.gov/resource/48iy-4sbg.json'
    uResponse = requests.get(uri)
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    df = pd.read_json(uri)
    df['uuid'] = uuid.uuid4() 

    # rd.set('data', json.dumps(data))
    return df.to_string()

@app.route('/select', methods=['GET'])

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job['start'], job['end']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

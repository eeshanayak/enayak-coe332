import json
from flask import Flask, request
import jobs
import requests
import pandas as pd
import uuid
import redis
from tabulate import tabulate


app = Flask(__name__)
rd_jobs = redis.StrictRedis(host='10.106.219.157', port='6379', db=0)


@app.route('/jobs', methods=['GET'])
def get_jobs():
    all_jobs = ''

    for key in rd_jobs.keys():
        all_jobs += key.decode('utf-8')
    #redis_dict = {}
    #for key in rd_jobs.keys():
    #    redis_dict[str(key.decode('utf-8'))] = {}
    #    redis_dict[str(key.decode('utf-8'))]['store_input'] = rd_jobs.hget(key, 'store_input').decode('utf-8')
    #    redis_dict[str(key.decode('utf-8'))]['start_date'] = rd_jobs.hget(key, 'start_date').decode('utf-8')
    #    redis_dict[str(key.decode('utf-8'))]['end_date'] = rd_jobs.hget(key, 'end_date').decode('utf-8')
    #    redis_dict[str(key.decode('utf-8'))]['status'] = rd.hget(key, 'status').decode('utf-8')
    #return json.dumps(redis_dict, indent=4)

    return all_jobs

@app.route('/select', methods=['GET'])
def select_job():
    jid = request.args.get('jid')
    summary_json = (rd_jobs.hget(jobs._generate_job_key(jid), 'summary json'))
    
    summary_df = pd.read_json(summary_json)
    
    return summary_df.to_markdown()

# allows user to create a post request with store input, start date, and end date as parameters for analysis
@app.route('/run', methods=['POST'])
def run_job():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(jobs.add_job(job['store_input'], job['start_date'], job['end_date']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

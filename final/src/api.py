import json
from flask import Flask, request
import jobs
import requests
import pandas as pd
import redis
from tabulate import tabulate

app = Flask(__name__)
rd_jobs = redis.StrictRedis(host='10.105.176.3', port='6379', db=0)

# allows user to create a post request with store input, start date, and end date as parameters for analysis
@app.route('/run', methods=['POST'])
def run_job():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
     
    return json.dumps(jobs.add_job(job['store_input'], job['start_date'], job['end_date']))

# returns job id, input parameters, and status of every job
@app.route('/jobs', methods=['GET'])
def get_jobs():
  
    jobs_df = pd.DataFrame()

    for key in rd_jobs.keys():
        row = {}
        jid = (rd_jobs.hget(key, 'id')).decode('utf-8')
        store = (rd_jobs.hget(key, 'store_input')).decode('utf-8')
        start = (rd_jobs.hget(key, 'start_date')).decode('utf-8')
        end = (rd_jobs.hget(key, 'end_date')).decode('utf-8')
        status = (rd_jobs.hget(key, 'status')).decode('utf-8')   
     
        row = {'Job ID':jid, 'Store':store, 'Start Date':start, 'End Date':end, 'Status':status}
        jobs_df = jobs_df.append(row, ignore_index = True)

    return jobs_df.to_markdown()

# shows summary table for job selected by id parameter
@app.route('/select', methods=['GET'])
def select_job():
    jid = request.args.get('jid')
    summary_json = (rd_jobs.hget(jobs._generate_job_key(jid), 'summary json'))
    
    summary_df = pd.read_json(summary_json)
    
    return summary_df.to_markdown()

# allows user to delete job selected by id parameter
@app.route('/delete', methods=['GET'])
def delete_job():
    jid = request.args.get('jid')
    
    rd_jobs.delete(jobs._generate_job_key(jid))

    return 'Job ' + jid + ' has been deleted'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

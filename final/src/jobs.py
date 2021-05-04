import uuid
from hotqueue import HotQueue
import redis
import os
import requests
import json
import pandas as pd

q = HotQueue("queue", host='10.106.219.157', port=6379, db=2)
rd_jobs = redis.StrictRedis(host='10.106.219.157', port=6379, db=0)
rd_data = redis.StrictRedis(host='10.106.219.157', port=6379, db=1)

uri = 'https://data.austintexas.gov/resource/48iy-4sbg.json'
#uResponse = requests.get(uri)
#data = json.loads(uResponse.text)
df = pd.read_json(uri)
df['uuid'] = [uuid.uuid4() for x in range(len(df))]

# rd_data.set('data', json.loads(data))

def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    if type(jid) == bytes:
        jid = jid.decode('utf-8')
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, x):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'x': x
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'x': x.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd_jobs.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(x, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, x)
    # update call to save_job:
    _save_job(_generate_job_key(jid), job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict


def update_job_status(jid, new_status):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, x = rd.hmget(_generate_job_key(jid), 'id', 'status', 'x')
    job = _instantiate_job(jid, status, x)
   
    if(new_status == 'in progress'):
        worker_IP = os.environ.get('WORKER_IP')
        print(worker_IP)
        rd_jobs.hset(_generate_job_key(jid), 'worker', worker_IP)

    if job:
        job['status'] = new_status
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()

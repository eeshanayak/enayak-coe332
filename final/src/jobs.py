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

#import stock and sales data into local dataframe
sales_df = pd.read_csv('sales.csv').fillna(0)
stock_df = pd.read_csv('stock.csv').fillna(0)

#variable to keep a count of stock days
stock_days = stock_df['Date'].nunique()

#import products and subtract 2 days due to transport time
products_df = pd.read_csv('products.csv')
products_df = products_df.set_index('Product')
products_df['wf_shelf_life'] = products_df['shelf_life'] - 2


#consolidate stock and sales into one master file
stock_and_sales_df = pd.merge(sales_df, stock_df,  how='left', left_on = ['Date','Store','Product'], 
                              right_on = ['Date','Store','Product']).fillna(0)


#convert date column to pandas date format
stock_and_sales_df['Date'] = pd.to_datetime(stock_and_sales_df.Date)

#sort dataframe by product, store, and date
stock_and_sales_df = stock_and_sales_df.sort_values(by=['Product','Store','Date'])


def _generate_jid():
    return str(uuid.uuid4())

def _generate_job_key(jid):
    if type(jid) == bytes:
        jid = jid.decode('utf-8')
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, stores, start, end):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'stores': stores,
                'start': start,
                'end': end
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'stores': stores.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
    }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd_jobs.hmset(job_key, job_dict)

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(stores, start, end, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, stores, start, end)
    # update call to save_job:
    _save_job(_generate_job_key(jid), job_dict)
    # update call to queue_job:
    _queue_job(jid)
    return job_dict


def update_job_status(jid, new_status):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, stores, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'stores', 'start', 'end')
    job = _instantiate_job(jid, status, stores, start, end)
   
    if(new_status == 'in progress'):
        worker_IP = os.environ.get('WORKER_IP')
        print(worker_IP)
        rd_jobs.hset(_generate_job_key(jid), 'worker', worker_IP)

    if job:
        job['status'] = new_status
        _save_job(_generate_job_key(job['id']), job)
    else:
        raise Exception()

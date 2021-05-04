import pandas as pd
from jobs import q, rd_jobs, update_job_status, get_stock_and_sales, _generate_job_key
import redis
import time

stock_and_sales_df = get_stock_and_sales()

def subset(store_input, start_date, end_date):
    
    #returns a subset of data that only pertains to what the user input
    subset_df = pd.DataFrame()
    
    subset_df = subset_df.append(stock_and_sales_df.loc[(stock_and_sales_df['Store'] == store_input) 
                                & (start_date <= stock_and_sales_df['Date'])
                                & (stock_and_sales_df['Date'] <= end_date),
                                  ['Date', 'Product','Store','Stock','Sales']])       
    return subset_df

@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')    
   
    store_input = rd_jobs.hget(_generate_job_key(jid), 'store_input')
    start_date = rd_jobs.hget(_generate_job_key(jid), 'start_date')
    end_date = rd_jobs.hget(_generate_job_key(jid), 'end_date')

    subset_df = subset(store_input, start_date, end_date)
    # rd_jobs.hset(jid, 's_test', stock_and_sales)

    update_job_status(jid, 'complete')

execute_job()

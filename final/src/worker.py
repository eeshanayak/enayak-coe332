import pandas as pd
from jobs import q, rd_jobs, update_job_status, get_stock_and_sales, get_products, get_stock_days, _generate_job_key
import redis
import time


def formulas_dynamic(index, counter, date, store, product, stock, sales, shelf_life, output_df):
    
    #initialize new row dictionary
    new_row = {'Date':date, 'Store':store, 'Product':product,'Stock':stock,'Sales':sales}
    
    day_before = index - 1
    shelf_life = int(shelf_life)
    
    #initialize array of 0s for the starts and ends for current row
    starts = [0]*(shelf_life)
    ends = [0]*(shelf_life)
    
    #start one at index start[0] = stock for that day
    starts[0] = stock
    new_row.update({"start1" : starts[0]})
    
    #iterates from start2 onwards, calculate starts and store into array
    for i in range(1 , shelf_life):
        #concatenate "start" with int for current value
        start_col = "start" + str(i + 1)
        
        #concatenate "end" with int for day before value
        end_day_before_col = "end" + str(i)
        
        #logic to calculate start value
        if(counter < i):
            starts[i] = 0
        else:
            starts[i] = output_df.iloc[day_before][end_day_before_col]
        
        #update new row dictionary with new value and name of the start col
        new_row.update({start_col : starts[i]})            
    

    #last end value added to array
    if(starts[shelf_life - 1] - sales < 0):
        ends[shelf_life - 1] = 0
    else:
        ends[shelf_life - 1] = starts[shelf_life - 1] - sales        
        
    last_end_col = "end" + str(shelf_life)
    new_row.update({last_end_col : ends[shelf_life - 1]})
    
    #iterates backwards from second to last end to first end
    for i in reversed (range(shelf_life - 1)):
        sum_starts = 0
        sum_ends = 0
        
        #sum the starts from current iteration to last
        for j in range(i, shelf_life):
            sum_starts += starts[j]
        
        #sum the ends from one iteration after to the last
        for j in range(i + 1, shelf_life):
            sum_ends += ends[j]
            
        #concatenate "end" with iteration for name of column the value is for   
        end_col = "end" + str(i + 1)
        
        #logic to calculate end values
        if(sum_ends == 0 and sum_starts - sales > 0):
            ends[i] = sum_starts - sales
        elif(ends[i + 1] == 0 and sum_starts - sales < 0):
            ends[i] = 0
        else:
            ends[i] = starts[i]
    
        #update new row dictionary with end column name and calculated value
        new_row.update({end_col : ends[i]})
    
    #sum start and end arrays to get the total starts and ends
    total_start = sum(starts)
    total_end = sum(ends)
    
    #set surplus as last end value in array
    surplus = ends[shelf_life - 1]
    
    #gapout is 1 if total end is 0, and 0 otherwise
    if(total_end == 0):
        gapout = 1
    else:
        gapout = 0
    
    #update dictionary with total start, total end, surplus, and gapout calculations
    new_row.update({"total start" : total_start, "total end" : total_end, "surplus" : surplus, "gapout" : gapout})
    
    return new_row

def summary(output_df, products_df):
        
    #calculates aggregate of output dataframe metrics (total stock, total sales, avg sales, surplus, gapout, total start, avg start, total end, avg end)
    summary_df = output_df.groupby(by=['Product'], as_index=False).agg({'Stock':['sum'],'Sales':['sum','mean'],'surplus':['sum'],
                                                   'gapout':['sum'], 'total start':['mean','min'], 'total end':['mean','min']})
    
    #renames columns
    summary_df.columns = ['Product','total_stock', 'total_sales', 'avg_sales', 'surplus', 'gapout',
                         'avg_start','min_start', 'avg_end', 'min_end']
    
    #calculates average stock based on stock days
    summary_df['avg_stock'] = summary_df['total_stock']/get_stock_days()
    
    #calculates surplus percentage
    summary_df['surplus_percentage'] = (summary_df['surplus']/summary_df['total_stock']*100)
    
    #calculates surplus cogs, avg sales, and avg gross sales by mapping to product dataframe
    summary_df['surplus_cogs'] = summary_df.surplus.mul(summary_df.Product.map(products_df.set_index('Product').COGS))
    summary_df['gross_sales'] = summary_df.total_sales.mul(summary_df.Product.map(products_df.set_index('Product').price))
    summary_df['avg_gross_sales'] = summary_df.avg_sales.mul(summary_df.Product.map(products_df.set_index('Product').price))

    summary_df = summary_df.round({'avg_stock':0, 'avg_sales': 0, 'surplus_percentage': 0, 'avg_start':0, 'avg_end':0, 'gross_sales':0,
                                  'avg_gross_sales':0}).reset_index(drop=True)

    return summary_df


@q.worker
def execute_job(jid):
    update_job_status(jid, 'in progress')    
  
    stock_and_sales_df = get_stock_and_sales()
    products_df = get_products()

    rd_jobs.hset(_generate_job_key(jid), 'stock rows', len(stock_and_sales_df))
 
    #finds the maximum shelf life a product can have
    products_df = get_products()
    shelf_life_column = products_df["shelf_life"]
    max_shelf_life = shelf_life_column.max() - 2
   
    output_columns = ['Date','Store','Product','Stock','Sales']
  
    #create columns based on maximum shelf life
    for index in range(max_shelf_life):
        start_index = "start" + str(index + 1)
        end_index = "end" + str(index + 1)
        output_columns.extend([start_index, end_index])
  
    output_columns.extend(['total start','total end','surplus','gapout'])
    output_df = pd.DataFrame(columns = output_columns)

 
    store_input = (rd_jobs.hget(_generate_job_key(jid), 'store_input')).decode("utf-8")
    start_date = (rd_jobs.hget(_generate_job_key(jid), 'start_date')).decode("utf-8")
    end_date = (rd_jobs.hget(_generate_job_key(jid), 'end_date')).decode("utf-8")


    subset_df = stock_and_sales_df.loc[(stock_and_sales_df['Store'] == store_input) 
                           & (start_date <= stock_and_sales_df['Date'])
                           & (stock_and_sales_df['Date'] <= end_date),
                            ['Date', 'Product','Store','Stock','Sales']]


    rd_jobs.hset(_generate_job_key(jid), 'subset rows', len(subset_df))


    #initializes index and counter variables to know where the method is at in the for loop
    index = 0
    counter = 0

    #iterates through every row and runs surplus / gapout formulas
    for index in range (len(subset_df)):

        #creates local variables for values that carry over from subset dataframe to output dataframe
        date = subset_df.iloc[index]['Date']
        product = subset_df.iloc[index]['Product']
        store = subset_df.iloc[index]['Store']
        stock = subset_df.iloc[index]['Stock']
        sales = subset_df.iloc[index]['Sales']
        shelf_life = products_df.loc[product]['wf_shelf_life']
    
        #counter resets to 0 if a new product is being started
        if(index == 0):
            counter = 0
        elif(product != subset_df.iloc[index - 1]['Product']):
            counter = 0

 
        new_row = formulas_dynamic(index, counter, date, store, product, stock, sales, shelf_life, output_df)
        output_df = output_df.append(new_row, ignore_index = True)

        counter += 1
        index += 1
    
    products_df = products_df.reset_index()
    
    output_json = output_df.to_json()

    summary_df = summary(output_df, products_df)
    summary_json = summary_df.to_json()

    rd_jobs.hset(_generate_job_key(jid), 'output json', output_json)
    rd_jobs.hset(_generate_job_key(jid), 'summary json', summary_json)

    update_job_status(jid, 'complete')

execute_job()

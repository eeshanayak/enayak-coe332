# Grocery Store Shelf FIFO Model

This app simulates how perishable food items are shelved at grocery stores and tracks how much gets thrown away due to expiration, given the stock and sales data for a time period. It is assumed in this model that the items are sold in priority of earliest expiration.


For example, let’s this was the sample data for a cheesecake

| Day | Stock | Sales |
| --- | --- | --- |
| 0 |	5 | 2 |
| 1 | 3 | 4 |
| 2 | 4 | 1 |
| 3 | 2 | 0 |

If the cheesecake had a 3 day shelf life, this is what it’s model would look like,

| Day | Stock | Sales | start1 | end1 | start2 | end2 | start3 | end3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 2 | 5 | 3 | 0 | 0 | 0 | 0 |
| 1 | 3 | 4 | 3 | 2 | 3 | 0 | 0 | 0 |
| 2 | 4 | 1 | 4 | 4 | 2 | 1 | 0 | 0 |
| 3 | 2 | 0 | 2 | 2 | 2 | 2 | 1 | 1 |

At the end of day 3, there is 1 cheesecake left that is thrown out due to expiration.

This app runs this simulation on a dataset and takes the start date, end date, and location of the store as parameters to generate a business report on how the sales went for the location. The food distributor can use this data to adjust future stocking to minimize surplus (number of food items thrown out due to expiration) and gapout (empty shelves on a day due to selling out).

Instructions on how to deploy and interact with this app are in the docs section.

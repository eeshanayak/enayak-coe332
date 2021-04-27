# Homwork 7

## Part A
I created a Flask deployment and a Worker deployment, and I tested it in the python debug container with this command 
```
curl -X POST -H "content-type: application/json" -d '{"start": "START", "end":"END"}' 10.244.15.48:5000/jobs
```
and the output was 
```
{"id": "632155f5-02a3-4c68-97a0-78616c112cfc", "status": "submitted", "start": "START", "end": "END"}
```
indicating the job was submitted.

## Part B
The jobs are getting executed and the status is getting updated which can be seen in the python debug deployment shell
```
>>> rd.hgetall('job.2342ffc8-0f44-47c4-a445-ebd423f1ccf4')
{b'id': b'2342ffc8-0f44-47c4-a445-ebd423f1ccf4', b'status': b'complete', b'start': b'START', b'end': b'END'}
```

My goal was to add a worker id hash key to be 'worker IP' in the update job status function if the 'new status' parameter was 'in progress' with this code:
```
if(new_status == 'in progress'):
        worker_IP = os.environ.get('WORKER_IP')
        rd.hset(_generate_job_key(jid), 'worker', 'worker_IP')
```

## Part C
I scaled my worker deployment to 2 pods by adding 
```
replicas: 2
```
to my worker deployment yml. 

To create 10 jobs, I would run this 10 times
```
curl -X POST -H "content-type: application/json" -d '{"start": "START", "end":"END"}' 10.244.15.48:5000/jobs
```

To check which workers worked each pod, I would call
```
rd.hget(jid, 'worker')
```
for each job id, and I would want to see that each one has done 5.

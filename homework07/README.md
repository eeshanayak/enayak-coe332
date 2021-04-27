# Homwork 7

## Part A
I created a Flask deployment and a Worker deployment, and I tested it in the flask deployment container with this command 
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

I then added this code to the ```update_job_status()``` method to assign a worker_IP to each job
```
if(new_status == 'in progress'):
        worker_IP = os.environ.get('WORKER_IP')
        rd.hset(_generate_job_key(jid), 'worker', worker_IP)
```

## Part C
I scaled my worker deployment to 2 pods by adding 
```
replicas: 2
```
to my worker deployment yml. 

To create 10 jobs, I ran the jobs route 10 times in the flask container
```
curl -X POST -H "content-type: application/json" -d '{"start": "START", "end":"END"}' 10.244.15.48:5000/jobs
```

To check which workers worked each pod, I ran 
```
>>> for key in rd.keys():
...    print(key)
...    rd.hget(key, 'worker')
```
The output was 
```
b'job.4247b8e9-85be-4005-833c-42e572d82d8b'
b'10.244.15.228'
b'job.61027b16-b11d-49e4-a7b2-d94331f0fe9e'
b'10.244.13.193'
b'job.18bffade-9d11-42a7-a3e1-d644efb607ac'
b'10.244.13.193'
b'job.67faf223-a14e-4661-95ed-7c86e9426144'
b'10.244.15.228'
b'job.be83e4c4-8110-4060-be4b-202a83cd197e'
b'10.244.15.228'
b'job.35b085b9-3e4a-4d15-a071-29dfbb4eba6d'
b'10.244.13.193'
b'job.fb799d2c-ce54-4e2b-800f-618758de4b0f'
b'10.244.13.193'
b'job.a4b54497-70d5-4dff-a59d-4f189170295b'
b'10.244.15.228'
b'job.fa4f6e47-b5b3-4bdd-8eaa-5cb40a86f7be'
b'10.244.13.193'
b'job.236809e7-5c91-486a-b1d8-e8a83a5937f1'
b'10.244.15.228'
```
which shower that the worker with IP '10.244.15.228' worked 5 jobs and the worker with IP '10.244.13.193' also worked 5 jobs.

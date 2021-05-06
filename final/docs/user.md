# User Instructions

The routes available to interact with this app are

```
/run
/jobs
/output
/summary
/delete
```

## Route: /run
First get the name and IP address of the deployment pod

```
kubectl get pods -o wide

NAME                                            READY   STATUS    RESTARTS   AGE    IP              NODE                         NOMINATED NODE   READINESS GATES
eesha-final-redis-deployment-76d9ff5cf5-c5fxj   1/1     Running   0          4h6m   10.244.13.195   c11                          <none>           <none>
enayak-final-flask-746c85788d-gmnxh             1/1     Running   0          117m   10.244.10.36    c009.rodeo.tacc.utexas.edu   <none>           <none>
enayak-final-worker-8477c756dc-6l5g8            1/1     Running   0          117m   10.244.10.35    c009.rodeo.tacc.utexas.edu   <none>           <none>
```

Then exec into the flask deployment
```
kubectl exec -it enayak-final-flask-746c85788d-gmnxh -- /bin/bash
```

In the flask deployment, curl a POST request giving the parameters of the store location, start date, and end date for analysis.
Currently the sample data has:
Locations: North, South
Dates: 6/10/2020 - 7/24/2020

I created 2 jobs
```
root@enayak-final-flask-746c85788d-gmnxh:/app# curl -X POST -H "content-type: application/json" -d '{"store_input":"North", "start_date": "6/17/2020", "end_date":"7/10/2020"}' 10.244.10.36:5000/run
{"id": "ec323e01-fe0c-4a0d-ae77-97a4a72851e6", "status": "submitted", "store_input": "North", "start_date": "6/17/2020", "end_date": "7/10/2020"}

root@enayak-final-flask-746c85788d-gmnxh:/app# curl -X POST -H "content-type: application/json" -d '{"store_input":"South", "start_date": "6/17/2020", "end_date":"7/10/2020"}' 10.244.10.36:5000/run
{"id": "532456f0-a583-49d6-8b38-186d23ba95c6", curl -X POST -H "content-type: application/json" -d '{"store_input":"South", "start_date": "6/17/2020", "end_date":"7/10/2020"}'
```

## Route: /jobs
```
root@enayak-final-flask-746c85788d-gmnxh:/app# curl 10.244.10.36:5000/jobs
|    | End Date   | Job ID                               | Start Date   | Status   | Store   |
|---:|:-----------|:-------------------------------------|:-------------|:---------|:--------|
|  0 | 7/10/2020  | ec323e01-fe0c-4a0d-ae77-97a4a72851e6 | 6/17/2020    | complete | North   |
|  1 | 7/10/2020  | 532456f0-a583-49d6-8b38-186d23ba95c6 | 6/17/2020    | complete | South   |
```


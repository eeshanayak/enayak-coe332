# Homework 6

## Step 1
I created the redis PVC and applied it using
```
$ kubectl apply -f eesha_n-test-redis-pvc.yml
```

## Step 2
I created the redis deployment and applied it using 
```
$ kubect apply -f eesha_n-test-redis-deployment.yml
```

## Step 3
I created the redis service and applied it using 
```
$ kubectl apply -f eesha_n-test-redis-service.yml
```

I checked my work by getting into my python debug container
```
$ kubectl exec -it py-debug-deployment-5cc8cdd65f-gg2tg -- /bin/bash
```

and then opening the python interactive interpreter
```
python
```

After importing redis in the interpreter, I created a redis client object with the IP Address of my redis service
```
>>> import redis
>>> rd = redis.StrictRedis(host = '10.106.219.157', port = 6379, db = 0)
```

Then to test the persistence, I started by creating a key
```
>>> rd.set('name', 'Eesha')
True
```

Then in another shell, I deleted the redis pod 
```
$ kubectl delete pods eesha-test-redis-deployment-9579cf698-dh8lc
```

Checked to see if a new one had been created 
```
$ kubectl get pods 

NAME                                           READY   STATUS    RESTARTS   AGE
eesha-test-redis-deployment-9579cf698-v8kck    1/1     Running   0          47s
```

And then checked if I could still get the same key in the python debug container shell
```
>>> rd.get('name')
b'eesha'
```

Because I could still retrieve the key with the same service IP after deleting the pod, I knew that the data was persisting.

# Step 4
I created the flask deployment and applied it using 
```
$ kubectl apply -f eesha_n-test-flask-deployment.yml
```

# Step 5
I created the flask service and applied it using 
```
$ kubectl apply -f eesha_n-test-flask-service.yml
```


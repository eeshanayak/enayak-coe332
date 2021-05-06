# Deployment Instructions

Deploy the redis pvc, deployment, and service in deployments/redis

```
kubectl apply -f enayak-final-redis-pvc.yml
kubectl apply -f enayak-final-redis-deployment.yml
kubectl apply -f enayak-final-redis-service.yml
```

Deploy the flask deployment and service in deployments/flask
```
kubectl apply -f enayak-final-flask-service.yml
kubectl apply -f enayak-final-flask-deployment.yml
```

Deploy the worker deployment in deployments/worker
```
kubectl apply -f enayak-final-worker-deployment.yml
```

For instructions on how to interact with the app, read user.md

# Deployment Instructions

First deploy the redis pvc, deployment, and service found in deployments/redis

```
kubectl apply -f enayak-final-redis-pvc.yml
kubectl apply -f enayak-final-redis-deployment.yml
kubectl apply -f enayak-final-redis-service.yml
```



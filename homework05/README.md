# Homework 5

## Part A
1. Create Pod:
```
$kubectl apply -f pod-a.yml
```

2. Get Pod:
```
$kubectl get pods homework05
```
```
NAME         READY   STATUS    RESTARTS   AGE
homework05   1/1     Running   0          10m
```

3. Check Logs:
```
$kubectl logs homework05a
```
```
Hello, 
```
This is what I expected because the name variable has no value right now.

4. Delete Pod
```
$kubectl delete pods homework05a
```
```
pod "homework05a" deleted
```

## Part B
1. Create Pod
```
$kubectl apply -f pod-b.yml
```

2. Check Logs
```
$kubectl logs homework05b
```
```
Hello, Eesha
```

3. Delete Pod
```
$kubectl delete pods homework05b
```
```
pod "homework05b" deleted
```

## Part C
1. Create Deployment
```
$kubectl apply -f homework05c
```

2. Get Pods
```
$kubectl get pods -o wide
```

```
NAME                                    READY   STATUS    RESTARTS   AGE     IP             NODE                         NOMINATED NODE   READINESS GATES
eesha-test-deployment-6d9566c67-2hp7r   1/1     Running   0          33h     10.244.3.48    c01                          <none>           <none>
helloflask-848c4fb54f-7zt2g             1/1     Running   0          3m21s   10.244.10.15   c009.rodeo.tacc.utexas.edu   <none>           <none>
homework05c-7859fd9656-m2hn2            1/1     Running   0          35m     10.244.6.164   c03                          <none>           <none>
py-debug-deployment-5cc8cdd65f-gg2tg    1/1     Running   0          6d9h    10.244.3.175   c01                          <none>           <none>
```

3. Check Logs
```
kubectl logs homework05c-7859fd9656-m2hn2
```
```
Hello, (Eesha) from (10.244.6.164)
```
Yes the IP Address matches part 2.


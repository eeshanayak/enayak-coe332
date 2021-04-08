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
pod "homework05" deleted
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
NAME                                    READY   STATUS    RESTARTS   AGE     IP             NODE   NOMINATED NODE   READINESS GATES
eesha-test-deployment-6d9566c67-2hp7r   1/1     Running   0          33h     10.244.3.48    c01    <none>           <none>
hello-deployment-55f4459bf-8brcp        1/1     Running   201        8d      10.244.4.53    c02    <none>           <none>
hello-deployment-55f4459bf-blh9h        1/1     Running   201        8d      10.244.5.23    c04    <none>           <none>
hello-deployment-55f4459bf-nvqd5        1/1     Running   201        8d      10.244.7.27    c05    <none>           <none>
hello-deployment-55f4459bf-t2sct        1/1     Running   7          7h35m   10.244.3.98    c01    <none>           <none>
helloflask-848c4fb54f-txg2b             1/1     Running   0          6d9h    10.244.3.153   c01    <none>           <none>
homework05b                             1/1     Running   1          78m     10.244.3.128   c01    <none>           <none>
homework05c-7859fd9656-m2hn2            1/1     Running   0          21m     10.244.6.164   c03    <none>           <none>
py-debug-deployment-5cc8cdd65f-gg2tg    1/1     Running   0          6d9h    10.244.3.175   c01    <none>           <none>
```

3. Check Logs
```
kubectl logs homework05c-7859fd9656-m2hn2
```
```
Hello, (Eesha) from (10.244.6.164)
```
Yes the IP Address matches part 2.


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
This is what I expected because the name variable has no value

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

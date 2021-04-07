# Homework 5

## Part A
1. Command:
```
command: ['sh', '-c', 'echo "Hello, $(NAME)" && sleep 3600']
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
$kubectl logs homework05
```
```
Hello, 
```

4. Delete Pod
```
$kubectl delete pods homework05
```
```
pod "homework05" deleted
```

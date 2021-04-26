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

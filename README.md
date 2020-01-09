# Proof of concept for asynchronous processing of long running tasks

## Run containers locally

`docker-compose run --build`

## Deploy containers to K8s

```bash
minikube addons enable ingress

eval $(minikube docker-env)

# Build custom images so that Minikube's docker registry knows about them
docker build -t job-api job-api/

kubectl apply -f kubernetes-all.yml
```

## Trigger job

`curl -X POST -H "Content-Type: application/json" -d '{"name": "test job", "parameters": {}}' http://localhost:8080/jobs`

## Get job status

`curl localhost:8080/jobs`

## Manually update job status

__Note: This is just for debugging, in reality the worker would do that__

`curl -X PATCH -H "Content-Type: application/json" -d '{"status": "done"}' http://localhost:8080/jobs/1`
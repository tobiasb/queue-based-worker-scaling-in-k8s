# Proof of concept for asynchronous processing of long running tasks

## Run containers locally

`docker-compose run --build`

## Trigger job

`curl -X POST -H "Content-Type: application/json" -d '{"name": "test job", "parameters": {}}' http://localhost:8080/jobs`

## Get job status

`curl localhost:8080/jobs`

## Manually update job status

__Note: This is just for debugging, in reality the worker would do that__

`curl -X PATCH -H "Content-Type: application/json" -d '{"status": "done"}' http://localhost:8080/jobs/1`
# Proof of concept for scaling queue workers in Kubernetes

What if we needed a system for long running work with an interface to determine work processing status.

Goals:
- There exists an API to trigger long running jobs
- There exists an API to retrieve job status and results
- Jobs are processed in parallel by medium CPU/high memory workers
- Idle workers are being scaled in timely
- Busy workers are not being killed prematurely

## How to run
### Run containers locally

_Note that this will only run the Job API and a single worker. Autoscaling can't be done using docker-compose. Deploy to K8s instead._

`docker-compose up --build`

`export JOBAPI_HOST=localhost:8080`

### Deploy containers to K8s (e.g. Minukube)

```bash
minikube addons enable ingress

eval $(minikube docker-env)
```

Build custom images so that Minikube's docker registry knows about them. Do this every time you make code changes.

`./docker-build-all.sh`

Apply deployments, services and ingress

`kubectl apply -f kubernetes-all.yml`

Get local cluster IP address
```
kubectl get ingress

NAME             HOSTS   ADDRESS        PORTS   AGE
jobapi-ingress   *       192.168.64.4   80      3m2s
```

`export JOBAPI_HOST=192.168.64.4/jobapi`

Shorthand to rebuild, redeploy, restart everything:

`./docker-build-all.sh && kubectl apply -f kubernetes-all.yml && kubectl rollout restart deployment/autoscaler deployment/worker deployment/jobapi`

### Deploy to GKS

Push the local images to GCR:

`./docker-build-all.sh && ./docker-push-all.sh`

Update image revision in `kubernetes-all-gcp.yml` with new ones from your cloud image registry.

__NOTE: Currently the ingress resource has to be created manually because I haven't figured out how to use the `nginx ingress controller` in GKS.__

`export JOBAPI_HOST=34.107.191.158`

Execute the following and paste the content of `kubernetes-all-gcp.yml`:

`rm deployment.yml && vi deployment.yml && kubectl apply -f deployment.yml`

## Using the API

### Get Job API status

`curl $JOBAPI_HOST/status`

### Trigger job

`curl -X POST -H "Content-Type: application/json" -d '{"name": "test job", "parameters": {"delay":30}}' $JOBAPI_HOST/jobs`

`"delay":30` will cause the worker to pause for 30 seconds. This way we can simulate long running tasks.

### Get all jobs and their statuses

`curl $JOBAPI_HOST/jobs`

### Delete jobs

`curl -X DELETE $JOBAPI_HOST/jobs`

### Manually update job status

_Note: This is just for debugging, in reality the worker would do that_

`curl -X PATCH -H "Content-Type: application/json" -d '{"status": "done"}' $JOBAPI_HOST/jobs/1`

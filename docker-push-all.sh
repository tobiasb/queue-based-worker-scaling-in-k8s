#!/bin/bash

docker tag job-api eu.gcr.io/tobiasb-test-project/tobiasb/job-api
docker push eu.gcr.io/tobiasb-test-project/tobiasb/job-api

docker tag worker eu.gcr.io/tobiasb-test-project/tobiasb/worker
docker push eu.gcr.io/tobiasb-test-project/tobiasb/worker

docker tag autoscaler eu.gcr.io/tobiasb-test-project/tobiasb/autoscaler
docker push eu.gcr.io/tobiasb-test-project/tobiasb/autoscaler

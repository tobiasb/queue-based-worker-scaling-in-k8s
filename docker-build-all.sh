#!/bin/bash

docker build -t job-api job-api/
docker build -t worker worker/
docker build -t autoscaler autoscaler/

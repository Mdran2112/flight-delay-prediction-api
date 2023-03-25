#!/bin/bash

docker build --tag=flights-prediction-api .
docker image prune -f
#!/bin/bash

./wait-for.sh pgdb:5432 -- python ./load-data.py
./wait-for.sh minio:9000 -- ./load-track-data.sh

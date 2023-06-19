#!/bin/bash

# Download the data
curl -o /data/f1db_csv.zip http://ergast.com/downloads/f1db_csv.zip

# Unzip the data
unzip -o /data/f1db_csv.zip -d /data/f1dbcsv

# Wait for MinIO to be ready
/wait-for localhost:9000 -t 60

# Configure MinIO client
mc alias set minio http://minio:9000 minioadmin minioadmin

# Create bucket
mc mb minio/track.data-raw

# Copy data to the bucket
mc cp --recursive /data/f1dbcsv/ minio/track.data-raw

# Remove the objects from the bucket f1dbcsv
mc rm --force --recursive minio/f1dbcsv

# Remove the bucket
mc rb --force minio/f1dbcsv

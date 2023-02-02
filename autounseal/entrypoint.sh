#!/bin/bash

# This script is used to start the autounseal service. It is used by the Dockerfile.
sleep 5;

while true; do
    python3 /app/autounseal.py;
    sleep $INTERVAL;
done

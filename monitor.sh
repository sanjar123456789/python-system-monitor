#!/bin/bash

while true
do
    start_time=$SECONDS

    echo "Starting system monitoring..."

    python system_monitor.py 2>> error.log

    if [ $? -ne 0 ]; then
        echo "Monitoring failed!"
    fi

    elapsed=$((SECONDS - start_time))
    remaining=$((10 - elapsed))

    if [ "$remaining" -gt 0 ]; then
        sleep "$remaining"
    fi
done

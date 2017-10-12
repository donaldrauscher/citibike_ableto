#!/bin/bash

# Prepare log files and start outputting logs to stdout
#touch logs/gunicorn.log
#touch logs/access.log
#tail -n 0 -f logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn app:app \
    --name citibike \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --preload \
    --worker-class gevent \
    --timeout 240 \
    --log-level=info \
    "$@"

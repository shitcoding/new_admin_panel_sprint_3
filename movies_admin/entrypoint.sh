#!/bin/sh

if [ "$MODE" = "prod" ]; then
    make run-gunicorn-docker
elif [ "$MODE" = "dev" ]; then
    make run-dev-server-docker
else
    echo "Unknown MODE: $MODE. Set \$MODE to 'dev' or 'prod'."
    exit 1
fi

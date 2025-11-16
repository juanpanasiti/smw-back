#!/bin/bash

# Make git pull
git pull

# Install dependencies
./env/bin/python -m pip install -r requirements.txt
./env/bin/python -m pip install gunicorn

# Upgrade DB
./env/bin/python -m alembic upgrade head

# Kill old server
kill $(lsof -t -i :8000) || echo "There are no process running on port 8000"

# run server
BUILD_ID=dontKillMe
./env/bin/python -m gunicorn src.entrypoints.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 > /dev/null 2>&1 &

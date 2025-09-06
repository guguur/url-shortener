#!/bin/bash
set -e

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT} --reload
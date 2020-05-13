#!/bin/sh

PORT=1488
WORKERS=2
exec gunicorn -b :"${PORT}" --timeout 600 -k uvicorn.workers.UvicornWorker --workers "${WORKERS}" --access-logfile ./gunicorn_access.log --error-logfile ./gunicorn_error.log app:APP --log-level DEBUG

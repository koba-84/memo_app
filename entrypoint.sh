#!/usr/bin/env bash
set -e
alembic upgrade head
exec gunicorn "app:app" -w 2 -b 0.0.0.0:5000 --threads 4

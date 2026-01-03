#!/bin/bash

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port ${USER_SERVICE_INTERNAL_PORT}
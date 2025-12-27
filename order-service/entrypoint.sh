#!/bin/bash

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port ${ORDER_SERVICE_INTERNAL_PORT}
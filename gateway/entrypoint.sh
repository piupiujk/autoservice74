#!/bin/bash

exec uvicorn app.main:app --host 0.0.0.0 --port ${GATEWAY_INTERNAL_PORT}
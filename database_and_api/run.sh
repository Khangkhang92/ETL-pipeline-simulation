#! /bin/bash

worker=${WORKER:-1}
port=${PORT:-8000}

# Run migration
poetry run alembic upgrade head

# Start server
poetry run uvicorn main:app --host 0.0.0.0 --port ${port} --workers ${worker} --reload

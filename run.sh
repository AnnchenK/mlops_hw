#!/bin/sh

poetry install

export ADDRESS=0.0.0.0 PORT=8000

poetry run python mlops_dz/__init__.py &
until curl -s -o /dev/null -w "%{http_code}" "http://$ADDRESS:$PORT/alive" | grep -q "200"; do
    sleep 1
done

poetry run streamlit run dashboard/dashboard.py >/dev/null 2>&1

dvc init --no-scm

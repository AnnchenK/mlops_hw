#!/bin/sh

export ADDRESS=0.0.0.0 PORT=8000

poetry run python mlops_dz/__init__.py &
until curl -s -o /dev/null -w "%{http_code}" "http://$ADDRESS:$PORT/alive" | grep -q "200"; do
    sleep 1
done

poetry run dvc init --no-scm
poetry run dvc remote add -d myremote s3://$MINIO_BUCKET
poetry run dvc remote modify myremote endpointurl http://$MINIO_ENDPOINT
poetry run dvc remote modify --local myremote access_key_id $MINIO_ROOT_USER
poetry run dvc remote modify --local myremote secret_access_key $MINIO_ROOT_PASSWORD

poetry run streamlit run dashboard/dashboard.py >/dev/null 2>&1

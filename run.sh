#!/bin/sh

poetry install

export ADDRESS=0.0.0.0 PORT=8000

poetry run python mlops_dz/__init__.py &
until curl -s -o /dev/null -w "%{http_code}" "http://$ADDRESS:$PORT/alive" | grep -q "200"; do
    sleep 1
done

dvc init --no-scm
dvc remote add -d myremote s3://$MINIO_BUCKET
dvc remote modify myremote endpointurl http://minio:9000/
dvc remote modify --local myremote access_key_id $MINIO_ROOT_USER
dvc remote modify --local myremote secret_access_key $MINIO_ROOT_PASSWORD

poetry run streamlit run dashboard/dashboard.py >/dev/null 2>&1

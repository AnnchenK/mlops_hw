from typing import List
import json
from minio import Minio
from werkzeug.utils import secure_filename
import os
import io

ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.environ.get("MINIO_BUCKET")
MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")

def data_commit(X: List[List[float]], y: List[float]) -> None:
    client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)
    content = json.dumps({'x': X, 'y': y}, indent=2).encode('utf-8')
    print('commit')
    # Make bucket if not exist.
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    else:
        print(f"Bucket {BUCKET_NAME} already exists")

    with io.BytesIO(content) as file:
        filename = secure_filename('name')
        size = len(content)
        client.put_object(BUCKET_NAME, filename, file, size)
        print(f"{filename} is successfully uploaded to bucket {BUCKET_NAME}.")
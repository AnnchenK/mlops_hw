from typing import List
import json
from minio import Minio
from werkzeug.utils import secure_filename
import os
import io
import subprocess

class DVC:
    def __init__(self):
        self.ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
        self.SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
        self.BUCKET_NAME = os.environ.get("MINIO_BUCKET")
        self.MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")

    def data_commit(self, X: List[List[float]], y: List[float]) -> None:
        client = Minio(self.MINIO_API_HOST, self.ACCESS_KEY, self.SECRET_KEY, secure=False)
        content = json.dumps({'x': X, 'y': y}, indent=2).encode('utf-8')
        
        # Make bucket if not exist.
        found = client.bucket_exists(self.BUCKET_NAME)
        if not found:
            client.make_bucket(self.BUCKET_NAME)

        if not os.path.exists(os.path.join(os.getcwd(), 'data')):
            os.mkdir('./data/')

        with open('./data/train_data.json', 'w') as f:
            json.dump({'x': X, 'y': y}, f)

        with io.BytesIO(content) as file:
            filename = secure_filename('name')
            size = len(content)
            client.put_object(self.BUCKET_NAME, filename, file, size)
            print(f"{filename} is successfully uploaded to bucket {self.BUCKET_NAME}.")

            subprocess.run(["dvc", "add", "data"])
            subprocess.run(["dvc", "push"])  
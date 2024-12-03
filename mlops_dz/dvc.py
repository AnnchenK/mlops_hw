from typing import List
import json
from minio import Minio
import os
import subprocess

class DVC:
    def __init__(self, logger):
        self.logger = logger
        self.ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
        self.SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
        self.BUCKET_NAME = os.environ.get("MINIO_BUCKET")
        self.MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")

    def data_commit(self, X: List[List[float]], y: List[float], path='./data', filename='train_data.json') -> None:
        client = Minio(self.MINIO_API_HOST, self.ACCESS_KEY, self.SECRET_KEY, secure=False)
        
        found = client.bucket_exists(self.BUCKET_NAME)
        if not found:
            client.make_bucket(self.BUCKET_NAME)

        if not os.path.exists(os.path.join(os.getcwd(), path)):
            os.mkdir(path)

        with open(path + '/' + filename, 'w') as f:
            json.dump({'x': X, 'y': y}, f)

        self.logger.info(f"save file {path + '/' + filename} locally")

        subprocess.run(["dvc", "add", path.replace('./', '')])
        subprocess.run(["dvc", "push"])

        self.logger.info(f"version file remote")
from fastapi import HTTPException
from uuid import uuid4
import logging


logger = logging.getLogger("uvicorn")
storage = {}


def store_model(model) -> str:
    id = str(uuid4())
    if id in storage:
        raise HTTPException(status_code=500, detail=f"id {id} is already taken")
    storage[id] = model
    logger.info(f"added model with id {id}")
    return id


def del_model(id: str):
    if id in storage:
        raise HTTPException(status_code=404, detail=f"id {id} is already taken")
    del storage[id]
    logger.info(f"removed model with id {id}")


def get_model(id: str):
    if id not in storage:
        raise HTTPException(status_code=404, detail=f"id {id} does not exist")
    return storage[id]

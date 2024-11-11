from models import Model

from fastapi import HTTPException
from typing import Dict
from uuid import uuid4
import logging


_logger = logging.getLogger("uvicorn")
_storage: Dict[str, Model] = {}


def store_model(model: Model) -> str:
    """
      stores a `model` in volatile memory and returns the assigned id
    """
    id = str(uuid4())
    if id in _storage:
        raise HTTPException(status_code=500, detail=f"id {id} is already taken")
    _storage[id] = model
    _logger.info(f"added model with id {id}")
    return id


def del_model(id: str):
    """
      removes the model with `id` from the memory
    """
    if id in _storage:
        raise HTTPException(status_code=404, detail=f"id {id} is already taken")
    del _storage[id]
    _logger.info(f"removed model with id {id}")


def get_model(id: str) -> Model:
    """
      returns the model with `id`
    """
    if id not in _storage:
        raise HTTPException(status_code=404, detail=f"id {id} does not exist")
    return _storage[id]

from models import *

from fastapi import FastAPI
from uuid import uuid4
import logging


logger = logging.getLogger("uvicorn")
app = FastAPI()


@app.post("/add_model?{model}", summary="Add a model")
async def add_model(
    model: Model,
    body: AddModelRequest
) -> AddModelResponse:
    """
      Trains a `model` with `parameters` on the provided `dataset` and saves it. Returns an id assigned to the model.
    """
    model_id = str(uuid4())
    return AddModelResponse(model_id=model_id)


@app.get("/alive", summary="Aliveness check")
async def alive() -> AliveResponse:
    """
      Returns "yes" if the service is alive and is ready to serve requests.
    """
    return "yes"

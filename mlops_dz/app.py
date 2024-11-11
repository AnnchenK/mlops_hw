from schemas import AddModelRequest, AddModelResponse, AliveResponse
from models import ModelNameUnion, validate_params, create_trained_model
from store import store_model


from fastapi import FastAPI, Query, Body, HTTPException
from typing import Annotated
import logging


_logger = logging.getLogger("uvicorn")
app = FastAPI()


@app.post("/add_model", summary="Add a model")
async def add_model(
    model: ModelNameUnion = Query(description="the name of the model to add"),
    body: AddModelRequest = Body()
) -> Annotated[AddModelResponse, "info about the added model"]:
    """
      Trains a `model` with `parameters` on the provided `dataset` and saves it. Returns an id assigned to the model.
    """
    if not validate_params(model, body.parameters):
        raise HTTPException(status_code=422, detail="model was incorrectly configured")

    model = create_trained_model(model, body.parameters, body.dataset.X, body.dataset.y)

    id = store_model(model)
    return AddModelResponse(id=id)


@app.get("/alive", summary="Aliveness check")
async def alive() -> Annotated[AliveResponse, "whether the service is alive"]:
    """
      Returns "yes" if the service is alive and is ready to serve requests.
    """
    return "yes"

from schemas import Id, AddModelRequest, AddModelResponse, PredictRequest, PredictResponse
from models import ModelNameUnion, model_names, validate_params, create_trained_model
from store import store_model, list_all_models, get_model, del_model
from dvc import DVC


from fastapi import FastAPI, Query, Body, HTTPException
from typing import Annotated, List, Literal, Dict
from pydantic import Field
import logging


_logger = logging.getLogger("uvicorn")
app = FastAPI()


@app.post("/add_model", summary="Add a model")
async def add_model(
    model: ModelNameUnion = Query(description="the name of the model to add"),
    body: AddModelRequest = Body()
) -> AddModelResponse:
    """
      Trains a `model` with `parameters` on the provided `dataset` and saves it. Returns an id assigned to the model.
    """
    if not validate_params(model, body.parameters):
        raise HTTPException(status_code=422, detail="model was incorrectly configured")

    model = create_trained_model(model, body.parameters, body.dataset.X, body.dataset.y)
    DVC(_logger).data_commit(body.dataset.X, body.dataset.y, path='./data', filename='train_data.json')

    id = store_model(model)
    return AddModelResponse(id=id)


@app.get("/list_models", summary="list all models")
async def my_list_models() -> Annotated[List[str], Field(description="the names of the models", examples=[model_names])]:
    """
      Returns the names of all the models that are supported.
    """
    return model_names


@app.get("/list_added", summary="list all added models")
async def list_models() -> Annotated[Dict[str, str], Field(description="all the added models", examples=[{"68fb4ce6-24a8-4615-8830-61ccada86eba": "neural_network"}])]:
    """
      Returns all the added models in a form "id": "model name"
    """
    return list_all_models()


@app.post("/predict", summary="predict target vals")
async def predict(
    id: Id = Query(description="id of the model", example="68fb4ce6-24a8-4615-8830-61ccada86eba"),
    data: PredictRequest = Body()
) -> PredictResponse:
    """
      Predict the target values for the given dataset using the model with `id`.
    """
    model = get_model(id)
    y = model.infer(data.X)

    return PredictResponse(y=y)


@app.get("/retrain_model", summary="retrain a model")
async def retrain_model(id: Id = Query(description="id of the model", example="68fb4ce6-24a8-4615-8830-61ccada86eba")) -> Literal["ok"]:
    """
      Retrain the model with `id`
    """
    model = get_model(id)
    model.refit()

    return "ok"


@app.get("/remove_model", summary="retrain a model")
async def remove_model(id: Id = Query(description="id of the model", example="68fb4ce6-24a8-4615-8830-61ccada86eba")) -> Literal["ok"]:
    """
      Remove the model with `id`
    """
    del_model(id)

    return "ok"


@app.get("/alive", summary="Aliveness check")
async def alive() -> Annotated[Literal["yes"], Field(description="whether the service is alive")]:
    """
      Returns "yes" if the service is alive and is ready to serve requests.
    """
    return "yes"

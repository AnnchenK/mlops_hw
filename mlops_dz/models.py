from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Union, Literal
from fastapi import Path


Model = Annotated[Literal["linear_regression", "neural_network"], Path(description="type of the model")]

class LinearRegressionParameters(BaseModel):
    """
      Parameters for linear regression model
    """
    train_constant: bool
    alpha: float

class NeuralNetworkParameters(BaseModel):
    """
      Parameters for neural network model
    """
    layers: int
    activation: str

class Dataset(BaseModel):
    X: List[List[float]]
    y: List[float]

    @field_validator('X')
    def check_x_consistency(cls, v, values):
        if len(v) == 0:
            raise ValueError("X cannot be empty")
        row_lengths = {len(row) for row in v}
        if len(row_lengths) > 1:
            raise ValueError("All rows in X must have the same length")
        return v

    @field_validator('y')
    def check_y_length(cls, v, values):
        if 'X' in values and len(v) != len(values['X']):
            raise ValueError("Length of y must match number of rows in X")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "X": [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
                    "y": [1.0, 2.0, 3.0]
                }
            ]
        }
    }

class AddModelRequest(BaseModel):
    parameters: Union[LinearRegressionParameters, NeuralNetworkParameters] = Field(
        description="the parameters of the model",
    )
    dataset: Dataset = Field(
        description="the dataset to train the model on"
    )

class AddModelResponse(BaseModel):
    model_id: str = Field(
        description="the id of the model", 
        examples=["68fb4ce6-24a8-4615-8830-61ccada86eba"]
    )

AliveResponse = Annotated[Literal["yes", "no"], "whether the service is alive"]

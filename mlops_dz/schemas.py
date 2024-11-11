from models import ModelParamsUnion

from pydantic import BaseModel, Field, field_validator
from typing import List


class Dataset(BaseModel):
    """
      dataset for the model to train on
    """
    X: List[List[float]] = Field(
        description="features of the dataset",
    )
    y: List[float] = Field(
        description="target values of the dataset",
    )


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
        if len(v) != len(values.data['X']):
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
    """
      body of the `add_model` handle request
    """
    parameters: ModelParamsUnion = Field(
        description="the parameters of the model",
    )
    dataset: Dataset = Field(
        description="the dataset to train the model on"
    )


class AddModelResponse(BaseModel):
    """
      response of the `add_model` handle
    """
    id: str = Field(
        description="the id of the model", 
        examples=["68fb4ce6-24a8-4615-8830-61ccada86eba"]
    )

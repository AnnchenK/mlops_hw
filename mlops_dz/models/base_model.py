from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
import logging


_logger = logging.getLogger("uvicorn")


class ModelParams(BaseModel):
    """
    base class for model parameters
    """


class Model:
    """
    base class for models
    """

    @staticmethod
    def model_name() -> str:
        """
        returns the name of the model
        """
        return "base_model"

    @staticmethod
    def model_params() -> type[ModelParams]:
        """
        returns the class for model params
        """
        return ModelParams

    def __init__(self, params: ModelParams) -> None:
        """
        initializes the model `self` with provided `params`
        """
        self._params = params

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """
        trains `self` on a dataset `X` with target values `y` and saves the dataset for future refiting
        """
        self._X = X
        self._y = y
        self._do_fit(self._X, self._y)

    def refit(self) -> None:
        """
        retrain `self`
        """
        self._reset()

        if not hasattr(self, "_X") or not hasattr(self, "_y"):
            raise HTTPException(status_code=500, detail="no dataset is saved for refit")
        self._do_fit(self._X, self._y)

    def _do_fit(self, X: List[List[float]], y: List[float]) -> None:
        """
        actually trains `self`
        """
        _logger.info(f"training a model on a dataset with {len(X)} rows")

    def _reset(self) -> None:
        """
        resets the model
        """

    def infer(self, X: List[List[float]]) -> List[float]:
        """
        predicts target values for `X` with `self`
        """
        _logger.info(f"infering from a dataset with {len(X)} rows")
        return []

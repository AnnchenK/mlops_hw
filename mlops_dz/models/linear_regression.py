from .base_model import ModelParams, Model

from typing import List


class LinearRegressionParams(ModelParams):
    """
      Parameters for linear regression model
    """
    train_constant: bool
    alpha: float


class LinearRegression(Model):
    """
      linear regression model
    """
    @staticmethod
    def model_name() -> str:
        """
          returns the name of the model
        """
        return "linear_regression"

    @staticmethod
    def model_params() -> type[ModelParams]:
        """
          returns the class for model params
        """
        return LinearRegressionParams

    def __init__(self, params: LinearRegressionParams) -> None:
        """
          initializes the model `self` with provided `params`
        """

    def _do_fit(self, X: List[List[float]], y: List[float]) -> None:
        """
          trains `self` on a dataset `X` with target values `y`
        """

    def _reset(self) -> None:
        """
          resets the model
        """

    def infer(self, X: List[List[float]]) -> List[float]:
        """
          predicts target values for `X` with `self`
        """
        return []


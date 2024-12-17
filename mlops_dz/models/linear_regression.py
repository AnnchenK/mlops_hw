from .base_model import ModelParams, Model

from sklearn.linear_model import LinearRegression as SklearnLinearRegression

from typing import List
from pydantic import Field

import mlflow

mlflow.sklearn.autolog()


class LinearRegressionParams(ModelParams):
    """
    Parameters for linear regression model
    """

    train_constant: bool = Field(description="wether to train a constant")
    positive: bool = Field(description="wether to keep coefs positive")


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
        super().__init__(params)
        self._model = SklearnLinearRegression(
            fit_intercept=self._params.train_constant,
            positive=self._params.train_constant,
        )

    def _do_fit(self, X: List[List[float]], y: List[float]) -> None:
        """
        trains `self` on a dataset `X` with target values `y`
        """
        mlflow.set_experiment("linear_experiment")

        with mlflow.start_run():
            mlflow.log_param("train_constant", self._params.train_constant)
            # mlflow.log_metric("metric1", 0.85)
            super()._do_fit(X, y)
            self._model.fit(X, y)
        mlflow.end_run()

    def _reset(self) -> None:
        """
        resets the model
        """
        self.model = SklearnLinearRegression(
            fit_intercept=self._params.train_constant,
            positive=self._params.train_constant,
        )

    def infer(self, X: List[List[float]]) -> List[float]:
        """
        predicts target values for `X` with `self`
        """
        super().infer(X)
        return self._model.predict(X).tolist()

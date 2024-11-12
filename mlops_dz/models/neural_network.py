from .base_model import ModelParams, Model

from sklearn.neural_network import MLPRegressor

from typing import Literal, List
from pydantic import Field
from pydantic.types import PositiveInt


class NeuralNetworkParams(ModelParams):
    """
      Parameters for neural network model
    """
    layers: PositiveInt = Field(
        description="number of hidden layers"
    )
    layer_size: PositiveInt = Field(
        description="size of the hidden layers"
    )
    activation: Literal["identity", "logistic", "tanh", "relu"] = Field(
        description="which activation function to use"
    )


class NeuralNetwork(Model):
    """
      neural network model
    """
    @staticmethod
    def model_name() -> str:
        """
          returns the name of the model
        """
        return "neural_network"

    @staticmethod
    def model_params() -> type[ModelParams]:
        """
          returns the class for model params
        """
        return NeuralNetworkParams

    def __init__(self, params: NeuralNetworkParams) -> None:
        """
          initializes the model `self` with provided `params`
        """
        super().__init__(params)
        self._model = MLPRegressor(hidden_layer_sizes=(self._params.layer_size,) * self._params.layers,
                                  activation=self._params.activation)

    def _do_fit(self, X: List[List[float]], y: List[float]) -> None:
        """
          trains `self` on a dataset `X` with target values `y`
        """
        super()._do_fit(X, y)
        self._model.fit(X, y)

    def _reset(self) -> None:
        """
          resets the model
        """
        self._model = MLPRegressor(hidden_layer_sizes=(self._params.layer_size,) * self._params.layers,
                                  activation=self._params.activation)

    def infer(self, X: List[List[float]]) -> List[float]:
        """
          predicts target values for `X` with `self`
        """
        super().infer(X)
        return self._model.predict(X).tolist()


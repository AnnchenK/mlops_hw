from .base_model import ModelParams, Model

from typing import Literal, List

class NeuralNetworkParams(ModelParams):
    """
      Parameters for neural network model
    """
    layers: int
    activation: Literal['relu'] | Literal['sigmoid']


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


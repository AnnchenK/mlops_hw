from .base_model import ModelParams, Model

# for class creation only
from .linear_regression import LinearRegression  # noqa # pylint: disable=unused-import
from .neural_network import NeuralNetwork  # noqa # pylint: disable=unused-import

from typing import List, Dict, Union, Literal


_models: List[type[Model]] = Model.__subclasses__()
_name_to_params_map: Dict[str, type[ModelParams]] = {}
_name_to_model_map: Dict[str, type[Model]] = {}

model_names: List[str] = []


for model in _models:
    _name_to_params_map[model.model_name()] = model.model_params()
    _name_to_model_map[model.model_name()] = model
model_names = list(_name_to_params_map.keys())


ModelNameUnion = Literal[*model_names]
ModelParamsUnion = Union[*_name_to_params_map.values()]


def validate_params(model: ModelNameUnion, params: ModelParamsUnion) -> bool:
    """
    validate if the provided `params` are compatible with the provided `model`
    """
    return isinstance(params, _name_to_params_map[model])


def create_model(model: ModelNameUnion, params: ModelParams) -> Model:
    """
    creates a `model` with provided `params`
    """
    return _name_to_model_map[model](params)


def create_trained_model(
    model: ModelNameUnion, params: ModelParams, X: List[List[float]], y: List[float]
):
    """
    creates a `model` with provided `params` and trains it on the `data`.
    """
    model = create_model(model, params)
    model.fit(X, y)
    return model

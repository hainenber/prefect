import inspect
import typing

from prefect._internal.pydantic import HAS_PYDANTIC_V2

if HAS_PYDANTIC_V2:
    from pydantic.v1 import BaseModel as V1BaseModel
else:
    from pydantic import BaseModel as V1BaseModel


def is_v1_model(v) -> bool:
    if isinstance(v, V1BaseModel):
        return True
    try:
        if inspect.isclass(v) and issubclass(v, V1BaseModel):
            return True
    except TypeError:
        pass

    return False


def has_v1_model_as_param(signature: inspect.Signature) -> bool:
    parameters = signature.parameters.values()
    for p in parameters:
        # check if this parameter is a v1 model
        if is_v1_model(p.annotation):
            return True

        # check if this parameter is a collection of types
        for v in typing.get_args(p.annotation):
            if is_v1_model(v):
                return True
    return False

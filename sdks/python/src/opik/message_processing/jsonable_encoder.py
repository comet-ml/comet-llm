import logging
import dataclasses
import datetime as dt
from enum import Enum
from pathlib import PurePath
from types import GeneratorType
from typing import Any

import numpy as np

import opik.rest_api.core.datetime_utils as datetime_utils

LOGGER = logging.getLogger(__name__)


def jsonable_encoder(obj: Any) -> Any:
    """
    This is a modified version of the serializer generated by Fern in rest_api.core.jsonable_encoder.
    The code is simplified to serialize complex objects into a textual representation.
    """
    try:
        if dataclasses.is_dataclass(obj):
            obj_dict = obj.__dict__
            return jsonable_encoder(obj_dict)
        if isinstance(obj, Enum):
            return jsonable_encoder(obj.value)
        if isinstance(obj, PurePath):
            return str(obj)
        if isinstance(obj, (str, int, float, type(None))):
            return obj
        if isinstance(obj, dt.datetime):
            return datetime_utils.serialize_datetime(obj)
        if isinstance(obj, dt.date):
            return str(obj)
        if isinstance(obj, dict):
            encoded_dict = {}
            allowed_keys = set(obj.keys())
            for key, value in obj.items():
                if key in allowed_keys:
                    encoded_key = jsonable_encoder(key)
                    encoded_value = jsonable_encoder(value)
                    encoded_dict[encoded_key] = encoded_value
            return encoded_dict
        if isinstance(obj, (list, set, frozenset, GeneratorType, tuple)):
            encoded_list = []
            for item in obj:
                encoded_list.append(jsonable_encoder(item))
            return encoded_list

        if isinstance(obj, np.ndarray):
            return jsonable_encoder(obj.tolist())

        if hasattr(obj, "to_string"):  # langchain internal data objects
            try:
                return jsonable_encoder(obj.to_string())
            except Exception:
                pass

    except Exception:
        LOGGER.debug("Failed to serialize object.", exc_info=True)

    data = str(obj)

    return data

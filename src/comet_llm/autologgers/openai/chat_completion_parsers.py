# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this package.
# *******************************************************

import inspect
import logging
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Tuple, Union

import comet_llm.logging

from . import metadata

if TYPE_CHECKING:
    from openai import Stream
    from openai.openai_object import OpenAIObject
    from openai.types.chat.chat_completion import ChatCompletion

Inputs = Dict[str, Any]
Outputs = Dict[str, Any]
Metadata = Dict[str, Any]

CreateCallResult = Union[
    "ChatCompletion", "Stream", "OpenAIObject", Iterable["OpenAIObject"]
]

LOGGER = logging.getLogger(__name__)


def create_arguments_supported(kwargs: Dict[str, Any]) -> bool:
    if "messages" not in kwargs:
        return False

    return True


def parse_create_arguments(kwargs: Dict[str, Any]) -> Tuple[Inputs, Metadata]:
    kwargs_copy = kwargs.copy()
    inputs = {}

    inputs["messages"] = kwargs_copy.pop("messages")
    if "function_call" in kwargs_copy:
        inputs["function_call"] = kwargs_copy.pop("function_call")

    metadata = {"created_from": "openai", "type": "openai_chat", **kwargs_copy}

    return inputs, metadata


def parse_create_result(result: CreateCallResult) -> Tuple[Outputs, Metadata]:
    openai_version = metadata.openai_version()

    if openai_version is not None and openai_version.startswith("0."):
        return _v0_x_x__parse_create_result(result)

    return _v1_x_x__parse_create_result(result)


def _v0_x_x__parse_create_result(
    result: Union["OpenAIObject", Iterable["OpenAIObject"]]
) -> Tuple[Outputs, Metadata]:
    if inspect.isgenerator(result):
        choices = "Generation is not logged when using stream mode"
        metadata = {}
    else:
        result_dict = result.to_dict()  # type: ignore
        choices: List[Dict[str, Any]] = result_dict.pop("choices")  # type: ignore
        metadata = result_dict

    outputs = {"choices": choices}

    if "model" in metadata:
        metadata["output_model"] = metadata.pop("model")

    return outputs, metadata


def _v1_x_x__parse_create_result(
    result: Union["ChatCompletion", "Stream"]
) -> Tuple[Outputs, Metadata]:
    stream_mode = not hasattr(result, "model_dump")
    if stream_mode:
        choices = "Generation is not logged when using stream mode"
        metadata = {}
    else:
        result_dict = result.model_dump()
        choices: List[Dict[str, Any]] = result_dict.pop("choices")  # type: ignore
        metadata = result_dict

    outputs = {"choices": choices}

    if "model" in metadata:
        metadata["output_model"] = metadata.pop("model")

    return outputs, metadata

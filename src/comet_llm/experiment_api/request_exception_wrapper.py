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


import functools
import json
import logging
import urllib.parse
from typing import Any, Callable, List

import requests  # type: ignore

from .. import config, exceptions, logging_messages

LOGGER = logging.getLogger(__name__)


def wrap(check_on_prem: bool = False) -> Callable:
    def inner_wrap(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # type: ignore
            try:
                return func(*args, **kwargs)
            except requests.RequestException as exception:
                exception_args: List[Any] = []

                if check_on_prem:
                    comet_url = config.comet_url()
                    if _is_on_prem(comet_url):
                        exception_args.append(
                            f"Failed to send prompt to your Comet installation at "
                            f"{comet_url}. Check that your Comet "
                            f"installation is up-to-date and check the traceback for more details."
                        )
                if exception.response is not None:
                    exception_args.append(_handle_response(exception.response))

                raise exceptions.CometLLMException(*exception_args) from exception

        return wrapper

    return inner_wrap


def _is_on_prem(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    root = f"{parsed.scheme}://{parsed.hostname}/"
    return root != "https://www.comet.com/"


def _handle_response(response: requests.Response):
    sdk_error_code = json.loads(response.text)["sdk_error_code"]
    return logging_messages.SDK_ERROR_CODES_LOGGING_MESSAGE.get(sdk_error_code)
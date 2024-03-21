# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this package.
# *******************************************************

import logging
import pathlib
import threading
import time
import os
from typing import Optional

from . import messages
from .offline_senders import chain, prompt

LOGGER = logging.getLogger(__name__)


class OfflineMessageProcessor:
    def __init__(self, offline_directory: str, file_usage_duration: float) -> None:
        self._offline_directory = offline_directory
        self._batch_duration_seconds = file_usage_duration
        self._lock = threading.Lock()

        self._current_file_started_at: Optional[float] = None
        self._current_file_name: Optional[str] = None

        os.makedirs(self._offline_directory, exist_ok=True)

    def process(self, message: messages.BaseMessage) -> None:
        with self._lock:
            self._update_current_file_if_needed()
            assert self._current_file_name is not None
            file_path = pathlib.Path(self._offline_directory, self._current_file_name)

            if isinstance(message, messages.PromptMessage):
                try:
                    return prompt.send(message, str(file_path))
                except Exception:
                    LOGGER.error("Failed to log prompt", exc_info=True)
            elif isinstance(message, messages.ChainMessage):
                try:
                    return chain.send(message, str(file_path))
                except Exception:
                    LOGGER.error("Failed to log chain", exc_info=True)

        LOGGER.debug(f"Unsupported message type {message}")
        return None

    def _update_current_file_if_needed(self) -> None:
        current_time = time.time()

        if (
            self._current_file_started_at is None
            or (current_time - self._current_file_started_at)
            >= self._batch_duration_seconds
        ):
            self._current_file_started_at = current_time
            self._current_file_name = f"messages_{current_time}.jsonl"

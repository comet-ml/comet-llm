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

import logging

from . import messages
from .online_senders import chain, prompt

LOGGER = logging.getLogger(__name__)


class OnlineMessageProcessor:
    def __init__(self) -> None:
        pass

    def process(self, message: messages.BaseMessage) -> None:
        if isinstance(message, messages.PromptMessage):
            try:
                prompt.send_prompt(message)
            except Exception:
                LOGGER.error("Failed to log prompt", exc_info=True)
        elif isinstance(message, messages.ChainMessage):
            try:
                chain.send_chain(message)
            except Exception:
                LOGGER.error("Failed to log chain", exc_info=True)

        LOGGER.debug(f"Unsupported message type {message}")
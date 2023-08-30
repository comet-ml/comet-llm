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
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import threading
from typing import TYPE_CHECKING, Dict, Optional

from .. import exceptions
from . import thread_registry

if TYPE_CHECKING:  # pragma: no cover
    from . import chain


class State:
    def __init__(self) -> None:
        self._id: int = 0
        self._chain: Optional["chain.Chain"] = None
        self._chain_thread_registry = thread_registry.ChainThreadRegistry()
        self._lock = threading.Lock()

    @property
    def chain(self) -> "chain.Chain":
        result = self._chain_thread_registry.get()
        if result is None:
            raise exceptions.CometLLMException(
                "Global chain is not initialized for this thread. Initialize it with `comet_llm.start_chain(...)`"
            )
        
        return result

    @chain.setter
    def chain(self, value: "chain.Chain") -> None:
        self._chain_thread_registry.add(value)

    def new_id(self) -> int:
        with self._lock:
            self._id += 1
            return self._id


_APP_STATE = State()


def get_global_chain() -> "chain.Chain":
    return _APP_STATE.chain


def set_global_chain(new_chain: "chain.Chain") -> None:
    _APP_STATE.chain = new_chain


def get_new_id() -> int:
    return _APP_STATE.new_id()

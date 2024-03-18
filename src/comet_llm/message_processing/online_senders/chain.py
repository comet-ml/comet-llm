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

import io
import json

from comet_llm import app, convert, experiment_api, llm_result

from .. import messages


def send_chain(message: messages.ChainMessage) -> llm_result.LLMResult:
    experiment_api_ = experiment_api.ExperimentAPI.create_new(
        api_key=message.experiment_information.api_key,
        workspace=message.experiment_information.workspace,
        project_name=message.experiment_information.project_name,
    )

    if message.tags is not None:
        experiment_api_.log_tags(message.tags)

    experiment_api_.log_asset_with_io(
        name="comet_llm_data.json",
        file=io.StringIO(json.dumps(message.chain_data)),
        asset_type="llm_data",
    )

    experiment_api_.log_metric(name="chain_duration", value=message.duration)

    parameters = convert.chain_metadata_to_flat_parameters(message.metadata)
    for name, value in parameters.items():
        experiment_api_.log_parameter(name, value)

    for name, value in message.others.items():
        experiment_api_.log_other(name, value)

    return llm_result.LLMResult(
        id=experiment_api_.id, project_url=experiment_api_.project_url
    )

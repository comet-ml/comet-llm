VERDICT_KEY = "verdict"
REASON_KEY = "reason"

evaluation_steps_template = """Create a list of evaluation steps based on the provided task and criteria. The data that will be evaluated will include the fields {{fields}} which can be included in the evaluation steps.

Task:
{evaluation_task}

Criteria:
{criteria}

Provide the list of evaluation steps in JSON format:
{{
    "steps": [<list of steps>]
}}
"""

# TODO: Review if this should be more general, including how to run the evaluation on general keys
scoring_template = """{evaluation_task}

Criteria:
{criteria}

Evaluation steps:
{evaluation_steps}

Data to be evaluated:
{data_to_evaluate}

Provide the evaluation score in JSON format:
{{
    "{VERDICT_KEY}": <your verdict>,
    "{REASON_KEY}": <list your reasoning as bullet points>
}}
"""

from typing import List, Callable, Dict, Any
import inspect
from opik import exceptions

def raise_if_score_arguments_are_missing(score_function: Callable, score_name: str, kwargs: Dict[str, Any]):
    signature = inspect.signature(score_function)

    parameters = signature.parameters

    is_method = False
    param_list = list(parameters.keys())
    if param_list and param_list[0] == 'self':
        is_method = True

    missing_required_arguments: List[str] = []

    # Check for required parameters that are not in kwargs
    for name, param in parameters.items():
        if is_method and name == 'self':
            continue

        if param.default == inspect.Parameter.empty and param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
            if name not in kwargs:
               missing_required_arguments.append(name)
    
    if len(missing_required_arguments) > 0:
        raise exceptions.ScoreMethodMissedArguments(
            f"The scoring function {score_name} expects arguments: {parameters.keys()} "
            f"but these keys were not present in the dictionary returned by the evaluation task. "
            f"Evaluation task dictionary keys: {kwargs.keys()}."
        )
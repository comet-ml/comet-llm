from .decorator.tracker import track, flush_tracker
from .api_objects.opik_client import Opik
from .api_objects.trace import Trace
from .api_objects.span import Span
from .api_objects.dataset.dataset_item import DatasetItem
from .api_objects.dataset import Dataset
from .api_objects.experiment.experiment import Experiment
from .api_objects.experiment.experiment_item import ExperimentItem
from . import _logging
from .configurator.configure import configure
from . import package_version
from .plugins.pytest.decorator import llm_unit
from .evaluation import evaluate

_logging.setup()

__version__ = package_version.VERSION
__all__ = [
    "__version__",
    "evaluate",
    "track",
    "flush_tracker",
    "Opik",
    "Trace",
    "Span",
    "DatasetItem",
    "Dataset",
    "Experiment",
    "ExperimentItem",
    "llm_unit",
    "configure",
]

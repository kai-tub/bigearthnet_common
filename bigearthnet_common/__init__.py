import importlib.metadata
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="fastcore")

__version__ = importlib.metadata.version("bigearthnet_common")

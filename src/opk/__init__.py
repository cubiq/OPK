from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("opk")
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.1.1-dev"


from .keycap import KeyCap
from .export import ExportType, export_key_rows, export_individual_keys
from . import defaults

__all__ = [
    "KeyCap",
    "ExportType",
    "export_key_rows",
    "export_individual_keys",
    "defaults"
]

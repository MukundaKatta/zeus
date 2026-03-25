"""Zeus — Build full-stack apps from natural language descriptions."""

__version__ = "0.1.0"

from zeus.core import AppGenerator
from zeus.templates import TemplateEngine, TEMPLATES

__all__ = ["AppGenerator", "TemplateEngine", "TEMPLATES", "__version__"]

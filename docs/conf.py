"""Configuration Sphinx (documentation en reStructuredText)."""

import sys
from pathlib import Path

# Rend le package importable pour autodoc (layout src/).
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

project = "example-package"
author = "Michel ANDRIANAIVO"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",  # doc API depuis les docstrings
    "sphinx.ext.autosummary",  # tables de résumé
    "sphinx.ext.viewcode",  # liens vers le code source
    "sphinx.ext.intersphinx",  # liens vers la doc Python
]

autosummary_generate = True
autodoc_typehints = "description"  # affiche les annotations dans la description

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

templates_path = ["_templates"]
exclude_patterns = ["_build"]
language = "fr"

html_theme = "furo"
html_static_path = ["_static"]

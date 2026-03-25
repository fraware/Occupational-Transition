# Sphinx configuration for API reference (development).
# Build: from repo root, pip install -e ".[dev]" then
#   sphinx-build -b html docs/sphinx docs/sphinx/_build/html

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

project = "Occupational Transition"
copyright = "Occupational Transition contributors"
author = "Occupational Transition contributors"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

autodoc_member_order = "bysource"
napoleon_google_docstring = True

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path: list[str] = []

"""Thin wrapper: QA lives in ``occupational_transition.qa.crosswalks``."""

from __future__ import annotations

import sys

from occupational_transition.qa.crosswalks import main

if __name__ == "__main__":
    sys.exit(main())

"""Public package exports and lazy pipeline submodule."""

from __future__ import annotations

import occupational_transition as ot


def test_figure1_panelB_t002_lazy_load() -> None:
    mod = ot.figure1_panelB_t002
    assert mod.__name__ == "occupational_transition.pipelines.figure1_panelB_t002"
    assert hasattr(mod, "build_figure1_panelB_t002")

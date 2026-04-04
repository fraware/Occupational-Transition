"""Contracts for ``run_step`` helpers (exit codes, script shims)."""

from __future__ import annotations

import importlib.util

import pytest

from occupational_transition.paths import repo_root
from occupational_transition.run_step import _coerce_qa_exit_code


def test_coerce_qa_exit_code_none_is_success() -> None:
    assert _coerce_qa_exit_code(None, spec="mod:main") == 0


def test_coerce_qa_exit_code_int_passthrough() -> None:
    assert _coerce_qa_exit_code(0, spec="mod:main") == 0
    assert _coerce_qa_exit_code(17, spec="mod:main") == 17


def test_coerce_qa_exit_code_rejects_bool() -> None:
    with pytest.raises(TypeError, match="bool"):
        _coerce_qa_exit_code(True, spec="mod:main")


def test_coerce_qa_exit_code_rejects_non_int() -> None:
    with pytest.raises(TypeError, match="str"):
        _coerce_qa_exit_code("0", spec="mod:main")


def test_scripts_awes_alpi_shim_delegates_to_package() -> None:
    """``scripts/awes_alpi_common.py`` must expose the same API via ``src``."""
    root = repo_root()
    path = root / "scripts" / "awes_alpi_common.py"
    spec = importlib.util.spec_from_file_location("_ot_awes_shim_check", path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.SECTOR6_ORDER == ("MFG", "INF", "FAS", "PBS", "HCS", "RET")
    assert mod.naics2_to_sector6(51)[0] == "INF"
    assert mod.occ22_code_from_id(3) == "occ22_03"

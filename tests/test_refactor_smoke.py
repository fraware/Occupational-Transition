import importlib

from occupational_transition.bundle_manifest import format_analysis_bundles_yaml
from occupational_transition.catalog import load_data_registry
from occupational_transition.manifests import FULL_REBUILD_STEPS
from occupational_transition.paper_scope import load_paper_scope
from occupational_transition.paths import repo_root
from occupational_transition.run_step import LEGACY_BUILD_CMDS, LEGACY_QA_CMDS


def test_paper_scope_loads() -> None:
    data = load_paper_scope()
    assert data["primary_bundle"] == "core-paper"
    assert "T-010" in data["core_paper_tickets"]
    assert "figures/figure1_panelA_occ_baseline.csv" in data["committed_core_paper_figures"]
    assert "figures/figure6_policy_roadmap.csv" in data["committed_core_paper_figures"]


def test_data_registry_has_catalog_columns() -> None:
    root = repo_root()
    rows = load_data_registry(root)
    assert len(rows) >= 1
    for key in ("extractor", "update_cadence", "notes_for_users"):
        assert key in rows[0]


def test_full_rebuild_steps_use_run_step() -> None:
    for s in FULL_REBUILD_STEPS:
        assert "occupational_transition.run_step build" in s.build_cmd
        assert "occupational_transition.run_step qa" in s.qa_cmd


def test_full_rebuild_steps_have_build_and_qa_modules() -> None:
    for s in FULL_REBUILD_STEPS:
        assert s.build_module, f"{s.ticket} missing build_module"
        assert s.qa_module, f"{s.ticket} missing qa_module"


def test_legacy_maps_cover_all_tickets() -> None:
    tickets = {s.ticket for s in FULL_REBUILD_STEPS}
    assert tickets == set(LEGACY_BUILD_CMDS.keys()) == set(LEGACY_QA_CMDS.keys())


def test_bundle_manifest_yaml_contains_quick_start() -> None:
    y = format_analysis_bundles_yaml()
    assert "quick-start" in y
    assert "T-001" in y


def test_pipeline_modules_importable() -> None:
    for s in FULL_REBUILD_STEPS:
        mod_name, _, attr = s.build_module.partition(":")
        m = importlib.import_module(mod_name)
        assert callable(getattr(m, attr))


def test_qa_modules_importable() -> None:
    for s in FULL_REBUILD_STEPS:
        mod_name, _, attr = s.qa_module.partition(":")
        m = importlib.import_module(mod_name)
        assert callable(getattr(m, attr))

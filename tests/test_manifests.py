from occupational_transition.manifests import (
    ANALYSIS_BUNDLES,
    FULL_REBUILD_STEPS,
    selectable_steps,
)


def test_analysis_bundles_exist() -> None:
    names = {b.name for b in ANALYSIS_BUNDLES}
    assert {"quick-start", "core-paper", "full-replication", "release-signoff"} <= names


def test_selectable_steps_bundle_core_paper() -> None:
    steps = selectable_steps("core-paper", None)
    tickets = [s.ticket for s in steps]
    assert tickets[0] == "T-001"
    assert "T-010" in tickets
    assert "T-011" not in tickets


def test_selectable_steps_explicit_tickets() -> None:
    steps = selectable_steps(None, ["T-001", "T-008"])
    assert [s.ticket for s in steps] == ["T-001", "T-008"]


def test_full_steps_include_pr000() -> None:
    assert FULL_REBUILD_STEPS[0].ticket == "PR-000"

from pathlib import Path

from occupational_transition.orchestration import env_for_source_mode, parse_profile


def test_env_for_source_mode() -> None:
    assert env_for_source_mode("latest_mode") == {
        "SOURCE_SELECTION_MODE": "latest_mode",
    }
    assert env_for_source_mode("freeze_mode") == {
        "SOURCE_SELECTION_MODE": "freeze_mode",
    }


def test_parse_profile_toml(tmp_path: Path) -> None:
    p = tmp_path / "profile.toml"
    p.write_text(
        "[run]\n"
        'bundle = "quick-start"\n'
        'source_selection_mode = "latest_mode"\n',
        encoding="utf-8",
    )
    data = parse_profile(p)
    assert data["run"]["bundle"] == "quick-start"
    assert data["run"]["source_selection_mode"] == "latest_mode"

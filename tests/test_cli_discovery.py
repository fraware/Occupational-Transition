from occupational_transition import cli


def test_list_analyses_outputs_known_bundle(capsys) -> None:  # type: ignore[no-untyped-def]
    cli._cmd_list_analyses()
    out = capsys.readouterr().out
    assert "quick-start" in out
    assert "full-replication" in out


def test_list_sources_outputs_known_source(capsys) -> None:  # type: ignore[no-untyped-def]
    cli._cmd_list_sources()
    out = capsys.readouterr().out
    assert "BLS_OEWS" in out
    assert "BTOS" in out

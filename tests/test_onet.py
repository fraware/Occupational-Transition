from occupational_transition.sources.onet import onet_version_to_zip_token


def test_onet_version_to_zip_token() -> None:
    assert onet_version_to_zip_token("30.2") == "30_2"

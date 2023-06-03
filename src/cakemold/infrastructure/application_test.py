import pytest


@pytest.mark.integration
def test_assert_true():
    assert True is True  # nosec

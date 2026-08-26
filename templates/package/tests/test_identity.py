import pytest

from {{package_name}}.models.identity import PackageId


def test_package_id() -> None:
    assert PackageId("a").value == "a"


def test_empty_id() -> None:
    with pytest.raises(ValueError):
        PackageId(" ")

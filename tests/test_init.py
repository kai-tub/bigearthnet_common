import bigearthnet_common
from packaging import version


def test_version():
    assert isinstance(version.parse(bigearthnet_common.__version__), version.Version)

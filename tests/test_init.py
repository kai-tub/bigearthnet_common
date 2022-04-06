from packaging import version

import bigearthnet_common


def test_version():
    assert isinstance(version.parse(bigearthnet_common.__version__), version.Version)

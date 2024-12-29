from __future__ import annotations

import importlib.metadata

import phy408 as m


def test_version():
    assert importlib.metadata.version("phy408") == m.__version__

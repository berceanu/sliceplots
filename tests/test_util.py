#!/usr/bin/env pytahon
# -*- coding: utf-8 -*-

"""Tests for `sliceplots._util` module."""

import numpy as np

from sliceplots.util import _idx_from_val


def test_idx_from_val():
    """Find element position in array."""
    position = _idx_from_val(np.linspace(0, 10, 11), 5.1)
    assert position == 5

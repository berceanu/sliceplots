#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sliceplots.util` module."""

import numpy as np

from sliceplots import util


def test_idx_from_val():
    """Find element position in array."""
    position = util.idx_from_val(np.linspace(0, 10, 11), 5.1)
    assert position == 5

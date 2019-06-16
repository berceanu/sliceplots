#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sliceplots` package."""

import numpy as np

from sliceplots import sliceplots as sp


def test_idx_from_val():
    """Find element position in array."""
    position = sp.idx_from_val(np.linspace(0, 10, 11), 5.)
    assert position == 5

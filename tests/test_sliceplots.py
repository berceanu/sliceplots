#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sliceplots` package."""

import pytest
from numpy.testing import assert_almost_equal
import numpy as np

from sliceplots import sliceplots as sp


def test_idx_from_val():
    """Find element position in array."""
    position = sp.idx_from_val(np.linspace(0, 10, 11), 5.)
    assert position == 5
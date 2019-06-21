# -*- coding: utf-8 -*-

"""Utility functions module."""

import numpy as np


def idx_from_val(arr1d, val):
    """Given a 1D array, find index of closest element to given value.

    :param arr1d: 1D array of values
    :type arr1d: :py:class:`numpy.ndarray`
    :param val: element value
    :type val: float
    :return: element position in the array
    :rtype: int
    """
    idx = (np.abs(arr1d - val)).argmin()
    return idx

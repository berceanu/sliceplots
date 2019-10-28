# -*- coding: utf-8 -*-

"""Top-level package for sliceplots.

The following functions and classes are importable from the
top-level ``sliceplots`` namespace:

* :class:`sliceplots.two_dimensional.Plot2D`
* :func:`sliceplots.one_dimensional.plot_multicolored_line`
* :func:`sliceplots.one_dimensional.plot1d_break_x`
* :func:`sliceplots.util.addcolorbar`
"""
from sliceplots.util import addcolorbar  # NOQA: F401
from sliceplots.one_dimensional import (
    plot_multicolored_line,
    plot1d_break_x,
    plot1d,
)  # NOQA: F401
from sliceplots.two_dimensional import Plot2D  # NOQA: F401


__author__ = """Andrei Berceanu"""
__email__ = "andreicberceanu@gmail.com"
__version__ = "0.3.2"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sliceplots.two_dimensional` module."""

import numpy as np
import pytest

import sliceplots.two_dimensional as two_d

# data for plotting
uu = np.linspace(0, np.pi, 128)
data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)

# todo directly use matplotlib's own testing facilities once 3.2.0 is released
#       see https://matplotlib.org/3.1.0/devel/testing.html

@pytest.mark.mpl_image_compare()
# https://github.com/matplotlib/pytest-mpl
def test_plot2d():
    """Checks ``Plot2D`` class."""
    p2d = two_d.Plot2D(data,
                       uu,
                       uu,
                       xlabel=r'$x$ ($\mu$m)',
                       ylabel=r'$y$ ($\mu$m)',
                       zlabel=r'$\rho$ (cm$^{-3}$)',
                       hslice_val=np.pi / 3.0,
                       vslice_val=np.pi / 1.2,
                       hslice_opts={'color': 'firebrick', 'lw': 0.5, 'ls': '-'},
                       vslice_opts={'color': 'blue', 'ls': '-'},
                       figsize=(8, 8),
                       cmap='viridis',
                       cbar=True,
                       extent=(0, np.pi, 0, np.pi),
                       vmin=-1.0,
                       vmax=1.0,
                       text='your text here',
                       )

    return p2d.fig

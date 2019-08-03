#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sliceplots.two_dimensional` module."""
import numpy as np
import pytest

from sliceplots import Plot2D


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot2d_2slices(plt_data):
    """Checks ``Plot2D`` class."""
    p2d = Plot2D(
        arr2d=plt_data.data,
        h_axis=plt_data.uu,
        v_axis=plt_data.uu,
        xlabel=r"$x$ ($\mu$m)",
        ylabel=r"$y$ ($\mu$m)",
        zlabel=r"$\rho$ (cm$^{-3}$)",
        hslice_val=0.75,
        vslice_val=2.75,
        hslice_opts={"color": "#1f77b4", "lw": 0.5, "ls": "-"},
        vslice_opts={"color": "#d62728", "ls": "-"},
        figsize=(8, 8),
        cmap="viridis",
        cbar=True,
        extent=(0, np.pi, 0, np.pi),
        vmin=-1.0,
        vmax=1.0,
        text="your text here",
    )

    return p2d.fig


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot2d_horiz_slice(plt_data):
    """Checks ``Plot2D`` class."""
    p2d = Plot2D(
        arr2d=plt_data.data,
        h_axis=plt_data.uu,
        v_axis=plt_data.uu,
        xlabel=r"$x$ ($\mu$m)",
        ylabel=r"$y$ ($\mu$m)",
        zlabel=r"$\rho$ (cm$^{-3}$)",
        hslice_val=0.75,
        hslice_opts={"color": "#1f77b4", "lw": 0.5, "ls": "-"},
        figsize=(8, 8),
        cmap="viridis",
        cbar=True,
        extent=(0, np.pi, 0, np.pi),
        vmin=-1.0,
        vmax=1.0,
        text="your text here",
    )

    return p2d.fig


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot2d_vert_slice(plt_data):
    """Checks ``Plot2D`` class."""
    p2d = Plot2D(
        arr2d=plt_data.data,
        h_axis=plt_data.uu,
        v_axis=plt_data.uu,
        xlabel=r"$x$ ($\mu$m)",
        ylabel=r"$y$ ($\mu$m)",
        zlabel=r"$\rho$ (cm$^{-3}$)",
        vslice_val=2.75,
        vslice_opts={"color": "#d62728", "ls": "-"},
        figsize=(8, 8),
        cmap="viridis",
        cbar=True,
        extent=(0, np.pi, 0, np.pi),
        vmin=-1.0,
        vmax=1.0,
        text="your text here",
    )

    return p2d.fig


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot2d_no_slices(plt_data):
    """Checks ``Plot2D`` class."""
    p2d = Plot2D(
        arr2d=plt_data.data,
        h_axis=plt_data.uu,
        v_axis=plt_data.uu,
        xlabel=r"$x$ ($\mu$m)",
        ylabel=r"$y$ ($\mu$m)",
        zlabel=r"$\rho$ (cm$^{-3}$)",
        figsize=(8, 8),
        cmap="viridis",
        cbar=False,
        extent=(0, np.pi, 0, np.pi),
        vmin=-1.0,
        vmax=1.0,
        text="your text here",
    )

    return p2d.fig


# todo directly use matplotlib's own testing facilities once 3.2.0 is released
#       see https://matplotlib.org/3.1.0/devel/testing.html

# py.test --mpl-generate-path=baseline
# https://github.com/matplotlib/pytest-mpl

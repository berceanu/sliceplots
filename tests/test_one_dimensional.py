#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sliceplots.one_dimensional` module."""

from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np
import pytest

import sliceplots.one_dimensional as one_d


@pytest.fixture(scope="module")
def plt_data():
    # data for plotting
    PlottingData = namedtuple("plotting_data", ["uu", "data", "idx"])
    uu = np.linspace(0, np.pi, 128)
    data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)
    return PlottingData(uu=uu, data=data, idx=data.shape[0] // 2)


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot1d_break_x(plt_data):
    """Checks broken x-axis plot."""

    fig, ax = plt.subplots(figsize=(8, 3.2))

    one_d.plot1d_break_x(
        fig,
        plt_data.uu,
        plt_data.data[plt_data.idx, :],
        {
            "xlim_left": (0, 1),
            "xlim_right": (2, 3),
            "xlabel": r"$x$ ($\mu$m)",
            "ylabel": r"$\rho$ (cm$^{-3}$)",
        },
        {"ls": "--", "color": "red"},
    )

    return fig


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot1d(plt_data):
    """Checks ``Plot1D`` class."""
    p1d = one_d.Plot1D(
        plt_data.uu,
        plt_data.data[plt_data.idx, :],
        xlabel=r"$%s \;(\mu m)$" % "z",
        ylabel=r"$%s$" % "a_0",
        xlim=[0, 3],
        ylim=[-1, 1],
        figsize=(10, 6),
        color="red",
    )

    return p1d.fig

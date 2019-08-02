#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sliceplots.one_dimensional` module."""
import matplotlib.pyplot as plt
import pytest

from sliceplots import plot1d_break_x, Plot1D


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot1d_break_x(plt_data):
    """Checks broken x-axis plot."""

    fig, ax = plt.subplots(figsize=(8, 3.2))

    plot1d_break_x(
        plt_data.uu,
        plt_data.data[plt_data.idx, :],
        {
            "xlim_left": (0, 1),
            "xlim_right": (2, 3),
            "xlabel": r"$x$ ($\mu$m)",
            "ylabel": r"$\rho$ (cm$^{-3}$)",
        },
        {"ls": "--", "color": "red"},
        ax=ax,
    )

    return fig


@pytest.mark.mpl_image_compare(style="mpl20", savefig_kwargs={"bbox_inches": "tight"})
def test_plot1d(plt_data):
    """Checks ``Plot1D`` class."""
    p1d = Plot1D(
        plt_data.uu,
        plt_data.data[plt_data.idx, :],
        xlabel=r"$%s \;(\mu m)$" % "z",
        ylabel=r"$%s$" % "a_0",
        xlim=[0, 3],
        ylim=[-1, 1],
        color="red",
    )

    return p1d.fig

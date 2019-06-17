# -*- coding: utf-8 -*-

"""Main containing useful 1D plotting abstractions on top of matplotlib."""

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .util import idx_from_val


def plot1d_break_x(fig, h_axis, v_axis, param, slice_opts):
    """Line plot with a broken x-axis.

    :param fig: Figure instance
    :type fig: :py:class:`matplotlib.figure.Figure`
    :param h_axis: x-axis data
    :type h_axis: :py:class:`numpy.ndarray`
    :param v_axis: y-axis data
    :type v_axis:  :py:class:`numpy.ndarray`
    :param param: Axes limits and labels.
    :type param: dict
    :param slice_opts: Options for plotted line.
    :type slice_opts: dict
    :returns: Generates plot on ``fig``.
    :rtype: None
    """
    ax_left = fig.axes[0]
    divider = make_axes_locatable(ax_left)
    ax_right = divider.new_horizontal(size="100%", pad=1)
    fig.add_axes(ax_right)

    ax_left.plot(h_axis, v_axis, **slice_opts)
    ax_left.set_ylabel(param["ylabel"])
    ax_left.set_xlabel(param["xlabel"])

    ax_left.set_xlim(*param["xlim_left"])
    ax_left.spines["right"].set_visible(False)
    ax_left.yaxis.set_ticks_position("left")

    ax_right.plot(h_axis, v_axis, **slice_opts)
    ax_right.set_ylabel(param["ylabel"])
    ax_right.set_xlabel(param["xlabel"])
    ax_right.yaxis.set_label_position("right")

    ax_right.set_xlim(*param["xlim_right"])
    ax_right.spines["left"].set_visible(False)
    ax_right.yaxis.set_ticks_position("right")

    # From https://matplotlib.org/examples/pylab_examples/broken_axis.html
    d = 0.015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax_left.transAxes, color="k", clip_on=False)
    ax_left.plot((1 - d, 1 + d), (-d, +d), **kwargs)
    ax_left.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    kwargs.update(transform=ax_right.transAxes)  # switch to the right axes
    ax_right.plot((-d, +d), (1 - d, 1 + d), **kwargs)
    ax_right.plot((-d, +d), (-d, +d), **kwargs)


class Plot1D:
    """Plot the data with given labels and plot options.

    :param v_axis: y-axis data
    :type v_axis: :py:class:`np.ndarray`
    :param h_axis: x-axis data
    :type h_axis: :py:class:`np.ndarray`
    :param xlabel: x-axis label
    :type xlabel: str
    :param ylabel: y-axis label
    :type ylabel: str
    :param kwargs: other arguments for :py:func:`matplotlib.plot`
    """

    def __init__(self, h_axis, v_axis, xlabel=r"", ylabel=r"", **kwargs):
        self.xlim = kwargs.pop("xlim", [np.min(h_axis), np.max(h_axis)])
        self.ylim = kwargs.pop("ylim", [np.min(v_axis), np.max(v_axis)])
        #
        xmin_idx, xmax_idx = (
            idx_from_val(h_axis, self.xlim[0]),
            idx_from_val(h_axis, self.xlim[1]),
        )
        #
        self.h_axis = h_axis[xmin_idx:xmax_idx]
        self.data = v_axis[xmin_idx:xmax_idx]
        #
        self.label = {"x": xlabel, "y": ylabel}
        self.text = kwargs.pop("text", "")
        #
        self.fig = Figure(figsize=kwargs.pop("figsize", (6.4, 6.4)))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        self.ax.plot(self.h_axis, self.data, **kwargs)

        self.ax.set(
            xlim=[self.h_axis[0], self.h_axis[-1]],
            ylim=self.ylim,
            ylabel=self.label["y"],
            xlabel=self.label["x"],
        )

        self.ax.grid()

        self.ax.text(
            0.02, 0.95, self.text, transform=self.ax.transAxes, color="firebrick"
        )

    def __str__(self):
        return "extent=({:.3f}, {:.3f}); min, max = ({:.3f}, {:.3f})".format(
            np.min(self.h_axis),
            np.max(self.h_axis),
            np.amin(self.data),
            np.amax(self.data),
        )

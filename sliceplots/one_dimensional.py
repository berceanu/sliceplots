# -*- coding: utf-8 -*-

"""Main containing useful 1D plotting abstractions on top of matplotlib."""

import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .util import idx_from_val


def plot1d_break_x(fig, h_axis, v_axis, param, slice_opts):
    r"""
    >>> uu = np.linspace(0, np.pi, 128)
    >>> data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)
    >>> fig, ax = plt.subplots(figsize=(8, 3.2))
    >>> plot1d_break_x(fig, uu, data[data.shape[0]//2], {'xlim_left':(0,1), 'xlim_right':(2,3),
        'xlabel':r'$x$ ($\mu$m)', 'ylabel':r'$\rho$ (cm$^{-3}$)'}, {'ls': '--', 'color': '0.5'})
    >>> fig
    """
    ax_left = fig.axes[0]
    divider = make_axes_locatable(ax_left)
    ax_right = divider.new_horizontal(size="100%", pad=1)
    fig.add_axes(ax_right)

    ax_left.plot(h_axis, v_axis, **slice_opts)
    ax_left.set_ylabel(param["ylabel"])
    ax_left.set_xlabel(param["xlabel"])

    ax_left.set_xlim(*param["xlim_left"])
    ax_left.yaxis.tick_left()
    ax_left.tick_params(labelright="off")
    ax_left.spines["right"].set_visible(False)

    ax_right.plot(h_axis, v_axis, **slice_opts)
    ax_right.set_ylabel(param["ylabel"])
    ax_right.set_xlabel(param["xlabel"])
    ax_right.yaxis.set_label_position("right")

    ax_right.set_xlim(*param["xlim_right"])
    ax_right.yaxis.tick_right()
    ax_right.spines["left"].set_visible(False)

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
    """
    Plot of 1D array.
    """

    def __init__(
        self, arr1d: np.ndarray, h_axis: np.ndarray, xlabel=r"", ylabel=r"", **kwargs
    ) -> None:
        r"""
        >>> plot = Plot1D(a0, z0, xlabel=r'$%s \;(\mu m)$'%'z', ylabel=r'$%s$'%'a_0',
                                xlim=[0, 900], ylim=[0, 10],
                                figsize=(10, 6), color='red')
        >>> plot.canvas.print_figure('a0.png')

        :param arr1d: data to be plotted on the "y" axis
        :param h_axis: values on the "x" axis
        :param xlabel: "x" axis label
        :param ylabel: "y" axis label
        :param kwargs: other arguments for ``matplotlib.plot()``
        """
        self.xlim = kwargs.pop("xlim", [np.min(h_axis), np.max(h_axis)])
        self.ylim = kwargs.pop("ylim", [np.min(arr1d), np.max(arr1d)])
        #
        xmin_idx, xmax_idx = (
            idx_from_val(h_axis, self.xlim[0]),
            idx_from_val(h_axis, self.xlim[1]),
        )
        #
        self.h_axis = h_axis[xmin_idx:xmax_idx]
        self.data = arr1d[xmin_idx:xmax_idx]
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

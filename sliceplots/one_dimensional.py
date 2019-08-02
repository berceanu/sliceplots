# -*- coding: utf-8 -*-

"""Module containing useful 1D plotting abstractions on top of matplotlib."""

import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

from sliceplots.util import _idx_from_val, _make_ax


def plot1d_break_x(h_axis, v_axis, param, slice_opts, ax=None):
    r"""Line plot with a broken x-axis.

    Parameters
    ----------
    h_axis : :py:class:`numpy.ndarray`
        x-axis data.
    v_axis : :py:class:`numpy.ndarray`
        y-axis data.
    param : dict
        Axes limits and labels.
    slice_opts : dict
        Options for plotted line.
    ax : :py:class:`matplotlib.axes.Axes`
        Axes instance, for plotting.
        If ``None``, a new :py:class:`Figure <matplotlib.figure.Figure>` will be created.
        Defaults to ``None``.

    Returns
    -------
    fig : :py:class:`matplotlib.figure.Figure`
        Figure instance.

    Examples
    --------
    >>> import numpy as np
    >>> uu = np.linspace(0, np.pi, 128)
    >>> data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)
    >>> plot1d_break_x(
    ...     ax=None,
    ...     h_axis=uu,
    ...     v_axis=data[data.shape[0] // 2, :],
    ...     param={
    ...         "xlim_left": (0, 1),
    ...         "xlim_right": (2, 3),
    ...         "xlabel": r"$x$ ($\mu$m)",
    ...         "ylabel": r"$\rho$ (cm${}^{-3}$)",
    ...     },
    ...     slice_opts={"ls": "--", "color": "#d62728"})  #doctest: +ELLIPSIS
    <Figure size ... with 2 Axes>

    """
    if ax is None:
        ax = _make_ax()

    fig = ax.figure
    ax_left = ax
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

    return fig


class Plot1D:
    r"""Plot the data with given labels and plot options.

    Parameters
    ----------
    v_axis : :py:class:`np.ndarray`
        y-axis data.
    h_axis : :py:class:`np.ndarray`
        x-axis data.
    xlabel : str
        x-axis label.
    ylabel : str
        y-axis label.
    ax : :py:class:`matplotlib.axes.Axes`
        Axes instance, for plotting.
        If ``None``, a new :py:class:`Figure <matplotlib.figure.Figure>` will be created.
        Defaults to ``None``.
    kwargs : dict
        Other arguments for :py:meth:`plot <matplotlib.axes.Axes.plot>`.

    Examples
    --------
    .. plot::
       :include-source:

        import numpy as np
        from matplotlib import pyplot

        from sliceplots import Plot1D

        uu = np.linspace(0, np.pi, 128)
        data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)

        fig = pyplot.figure()
        ax = fig.add_subplot(111)

        p1d = Plot1D(
            ax=ax,
            h_axis=uu,
            v_axis=data[data.shape[0] // 2, :],
            xlabel=r"$z$ ($\mu$m)",
            ylabel=r"$a_0$",
            xlim=[0, 3],
            ylim=[-1, 1],
            color="#d62728",
        )
        p1d.fig
    """

    def __init__(self, h_axis, v_axis, xlabel=r"", ylabel=r"", ax=None, **kwargs):
        self.xlim = kwargs.pop("xlim", [np.min(h_axis), np.max(h_axis)])
        self.ylim = kwargs.pop("ylim", [np.min(v_axis), np.max(v_axis)])
        #
        xmin_idx, xmax_idx = (
            _idx_from_val(h_axis, self.xlim[0]),
            _idx_from_val(h_axis, self.xlim[1]),
        )
        #
        self.h_axis = h_axis[xmin_idx:xmax_idx]
        self.data = v_axis[xmin_idx:xmax_idx]
        #
        self.label = {"x": xlabel, "y": ylabel}
        self.text = kwargs.pop("text", "")
        #
        if ax is None:
            ax = _make_ax()
        self.ax = ax

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

        self.fig = self.ax.figure

    def __str__(self):
        return "extent=({:.3f}, {:.3f}); min, max = ({:.3f}, {:.3f})".format(
            np.min(self.h_axis),
            np.max(self.h_axis),
            np.amin(self.data),
            np.amax(self.data),
        )

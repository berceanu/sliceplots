# -*- coding: utf-8 -*-

"""Module containing useful 1D plotting abstractions on top of matplotlib."""

import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize

from sliceplots.util import _idx_from_val, _make_ax, addcolorbar


label = (None,)


def plot_multicolored_line(*, ax=None, x, y, other_y, cmap="viridis", cbar_opts={}):
    r"""Plots a line colored based on the values of another array.

    Plots the curve ``y(x)``, colored based on the values in ``other_y``.

    Parameters
    ----------
    ax : :py:class:`matplotlib.axes.Axes`
        Axes instance, for plotting.
        If ``None``, a new :py:class:`Figure <matplotlib.figure.Figure>` will be created.
        Defaults to ``None``.
    y : 1d array_like
        The dependent variable.
    x : 1d array_like
        The independent variable.
    other_y: 1d array_like
        The values whose magnitude will be converted to colors.
    cmap : str
        The used colormap (defaults to "viridis").
    cbar_opts : dict
        Options for :py:func:`sliceplots.addcolorbar`.

    Raises
    ------
    AssertionError
        If the length of `y` and `other_y` do not match.

    References
    ----------
    Original ``matplotlib`` `example <https://matplotlib.org/gallery/lines_bars_and_markers/multicolored_line.html>`_.

    Examples
    --------
    We plot a curve and color it based on the value of its first derivative.

    .. plot::
       :include-source:

        import numpy as np
        from matplotlib import pyplot

        from sliceplots import plot_multicolored_line

        x = np.linspace(0, 3 * np.pi, 500)
        y = np.sin(x)
        dydx = np.gradient(y) * 100  # first derivative

        fig, ax = pyplot.subplots()

        plot_multicolored_line(ax=ax, x=x, y=y, other_y=dydx,
         cbar_opts={"label" : "dydx"})

        ax.set(ylabel="y", xlabel="x")
    """
    if not (len(y) == len(other_y)):
        raise AssertionError("The two 'y' arrays must have the same size!")

    if ax is None:
        ax = _make_ax()

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    norm = Normalize(other_y.min(), other_y.max())
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    # Set the values used for colormapping
    lc.set_array(other_y)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)

    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())

    addcolorbar(ax=ax, artist=line, **cbar_opts)


def plot1d_break_x(*, ax=None, h_axis, v_axis, param, slice_opts):
    r"""Line plot with a broken x-axis.

    Parameters
    ----------
    ax : :py:class:`matplotlib.axes.Axes`
        Axes instance, for plotting.
        If ``None``, a new :py:class:`Figure <matplotlib.figure.Figure>` will be created.
        Defaults to ``None``.
    h_axis : :py:class:`numpy.ndarray`
        x-axis data.
    v_axis : :py:class:`numpy.ndarray`
        y-axis data.
    param : dict
        Axes limits and labels.
    slice_opts : dict
        Options for plotted line.

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
    <matplotlib.axes._subplots.AxesSubplot object at 0x...>

    """
    if ax is None:
        ax = _make_ax()

    ax_left = ax
    divider = make_axes_locatable(ax_left)
    ax_right = divider.new_horizontal(size="100%", pad=1)
    ax.figure.add_axes(ax_right)

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

    return ax


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
    >>> import numpy as np

    >>> uu = np.linspace(0, np.pi, 128)
    >>> data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)

    >>> Plot1D(
    ...     h_axis=uu,
    ...     v_axis=data[data.shape[0] // 2, :],
    ...     xlabel=r"$z$ ($\mu$m)",
    ...     ylabel=r"$a_0$",
    ...     xlim=[0, 3],
    ...     ylim=[-1, 1],
    ...     color="#d62728",
    ... )  #doctest: +ELLIPSIS
    <sliceplots.one_dimensional.Plot1D object at 0x...>
    """

    def __init__(self, *, ax=None, h_axis, v_axis, xlabel=r"", ylabel=r"", **kwargs):
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

        self.ax.text(
            0.02, 0.95, self.text, transform=self.ax.transAxes, color="firebrick"
        )

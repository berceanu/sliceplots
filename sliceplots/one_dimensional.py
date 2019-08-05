# -*- coding: utf-8 -*-

"""Module containing useful 1D plotting abstractions on top of matplotlib."""

import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize

from sliceplots.util import _idx_from_val, _make_ax, addcolorbar


def plot_multicolored_line(*, ax=None, x, y, other_y, cmap="viridis", **cbar_opts):
    r"""Plots a line colored based on the values of another array.

    Plots the curve ``y(x)``, colored based on the values in ``other_y``.

    Parameters
    ----------
    ax : :py:class:`~matplotlib.axes.Axes`, optional
        Axes instance, for plotting, defaults to ``None``.
        If ``None``, a new :py:class:`~matplotlib.figure.Figure` will be created.

    y : 1d array_like
        The dependent variable.
    x : 1d array_like
        The independent variable.
    other_y: 1d array_like
        The values whose magnitude will be converted to colors.

    cmap : str, optional
        The used colormap (defaults to "viridis").
    cbar_opts : dict, optional
        Options for :meth:`~sliceplots.util.addcolorbar`.

    Returns
    -------
    ax, cax : tuple of Axes
        Main Axes and colorbar Axes.

    Raises
    ------
    AssertionError
        If the length of `y` and `other_y` do not match.

    References
    ----------
    ``matplotlib`` `example <https://matplotlib.org/gallery/lines_bars_and_markers/multicolored_line.html>`_.

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

        _, ax = pyplot.subplots()

        plot_multicolored_line(ax=ax, x=x, y=y, other_y=dydx, label="dydx")

        ax.set(ylabel="y", xlabel="x")
    """
    if not (len(y) == len(other_y)):
        raise AssertionError("The two 'y' arrays must have the same size!")

    ax = ax or _make_ax()

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

    cax = addcolorbar(ax=ax, mappable=line, **cbar_opts)

    return ax, cax


def plot1d_break_x(*, ax=None, h_axis, v_axis, param, slice_opts):
    r"""Line plot with a broken x-axis.

    Parameters
    ----------
    ax : :py:class:`~matplotlib.axes.Axes`, optional
        Axes instance, for plotting.
        If ``None``, a new :py:class:`~matplotlib.figure.Figure` will be created.
        Defaults to ``None``.
    h_axis : 1d array_like
        x-axis data.
    v_axis : 1d array_like
        y-axis data.
    param : dict
        Axes limits and labels.
    slice_opts : dict
        Options for plotted line.

    Returns
    -------
    ax_left, ax_right : tuple of Axes
        Left and right Axes of the split plot.

    Examples
    --------
    .. plot::
        :include-source:

            import numpy as np
            from matplotlib import pyplot

            from sliceplots import plot1d_break_x

            uu = np.linspace(0, np.pi, 128)
            data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)

            _, ax = pyplot.subplots()

            plot1d_break_x(
                ax=ax,
                h_axis=uu,
                v_axis=data[data.shape[0] // 2, :],
                param={
                    "xlim_left": (0, 1),
                    "xlim_right": (2, 3),
                    "xlabel": r"$x$ ($\mu$m)",
                    "ylabel": r"$\rho$ (cm${}^{-3}$)",
                },
                slice_opts={"ls": "--", "color": "#d62728"})

    """
    ax_left = ax or _make_ax()

    divider = make_axes_locatable(ax_left)
    ax_right = divider.new_horizontal(size="100%", pad=1)
    ax_left.figure.add_axes(ax_right)

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

    return ax_left, ax_right


def plot1d(*, ax=None, h_axis, v_axis, xlabel=r"", ylabel=r"", **kwargs):
    r"""Plot the data with given labels and plot options.

    Parameters
    ----------
    ax : class:`~matplotlib.axes.Axes`, optional
        Axes instance, for plotting.
        If ``None``, a new :class:`~matplotlib.figure.Figure` will be created.
        Defaults to ``None``.

    h_axis : :py:class:`np.ndarray`
        x-axis data.
    v_axis : :py:class:`np.ndarray`
        y-axis data.
    xlabel : str, optional
        x-axis label.
    ylabel : str, optional
        y-axis label.

    kwargs : dict, optional
        Other arguments for :meth:`~matplotlib.axes.Axes.plot`.

    Returns
    -------
    ax : Axes
        Modified Axes, containing plot.

    Examples
    --------
    >>> import numpy as np

    >>> uu = np.linspace(0, np.pi, 128)
    >>> data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)

    >>> plot1d(
    ...     h_axis=uu,
    ...     v_axis=data[data.shape[0] // 2, :],
    ...     xlabel=r"$z$ ($\mu$m)",
    ...     ylabel=r"$a_0$",
    ...     xlim=[0, 3],
    ...     ylim=[-1, 1],
    ...     color="#d62728",
    ... )  #doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at 0x...>
    """
    xlim = kwargs.pop("xlim", [np.min(h_axis), np.max(h_axis)])
    ylim = kwargs.pop("ylim", [np.min(v_axis), np.max(v_axis)])
    #
    xmin_idx, xmax_idx = (
        _idx_from_val(h_axis, xlim[0]),
        _idx_from_val(h_axis, xlim[1]),
    )
    #
    h_axis = h_axis[xmin_idx:xmax_idx]
    data = v_axis[xmin_idx:xmax_idx]
    #
    label = {"x": xlabel, "y": ylabel}
    text = kwargs.pop("text", "")
    #
    ax = ax or _make_ax()

    ax.plot(h_axis, data, **kwargs)

    ax.set(
        xlim=[h_axis[0], h_axis[-1]], ylim=ylim, ylabel=label["y"], xlabel=label["x"]
    )

    ax.text(0.02, 0.95, text, transform=ax.transAxes, color="firebrick")

    return ax

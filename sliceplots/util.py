# -*- coding: utf-8 -*-

"""Utility functions module."""

import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable


def addcolorbar(
    *,
    ax,
    artist,
    pos="right",
    size="5%",
    pad=0.05,
    orientation="vertical",
    stub=False,
    max_ticks=None,
    label=None,
):
    r"""Add a colorbar to a matplotlib image.

    Parameters
    ----------
    ax : :py:class:`matplotlib.axes.Axes`
        The axis object the image is drawn in.
    artist : :py:class:`matplotlib.image.AxesImage` etc.
        The matplotlib artist which is colored, eg. an image.

    Returns
    -------
    cax : :py:class:`matplotlib.axes.Axes`
        New axes instance, with attached colorbar.

    Notes
    -----
    When changed, please update `this gist <https://gist.github.com/skuschel/85f0645bd6e37509164510290435a85a>`_.

    Examples
    --------
    .. plot::
       :include-source:

        import numpy as np
        from matplotlib import pyplot

        from sliceplots import addcolorbar

        uu = np.linspace(0, np.pi, 128)
        data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)

        fig, ax = pyplot.subplots()
        img = ax.imshow(data)

        addcolorbar(ax=ax, artist=img, label="x")
    """
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(pos, size=size, pad=pad)
    if stub:
        cax.set_visible(False)
        return cax

    cb = ax.figure.colorbar(artist, cax=cax, orientation=orientation)
    if max_ticks is not None:
        from matplotlib import ticker

        tick_locator = ticker.MaxNLocator(nbins=max_ticks)
        cb.locator = tick_locator
        cb.update_ticks()
    if label is not None:
        cb.set_label(label)

    return cax


def _make_ax(**my_adjust):
    r"""

    Parameters
    ----------
    my_adjust : dict
        Parameters for tuning the subplot layout.

    Returns
    -------
    ax : :py:class:`matplotlib.axes.Axes`
        Axes instance, for plotting.

    Examples
    --------
    >>> _make_ax(left=0.15, right=0.98)  #doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at 0x...>
    """
    adjust = dict(
        left=0.125,  # the left side of the subplots of the figure
        right=0.9,  # the right side of the subplots of the figure
        bottom=0.1,  # the bottom of the subplots of the figure
        top=0.9,  # the top of the subplots of the figure
        wspace=0.2,  # the amount of width reserved for space between subplots,
        # expressed as a fraction of the average axis width
        hspace=0.2,  # the amount of height reserved for space between subplots,
        # expressed as a fraction of the average axis height
    )

    if not my_adjust.keys() <= adjust.keys():
        raise TypeError("Unknown keyword arg!")

    adjust.update(my_adjust)

    fig = Figure()
    canvas = FigureCanvas(fig)
    canvas.figure.subplots_adjust(**adjust)
    ax = canvas.figure.add_subplot(111)

    return ax


def _idx_from_val(arr1d, val):
    """Given a 1D array, find index of closest element to given value.

    Parameters
    ----------
    arr1d : arr1d: :py:class:`numpy.ndarray`
        1D array of values.
    val : float
        Element value.

    Returns
    -------
    idx : int
        Element position in the array.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.linspace(10, 20, 11)
    >>> _idx_from_val(a, 14.2)
    4
    """
    idx = (np.abs(arr1d - val)).argmin()
    return idx

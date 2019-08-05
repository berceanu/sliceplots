# -*- coding: utf-8 -*-

"""Utility functions module."""

import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import ticker
from mpl_toolkits.axes_grid1 import make_axes_locatable


def addcolorbar(*, ax, mappable, label=None, stub=False, **kwargs):
    r"""Add a colorbar to a matplotlib image.

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`, list of Axes, optional
        Parent axes from which space for a new colorbar axes will be stolen.
        If a list of axes is given they will all be resized to make room for the
        colorbar axes.
    mappable : :class:`~matplotlib.cm.ScalarMappable`
        The :class:`~matplotlib.image.Image`,
        :class:`~matplotlib.contour.ContourSet`, etc.
        described by this colorbar.

    label : str, optional
        Colorbar axis label (defaults to ``None``).
    stub : bool, optional
        If ``True``, return the Axes into which the colorbar was drawn.
        The colorbar is invisible in this case. Defaults to ``False``.

    kwargs : dict, optional
        Keyword arguments that control the look of the colorbar.
        Optional keyword arguments include:

        ============= ====================================================
        Property      Description
        ============= ====================================================
        pos           position wrt parent axes: left, right, bottom or top
        size          5%; width, in percentage of the original axes width
        orientation   vertical or horizontal
        pad           0.05 if vertical, 0.15 if horizontal; fraction
                      of original axes between colorbar and new image axes
        max_ticks     maximum number of tick marks on the colorbar
        ============= ====================================================

    Returns
    -------
    cax : :class:`~matplotlib.axes.Axes`
        New axes instance, with drawn colorbar.

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

        addcolorbar(ax=ax, mappable=img, label="x")
    """
    max_ticks = kwargs.pop("max_ticks", None)

    pos = kwargs.pop("pos", "right")
    size = kwargs.pop("size", "5%")
    orientation = kwargs.pop("orientation", "vertical")

    default_pad = 0.05
    if orientation == "horizontal":
        default_pad = 0.15
    pad = kwargs.pop("pad", default_pad)

    divider = make_axes_locatable(axes=ax)
    cax = divider.append_axes(position=pos, size=size, pad=pad)

    if stub:
        cax.set_visible(False)
        return cax

    cb = ax.figure.colorbar(mappable=mappable, cax=cax, orientation=orientation)

    if max_ticks is not None:
        tick_locator = ticker.MaxNLocator(nbins=max_ticks)
        cb.locator = tick_locator
        cb.update_ticks()

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

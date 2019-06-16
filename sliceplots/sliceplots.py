# -*- coding: utf-8 -*-

"""Main module, containing useful plotting abstractions on top of matplotlib."""

import numpy as np
from matplotlib.artist import setp, getp
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def idx_from_val(arr1d, val):
    """Given a 1D array `arr1d`, find index of closest value to `val`."""
    idx = (np.abs(arr1d - val)).argmin()
    return idx


class Plot2D:
    """
    Pseudocolor plot of a 2D array with optional 1D slices attached.
    """

    def __init__(
        self,
        arr2d: np.ndarray,
        h_axis: np.ndarray,
        v_axis: np.ndarray,
        xlabel=r"",
        ylabel=r"",
        zlabel=r"",
        **kwargs
    ) -> None:
        r"""
        >>> uu = np.linspace(0, np.pi, 128)
        >>> data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)
        >>> p2d = Plot2D(data, uu, uu,
                    xlabel=r'$x$ ($\mu$m)', ylabel=r'$y$ ($\mu$m)', zlabel=r'$\rho$ (cm$^{-3}$)',
                    hslice_val=0,
                    vslice_val=840.5,
                    hslice_opts={'color': 'firebrick', 'lw' : 0.5, 'ls':'-'},
                    vslice_opts={'color': 'blue', 'ls': '-'},
                    figsize=(8, 8), cmap='viridis', cbar=True,
                    extent=(822, 865, -20, 20),
                    vmin=-0.1, vmax=10,
                    text='iteration = {}'.format(35100),
                    norm=colors.SymLogNorm(linthresh=1e-4)
                    )
        Other options for norm:
        >>> import matplotlib.colors as colors
        >>> norm = colors.LogNorm()

        :param arr2d: data to be plotted
        :param h_axis: values on the "x" axis
        :param v_axis: values on the "y" axis
        :param xlabel: "x" axis label
        :param ylabel: "y" axis label
        :param zlabel: colorbar label
        :param kwargs: other arguments for ``matplotlib``
        """
        self.extent = kwargs.get(
            "extent", (np.min(h_axis), np.max(h_axis), np.min(v_axis), np.max(v_axis))
        )
        #
        xmin, xmax, ymin, ymax = self.extent
        xmin_idx, xmax_idx = idx_from_val(h_axis, xmin), idx_from_val(h_axis, xmax)
        ymin_idx, ymax_idx = idx_from_val(v_axis, ymin), idx_from_val(v_axis, ymax)
        #
        self.data = arr2d[ymin_idx:ymax_idx, xmin_idx:xmax_idx]
        self.min_data, self.max_data = np.amin(self.data), np.amax(self.data)
        self.vmin, self.vmax = (
            kwargs.get("vmin", self.min_data),
            kwargs.get("vmax", self.max_data),
        )
        #
        self.h_axis = h_axis[xmin_idx:xmax_idx]
        self.v_axis = v_axis[ymin_idx:ymax_idx]
        # np.clip(self.data, self.vmin, self.vmax, self.data)
        #
        self.label = {"x": xlabel, "y": ylabel, "z": zlabel}
        #
        self.cbar = kwargs.get("cbar", True)
        # see https://matplotlib.org/users/colormapnorms.html
        self.norm = kwargs.get("norm")
        #
        self.hslice_val = kwargs.get("hslice_val")
        self.vslice_val = kwargs.get("vslice_val")
        self.hslice_idx = None
        self.vslice_idx = None
        if self.hslice_val is not None:
            self.hslice_idx = idx_from_val(self.v_axis, self.hslice_val)
        if self.vslice_val is not None:
            self.vslice_idx = idx_from_val(self.h_axis, self.vslice_val)
            #
        #
        self.text = kwargs.get("text", "")
        #
        self.fig = Figure(figsize=kwargs.pop("figsize", (8, 8)))
        # A canvas must be manually attached to the figure (pyplot would automatically
        # do it).  This is done by instantiating the canvas with the figure as
        # argument.
        self.canvas = FigureCanvas(self.fig)
        #
        self.draw_fig(**kwargs)

    def __str__(self):
        return "extent=({:.3f}, {:.3f}, {:.3f}, {:.3f}); min, max = ({:.3f}, {:.3f})".format(
            np.min(self.h_axis),
            np.max(self.h_axis),
            np.min(self.v_axis),
            np.max(self.v_axis),
            np.amin(self.data),
            np.amax(self.data),
        )

    @staticmethod
    def colorbar(mappable):
        r"""Constructs a scaled colorbar for a given plot.

        Parameters
        ----------
        mappable : The Image, ContourSet, etc. to which the colorbar applies.
        """
        ax = mappable.axes
        fig = ax.figure
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        return fig.colorbar(mappable, cax=cax)

    def main_panel(self, **kwargs):
        self.im = self.ax0.imshow(
            self.data,
            origin="lower",
            extent=self.extent,
            aspect="auto",
            norm=self.norm,
            interpolation="none",
            cmap=kwargs.get("cmap", "viridis"),
            vmin=self.vmin,
            vmax=self.vmax,
        )
        #
        self.ax0.set_xlabel(self.label["x"])
        self.ax0.set_ylabel(self.label["y"])

    def draw_fig(self, **kwargs):
        slice_opts = {"ls": "-", "color": "firebrick", "lw": 0.5}  # defaults
        hslice_opts = slice_opts.copy()
        vslice_opts = slice_opts.copy()
        #
        hslice_opts.update(kwargs.get("hslice_opts", {}))
        vslice_opts.update(kwargs.get("vslice_opts", {}))

        # #
        if (self.hslice_idx is None) and (self.vslice_idx is None):
            gs = GridSpec(1, 1, height_ratios=[1], width_ratios=[1])
            self.ax0 = self.fig.add_subplot(gs[0])
            self.main_panel(**kwargs)

        # ---- #
        elif (self.hslice_idx is not None) and (self.vslice_idx is None):
            gs = GridSpec(2, 1, height_ratios=[1, 3], width_ratios=[1])
            self.ax0 = self.fig.add_subplot(gs[1, 0])
            self.axh = self.fig.add_subplot(gs[0, 0], sharex=self.ax0)
            #
            self.main_panel(**kwargs)
            #
            self.ax0.axhline(y=self.v_axis[self.hslice_idx], **hslice_opts)
            #
            self.ax0.annotate(
                "{:.1f}".format(self.v_axis[self.hslice_idx]),
                xy=(self.h_axis[3], self.v_axis[self.hslice_idx + 3]),
                xycoords="data",
                color=hslice_opts["color"],
            )
            #
            self.axh.set_xmargin(0)
            self.axh.set_ylabel(self.label["z"])
            self.axh.plot(self.h_axis, self.data[self.hslice_idx, :], **hslice_opts)
            self.axh.set_ylim(self.vmin, self.vmax)
            #
            self.axh.xaxis.set_visible(False)
            #
            for sp in ("top", "bottom", "right"):
                self.axh.spines[sp].set_visible(False)
            #
            self.fig.subplots_adjust(hspace=0.03)

        # | #
        elif (self.vslice_idx is not None) and (self.hslice_idx is None):
            gs = GridSpec(1, 2, height_ratios=[1], width_ratios=[3, 1])
            self.ax0 = self.fig.add_subplot(gs[0, 0])
            self.axv = self.fig.add_subplot(gs[0, 1], sharey=self.ax0)
            #
            self.main_panel(**kwargs)
            #
            self.ax0.axvline(x=self.h_axis[self.vslice_idx], **vslice_opts)
            #
            self.ax0.annotate(
                "{:.1f}".format(self.h_axis[self.vslice_idx]),
                xy=(self.h_axis[self.vslice_idx - 40], self.v_axis[-40]),
                xycoords="data",
                color=vslice_opts["color"],
                rotation="vertical",
            )
            #
            self.axv.set_ymargin(0)
            self.axv.set_xlabel(self.label["z"])
            self.axv.plot(self.data[:, self.vslice_idx], self.v_axis, **vslice_opts)
            self.axv.set_xlim(self.vmin, self.vmax)
            #
            self.axv.yaxis.set_visible(False)
            #
            for sp in ("top", "left", "right"):
                self.axv.spines[sp].set_visible(False)
            #
            self.fig.subplots_adjust(wspace=0.03)

        # --|-- #
        else:
            gs = GridSpec(2, 2, height_ratios=[1, 3], width_ratios=[3, 1])
            self.ax0 = self.fig.add_subplot(gs[1, 0])
            self.axh = self.fig.add_subplot(gs[0, 0], sharex=self.ax0)
            self.axv = self.fig.add_subplot(gs[1, 1], sharey=self.ax0)
            #
            self.main_panel(**kwargs)
            #
            self.ax0.axhline(y=self.v_axis[self.hslice_idx], **hslice_opts)  # ##----##
            self.ax0.axvline(x=self.h_axis[self.vslice_idx], **vslice_opts)  # ## | ##
            # --- #
            self.ax0.annotate(
                "{:.1f}".format(self.v_axis[self.hslice_idx]),
                xy=(self.h_axis[3], self.v_axis[self.hslice_idx + 3]),
                xycoords="data",
                color=hslice_opts["color"],
            )
            # | #
            self.ax0.annotate(
                "{:.1f}".format(self.h_axis[self.vslice_idx]),
                xy=(self.h_axis[self.vslice_idx - 40], self.v_axis[-40]),
                xycoords="data",
                color=vslice_opts["color"],
                rotation="vertical",
            )
            # --- #
            self.axh.set_xmargin(0)  # otherwise ax0 may have white margins
            self.axh.set_ylabel(self.label["z"])
            self.axh.plot(self.h_axis, self.data[self.hslice_idx, :], **hslice_opts)
            self.axh.set_ylim(self.vmin, self.vmax)
            # self.axh.set_yticks([-1, 0, 1])
            # | #
            self.axv.set_ymargin(0)
            self.axv.set_xlabel(self.label["z"])
            self.axv.plot(self.data[:, self.vslice_idx], self.v_axis, **vslice_opts)
            self.axv.set_xlim(self.vmin, self.vmax)
            # hide the relevant axis
            self.axh.xaxis.set_visible(False)  # -
            self.axv.yaxis.set_visible(False)  # |
            # "Despine" the slice profiles
            for ax, spines in (
                (self.axh, ("top", "bottom", "right")),
                (self.axv, ("top", "left", "right")),
            ):
                #
                for sp in spines:
                    ax.spines[sp].set_visible(False)
            #
            self.fig.subplots_adjust(wspace=0.03, hspace=0.03)

        # self.fig.tight_layout()
        #
        self.ax0.text(
            0.02, 0.02, self.text, transform=self.ax0.transAxes, color="firebrick"
        )
        #
        if self.cbar:
            cax = inset_axes(self.ax0, width="70%", height="3%", loc=2)
            cbar = self.fig.colorbar(
                self.im, cax=cax, orientation="horizontal"
            )  # ticks=[self.vmin, self.vmax]
            # cbar.set_label(self.label['z'], color='firebrick')
            self.ax0.text(
                0.74,
                0.97,
                self.label["z"],
                transform=self.ax0.transAxes,
                color="firebrick",
            )
            # cbar.ax.xaxis.set_ticks_position('top')
            # cbar.ax.xaxis.set_label_position('top')
            cbar.ax.tick_params(color="firebrick", width=1.5, labelsize=8)
            cbxtick_obj = getp(cbar.ax.axes, "xticklabels")
            setp(cbxtick_obj, color="firebrick")


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

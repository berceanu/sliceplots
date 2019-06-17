=====
Usage
=====

To use ``sliceplots`` in a project, we first import it and generate some data::

    import sliceplots.one_dimensional as one_d
    import matplotlib.pyplot as plt
    import numpy as np

    # data for plotting
    uu = np.linspace(0, np.pi, 128)
    data = np.cos(uu - 0.5) * np.cos(uu.reshape(-1, 1) - 1.0)

here is an example of a "broken-axis" plot::

    fig, ax = plt.subplots(figsize=(8, 3.2))
    one_d.plot1d_break_x(fig, uu, data[data.shape[0] // 2, :],
                         {'xlim_left': (0, 1),
                          'xlim_right': (2, 3),
                          'xlabel': r'$x$ ($\mu$m)',
                          'ylabel': r'$\rho$ (cm$^{-3}$)'},
                         {'ls': '--', 'color': 'red'})
    fig.savefig("test_plot1d_break_x.png")

.. image:: ../tests/baseline/test_plot1d_break_x.png

The :py:class:`Plot1D` class is a very thin wrapper around :py:func:`matplotlib.axes.Axes.plot`::

    plot = one_d.Plot1D(uu,
                        data[data.shape[0] // 2, :],
                        xlabel=r'$%s \;(\mu m)$' % 'z',
                        ylabel=r'$%s$' % 'a_0',
                        xlim=[0, 3],
                        ylim=[-1, 1],
                        figsize=(10, 6),
                        color='red')
    plot.canvas.print_figure('test_plot1d.png')

.. image:: ../tests/baseline/test_plot1d.png

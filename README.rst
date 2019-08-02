===========
Slice Plots
===========


.. image:: https://img.shields.io/pypi/v/sliceplots.svg
   :target: https://pypi.python.org/pypi/sliceplots


.. image:: https://img.shields.io/travis/berceanu/sliceplots.svg
   :target: https://travis-ci.org/berceanu/sliceplots


.. image:: https://readthedocs.org/projects/sliceplots/badge/?version=latest
   :target: https://sliceplots.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://pyup.io/repos/github/berceanu/sliceplots/shield.svg
   :target: https://pyup.io/repos/github/berceanu/sliceplots/
   :alt: Updates


.. image:: https://codecov.io/gh/berceanu/sliceplots/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/berceanu/sliceplots


.. image:: https://img.shields.io/pypi/l/sliceplots.svg
   :target: https://github.com/berceanu/sliceplots/blob/master/LICENSE
   :alt: PyPI - License


thin wrapper on top of ``matplotlib``'s ``.imshow()`` for 2D plotting, with attached slice plots


* Free software: BSD license
* Documentation: https://sliceplots.readthedocs.io

Features
--------

* only depends on ``matplotlib``
* uses its pure OO (look Ma, no ``pyplot``!) interface
* support for 1D and 2D plots with various customization options
* broken-axis 1D plots
* small codebase
* designed for non-interactive use, scripting and publication-quality plots

Quick start
-----------

Install the package via:

.. code-block:: console

        $ pip install sliceplots

Generate a quick slice plot:

.. plot::
   :include-source:

    from sliceplots import Plot2D

    axis_data = np.linspace(0, np.pi, 128)
    data_2d = np.cos(axis_data - 0.5) * np.cos(axis_data.reshape(-1, 1) - 1.0)

    Plot2D(
        data_2d,
        axis_data,  # horiz. axis
        axis_data,  # vert. axis
        xlabel="x",
        ylabel="y",
        zlabel="f(x,y)",
        hslice_val=0.75,
        vslice_val=2.75,
    )


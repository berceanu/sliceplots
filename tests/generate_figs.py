#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

import sliceplots.two_dimensional as two_d

if __name__ == '__main__':
    axis_data = np.linspace(0, np.pi, 128)
    data_2d = np.cos(axis_data - 0.5) * np.cos(axis_data.reshape(-1, 1) - 1.0)

    p2d = two_d.Plot2D(data_2d,
                       axis_data,
                       axis_data,
                       xlabel='x',
                       ylabel='y',
                       zlabel='f(x,y)',
                       hslice_val=0.75,
                       vslice_val=2.75,
                       figsize=(6.0, 6.0)
                       )
    p2d.fig.savefig("imshow_slices.png", bbox_inches='tight')

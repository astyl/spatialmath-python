#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:19:04 2020

@author: corkep

"""

import numpy as np
import numpy.testing as nt
import unittest
from math import pi
import math
from scipy.linalg import logm, expm

from spatialmath.base.transforms2d import *
from spatialmath.base.transformsNd import isR, t2r, r2t, rt2tr, skew

import matplotlib.pyplot as plt


class Test2D(unittest.TestCase):
    def test_rot2(self):
        R = np.array([[1, 0], [0, 1]])
        nt.assert_array_almost_equal(rot2(0), R)
        nt.assert_array_almost_equal(rot2(0, unit="rad"), R)
        nt.assert_array_almost_equal(rot2(0, unit="deg"), R)
        nt.assert_array_almost_equal(rot2(0, "deg"), R)
        nt.assert_almost_equal(np.linalg.det(rot2(0)), 1)

        R = np.array([[0, -1], [1, 0]])
        nt.assert_array_almost_equal(rot2(pi / 2), R)
        nt.assert_array_almost_equal(rot2(pi / 2, unit="rad"), R)
        nt.assert_array_almost_equal(rot2(90, unit="deg"), R)
        nt.assert_array_almost_equal(rot2(90, "deg"), R)
        nt.assert_almost_equal(np.linalg.det(rot2(pi / 2)), 1)

        R = np.array([[-1, 0], [0, -1]])
        nt.assert_array_almost_equal(rot2(pi), R)
        nt.assert_array_almost_equal(rot2(pi, unit="rad"), R)
        nt.assert_array_almost_equal(rot2(180, unit="deg"), R)
        nt.assert_array_almost_equal(rot2(180, "deg"), R)
        nt.assert_almost_equal(np.linalg.det(rot2(pi)), 1)

    def test_trot2(self):
        nt.assert_array_almost_equal(
            trot2(pi / 2, t=[3, 4]), np.array([[0, -1, 3], [1, 0, 4], [0, 0, 1]])
        )
        nt.assert_array_almost_equal(
            trot2(pi / 2, t=(3, 4)), np.array([[0, -1, 3], [1, 0, 4], [0, 0, 1]])
        )
        nt.assert_array_almost_equal(
            trot2(pi / 2, t=np.array([3, 4])),
            np.array([[0, -1, 3], [1, 0, 4], [0, 0, 1]]),
        )

    def test_Rt(self):
        nt.assert_array_almost_equal(rot2(0.3), t2r(trot2(0.3)))
        nt.assert_array_almost_equal(trot2(0.3), r2t(rot2(0.3)))

        R = rot2(0.2)
        t = [1, 2]
        T = rt2tr(R, t)
        nt.assert_array_almost_equal(t2r(T), R)
        nt.assert_array_almost_equal(transl2(T), np.array(t))
        # TODO

    def test_trlog2(self):
        R = rot2(0.5)
        nt.assert_array_almost_equal(trlog2(R), skew(0.5))

        T = transl2(1, 2) @ trot2(0.5)
        nt.assert_array_almost_equal(logm(T), trlog2(T))

    def test_trexp2(self):
        R = trexp2(skew(0.5))
        nt.assert_array_almost_equal(R, rot2(0.5))

        T = transl2(1, 2) @ trot2(0.5)
        nt.assert_array_almost_equal(trexp2(logm(T)), T)

    def test_transl2(self):
        nt.assert_array_almost_equal(
            transl2(1, 2), np.array([[1, 0, 1], [0, 1, 2], [0, 0, 1]])
        )
        nt.assert_array_almost_equal(
            transl2([1, 2]), np.array([[1, 0, 1], [0, 1, 2], [0, 0, 1]])
        )

    def test_print2(self):

        T = transl2(1, 2) @ trot2(0.3)

        s = trprint2(T, file=None)
        self.assertIsInstance(s, str)
        self.assertEqual(len(s), 15)

    def test_checks(self):
        # 2D case, with rotation matrix
        R = np.eye(2)
        nt.assert_equal(isR(R), True)
        nt.assert_equal(isrot2(R), True)

        nt.assert_equal(ishom2(R), False)
        nt.assert_equal(isrot2(R, True), True)

        nt.assert_equal(ishom2(R, True), False)

        # 2D case, invalid rotation matrix
        R = np.array([[1, 1], [0, 1]])
        nt.assert_equal(isR(R), False)
        nt.assert_equal(isrot2(R), True)
        nt.assert_equal(ishom2(R), False)
        nt.assert_equal(isrot2(R, True), False)
        nt.assert_equal(ishom2(R, True), False)

        # 2D case, with homogeneous transformation matrix
        T = np.array([[1, 0, 3], [0, 1, 4], [0, 0, 1]])
        nt.assert_equal(isR(T), False)
        nt.assert_equal(isrot2(T), False)

        nt.assert_equal(ishom2(T), True)
        nt.assert_equal(isrot2(T, True), False)

        nt.assert_equal(ishom2(T, True), True)

        # 2D case, invalid rotation matrix
        T = np.array([[1, 1, 3], [0, 1, 4], [0, 0, 1]])
        nt.assert_equal(isR(T), False)
        nt.assert_equal(isrot2(T), False)

        nt.assert_equal(ishom2(T), True)
        nt.assert_equal(isrot2(T, True), False)

        nt.assert_equal(ishom2(T, True), False)

        # 2D case, invalid bottom row
        T = np.array([[1, 1, 3], [0, 1, 4], [9, 0, 1]])
        nt.assert_equal(isR(T), False)
        nt.assert_equal(isrot2(T), False)

        nt.assert_equal(ishom2(T), True)
        nt.assert_equal(isrot2(T, True), False)

        nt.assert_equal(ishom2(T, True), False)

    def test_trinterp2(self):

        T0 = trot2(-0.3)
        T1 = trot2(0.3)

        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0), T0)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=1), T1)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0.5), np.eye(3))

        T0 = transl2(-1, -2)
        T1 = transl2(1, 2)

        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0), T0)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=1), T1)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0.5), np.eye(3))

        T0 = transl2(-1, -2) @ trot2(-0.3)
        T1 = transl2(1, 2) @ trot2(0.3)

        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0), T0)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=1), T1)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0.5), np.eye(3))

        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0), T0)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=1), T1)
        nt.assert_array_almost_equal(trinterp2(start=T0, end=T1, s=0.5), np.eye(3))

    def test_plot(self):
        plt.figure()
        trplot2(transl2(1, 2), block=False, frame="A", rviz=True, width=1)
        trplot2(transl2(3, 1), block=False, color="red", arrow=True, width=3, frame="B")
        trplot2(
            transl2(4, 3) @ trot2(math.pi / 3), block=False, color="green", frame="c"
        )
        plt.close("all")


# ---------------------------------------------------------------------------------------#
if __name__ == "__main__":

    unittest.main()

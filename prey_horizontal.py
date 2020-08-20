#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import QDS
from numpy import sin, cos, pi, rad2deg, deg2rad, arange


class HorizontalDot:
    next_id = 0

    def __init__(self, width=20, height=5,
                 #width and height defines the size of the object
                 azimuth=0, altitude=0,
                 circulation_frequency=0, circulation_anticlockwise=True, initial_circulation_angle=0.,
                 #cir_frequency: for speed of rotation
                 circulation_radius=30., #size of the circle it makes
                 rotation_frequency=None, rotation_anticlockwise=None, initial_rotation_angle=None,
                 #rotation_frequency: rotation of the object as it moves around the circulation (None  = 0)
                 t0=0, color=(255, 255, 255), magnification=(1.0, 1.0)):
        self._w = width
        self._h = height

        self._azi = azimuth
        self._alt = altitude

        self._f = circulation_frequency
        self._cir_dir = 1 if circulation_anticlockwise else -1
        self._theta0 = deg2rad(initial_circulation_angle)

        self._r = circulation_radius

        self._fr = rotation_frequency if rotation_frequency else circulation_frequency
        self._rot_dir = -self._cir_dir if rotation_anticlockwise is None else 1 if rotation_anticlockwise else -1
        self._phi0 = initial_rotation_angle if initial_rotation_angle else deg2rad(initial_circulation_angle)

        self._t = t0
        self._color = color
        self._mag = magnification

        self._id = self.next_id
        self.next_id += 1

    def __call__(self, t):
        self._t = t

    def init(self):
        QDS.DefObj_Ellipse(self.id, self._w, self._h) #shape define width and height
        QDS.SetObjColor(1, [self.id], [self.color]) # color


    @property
    def color(self):
        return self._color

    @property
    def id(self):
        return self._id

    @property
    def magnification(self):
        return self._mag

    @property
    def rotation(self):
        return rad2deg(self._phi0 + self._rot_dir * 2 * pi * self._fr * self._t)

    @property
    def x(self):
        return self._x0 + self._r * cos(self._theta)

    @property
    def xy(self):
        return self.x, self.y

    @property
    def y(self):
        return self._y0 + self._r * sin(self._theta)

    @property
    def _theta(self):
        return self._theta0 + self._cir_dir * 2 * pi * self._f * self._t

    @property
    def _x0(self):
        return self._azi

    @property
    def _y0(self):
        return self._alt

frame_duration = 1 / 60
background_color = (10, 20, 30, 30, 20, 10)  # line 104
n_trials = 1

dot = HorizontalDot()

def HorizontalDotSequence():
    for i in range(400):
        t = i * frame_duration
        dot(t)
        QDS.Scene_RenderEx(frame_duration, [dot.id], [dot.xy], [dot.magnification], [dot.rotation])


# --------------------------------------------------------------------------
# Main script
# --------------------------------------------------------------------------
QDS.Initialize("HorizontalDot", "horizonal moving dot")

QDS.StartScript()

dot.init()

QDS.SetBkgColor(background_color)

QDS.Loop(n_trials, HorizontalDotSequence)

QDS.EndScript()

# --------------------------------------------------------------------------

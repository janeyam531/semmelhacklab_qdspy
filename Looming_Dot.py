#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import collections
from functools import partial
import QDS
import math

# Define global stimulus parameters
loom = {'_sName': "Looming Dot",
        '_sDescr': "Dot of increasing size",

        "loom_nTrials": 10,

        "initial_dot_um": 1, # dot size
        "max_size": 30, #maxium for max_size * mag_rate is 800
        "mag_rate": 1, # rate at which it magnifies

         "origin_x": 0,
         "origin_y": 0,

         "loom_bkgColor": (0, 0, 0),  # background color
         "BoxColor": (255, 255, 255),  # bar color

        "durFr_s": 1 / 60.0,  # Frame duration
        "nFrPerMarker": 0 # afffects the math in durMarker_s
        }

def build_loomingstimulus(loom):
    # Define stimulus objects
    QDS.DefObj_Ellipse(1, loom['initial_dot_um'], loom['initial_dot_um'])

def LoomingDotSeq():
    # A function that presents the dot and increases its size by increasing the magnification in Scene_RenderEx
    for dot_size in range(loom['max_size']):
        a = dot_size * (loom['mag_rate'])
        b = dot_size * (loom['mag_rate'])
        # print ("(", x, y, ")")
        for iStep in range(1):
            QDS.Scene_RenderEx(loom["durFr_s"], [1], [(loom["origin_x"], loom["origin_y"])], [(a, b)], [0], 0)
    QDS.Scene_Clear(0.5, 0)

def loom_iterateStimulus(loom):
    QDS.SetObjColor(1, [1], [loom["BoxColor"]])
    QDS.SetBkgColor(loom["loom_bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(loom["loom_nTrials"], LoomingDotSeq)

# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize, loom['_sName'], loom['_sDescr'])),
    ('log', partial(QDS.LogUserParameters, loom)),
    ('build', partial(build_loomingstimulus, loom)),
    ('start', QDS.StartScript),
    ('clear1', partial(QDS.Scene_Clear, 0.0, 0)),
    ('iter1', partial(loom_iterateStimulus, loom)),
    ('clear2', partial(QDS.Scene_Clear, 0.0, 0)),
    ('stop', QDS.EndScript)]
)

[dispatcher[process]() for process in list(dispatcher.keys())]
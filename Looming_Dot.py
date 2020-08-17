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
        "nTrials": 5,

        "initial_dot_um": 1, # dot size
        "max_size": 50, #maxium for max_size * mag_rate is 800
        "mag_rate": 3, # rate at which it magnifies

         "origin_x": 0,
         "origin_y": 0,

         "bkgColor": (0, 0, 0),  # background color
         "ellipseColor": (255, 255, 255),  # bar color

        "durFr_s": 1 / 60.0,  # Frame duration
        "nFrPerMarker": 0 # afffects the math in durMarker_s
        }

def buildStimulus(loom):
    # Define stimulus objects
    QDS.DefObj_Ellipse(1, loom['initial_dot_um'], loom['initial_dot_um'])

def LoomingEllipseSeq():
    # A function that presents the dot and increases its size by increasing the magnification in Scene_RenderEx
    for dot_size in range(loom['max_size']):
        x = dot_size * (loom['mag_rate'])
        y = dot_size * (loom['mag_rate'])
        # print ("(", x, y, ")")
        for iStep in range(1):
            QDS.Scene_RenderEx(loom["durFr_s"], [1], [(loom["origin_x"], loom["origin_y"])], [(x, y)], [0], 0)

def iterateStimulus(loom):
    QDS.SetObjColor(1, [1], [loom["ellipseColor"]])
    QDS.SetBkgColor(loom["bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(loom["nTrials"], LoomingEllipseSeq)

# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize, loom['_sName'], loom['_sDescr'])),
    ('log', partial(QDS.LogUserParameters, loom)),
    ('build', partial(buildStimulus, loom)),
    ('start', QDS.StartScript),
    ('clear1', partial(QDS.Scene_Clear, 1.0, 0)),
    ('iter1', partial(iterateStimulus, loom)),
    ('clear2', partial(QDS.Scene_Clear, 0.0, 0)),
    ('stop', QDS.EndScript)]
)

[dispatcher[process]() for process in list(dispatcher.keys())]
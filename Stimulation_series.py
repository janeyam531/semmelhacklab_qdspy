#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import collections
from functools import partial
import QDS
import math

# Define global stimulus parameters
loom = {'loom_sName': "Looming Dot",
        'loom_sDescr': "Dot of increasing size",

        "loom_nTrials": 8,

        "initial_dot_um": 1, # dot size
        "max_size": 50, #maxium for max_size * mag_rate is 800
        "mag_rate": 3, # rate at which it magnifies

         "origin_x": 0,
         "origin_y": 0,

         "loom_bkgColor": (0, 0, 0),  # background color
         "DotColor": (255, 255, 255),  # bar color

        "durFr_s": 1 / 60.0,  # Frame duration
        "nFrPerMarker": 0 # afffects the math in durMarker_s
        }

p = {'_sName': "Prey_Vibration",
     '_sDescr': "horizontal vibrating 'moving ellipse'",
     "p_nTrials": 8,

     "DirList":[0, 180], #controls the directionality in which the dot moves in order
     "vel_umSec": 200.0,  # speed of moving bar in um/sec
     "tMoveDur_s": .8,  # duration of movement (defines distance
     # the bar travels, not its speed)

     "ellipseDx_um": 25.0,  # bar dimensions in um width
     "ellipseDy_um": 15.0,  # height

     "p_bkgColor": (0, 0, 0),  # background color
     "p_ellipseColor": (255, 255, 255),  # bar color

     "durFr_s"         : 1/60.0, # Frame duration
     "nFrPerMarker"    : 0
     }

def build_loomingstimulus(loom):
    # Define stimulus objects
    QDS.DefObj_Ellipse(1, loom['initial_dot_um'], loom['initial_dot_um'])

def prey_buildStimulus(p):
    p['durMarker_s'] = p["durFr_s"] * p["nFrPerMarker"]
    p['freq_Hz'] = round(1.0 / p["durFr_s"])
    p['umPerFr'] = float(p["vel_umSec"]) / p['freq_Hz']
    p['moveDist_um'] = p["vel_umSec"] * p["tMoveDur_s"]
    p['nFrToMove'] = float(p['moveDist_um']) / p['umPerFr']

    QDS.DefObj_Ellipse(2, p["ellipseDx_um"], p["ellipseDy_um"])

def LoomingDotSeq():
    # A function that presents the dot and increases its size by increasing the magnification in Scene_RenderEx
    for dot_size in range(loom['max_size']):
        a = dot_size * (loom['mag_rate'])
        b = dot_size * (loom['mag_rate'])
        # print ("(", x, y, ")")
        for iStep in range(1):
            QDS.Scene_RenderEx(loom["durFr_s"], [1], [(loom["origin_x"], loom["origin_y"])], [(a, b)], [0], 0)

def MoveEllipseSeq():
    # A function that presents the moving bar in the given number of
    # directions (= moving bar sequence)
    for rot_deg in p["DirList"]:
        rot_rad = (rot_deg) / 360.0 * 2 * math.pi
        x = math.cos(rot_rad) * (p['moveDist_um'] / 2.0)
        y = math.sin(rot_rad) * (-p['moveDist_um'] / 2.0)

        for iStep in range(int(p['nFrToMove'])):
            QDS.Scene_RenderEx(p["durFr_s"], [2], [(x, y)], [(1.0, 1.0)], [rot_deg], 0)
            x -= math.cos(rot_rad) * p['umPerFr']
            y += math.sin(rot_rad) * p['umPerFr']

def loom_iterateStimulus(loom):
    QDS.SetObjColor([1],[1,2], [loom["DotColor"], p["p_ellipseColor"]])
    QDS.SetBkgColor(loom["loom_bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(loom["loom_nTrials"], LoomingDotSeq)

def prey_iterateStimulus(p):
    QDS.SetObjColor([1],[1,2], [loom["DotColor"], p["p_ellipseColor"]])
    QDS.SetBkgColor(p["p_bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(p["p_nTrials"], MoveEllipseSeq)

# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize, loom['loom_sName'], loom['loom_sDescr'])),
    ('init2', partial(QDS.Initialize, p['_sName'], p['_sDescr'])),
    ('log1', partial(QDS.LogUserParameters, p)),
    ('log2', partial(QDS.LogUserParameters, loom)),
    ('build1', partial(prey_buildStimulus, p)),
    ('build2', partial(build_loomingstimulus, loom)),
    ('start', QDS.StartScript),
    ('clear', partial(QDS.Scene_Clear, 8.0, 0)),
    ('iter', partial(loom_iterateStimulus, loom)),
    ('clear1', partial(QDS.Scene_Clear, 8.0, 0)),
    ('iter1', partial(prey_iterateStimulus, p)),
    ('clear2', partial(QDS.Scene_Clear, 8.0, 0)),
    ('stop', QDS.EndScript)]
)

[dispatcher[process]() for process in list(dispatcher.keys())]
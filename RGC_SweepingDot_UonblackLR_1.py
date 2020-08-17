#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import collections
from functools import partial
import QDS
import math 

# Define global stimulus parameters
p = {'_sName'          : "RGC_MovingEllipse",
     '_sDescr'         : "'moving ellipse' in fingerprinting stimulus set",
     "nTrials"         : 5,
     "DirList"         : [0, 180],

     "vel_umSec"       : 400.0, # speed of moving bar in um/sec
     "tMoveDur_s"      : 4.0,    # duration of movement (defines distance
                                 # the bar travels, not its speed)
     "ellipseDx_um"    : 10.0,  # bar dimensions in um width
     "ellipseDy_um"    : 5.0, #height
     "bkgColor"        : (0,0,0),       # background color
     "ellipseColor"    : (255, 255, 255), # bar color
     "durFr_s"         : 1/60.0, # Frame duration
     "nFrPerMarker"    : 0
}

def buildStimulus(p):
    p['durMarker_s']    = p["durFr_s"]*p["nFrPerMarker"]
    p['freq_Hz']        = round(1.0 /p["durFr_s"])
    p['umPerFr']        = float(p["vel_umSec"]) /p['freq_Hz']
    p['moveDist_um']    = p["vel_umSec"] *p["tMoveDur_s"]
    p['nFrToMove']      = float(p['moveDist_um']) /p['umPerFr']
    p['nFrToMove']      = float(p['moveDist_um']) /p['umPerFr']

    # Define stimulus objects
    QDS.DefObj_Ellipse(1, p["ellipseDx_um"], p["ellipseDy_um"])

def MoveEllipseSeq():
  # A function that presents the moving bar in the given number of 
  # directions (= moving bar sequence)
  for rot_deg in p["DirList"]:
    # Calculate rotation angle and starting position of bar
    rot_rad = (rot_deg)/360.0 *2 *math.pi
    x       = math.cos(rot_rad) *( p['moveDist_um'] /2.0)
    y       = math.sin(rot_rad) *(-p['moveDist_um'] /2.0)

    # Move the bar stepwise across the screen (as smooth as permitted
    # by the refresh frequency)
    QDS.Scene_Clear(p['durMarker_s'], 0)
    for iStep in range(int(p['nFrToMove'])):
      QDS.Scene_RenderEx(p["durFr_s"], [1], [(x,y)], [(1.0,1.0)], [rot_deg], 0)
      x -= math.cos(rot_rad) *p['umPerFr']
      y += math.sin(rot_rad) *p['umPerFr']
      
def iterateStimulus(p):
    QDS.SetObjColor(1, [1], [p["ellipseColor"]])
    QDS.SetBkgColor(p["bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(p["nTrials"], MoveEllipseSeq)

# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize,p['_sName'],p['_sDescr'])),
    ('log', partial(QDS.LogUserParameters,p)),
    ('build', partial(buildStimulus,p)),
    ('start', QDS.StartScript),
    ('clear1', partial(QDS.Scene_Clear,1.0, 0)),
    ('iter', partial(iterateStimulus,p)),
    ('clear2', partial(QDS.Scene_Clear,1.0, 0)),
    ('stop', QDS.EndScript)]
)

[dispatcher[process]() for process in list(dispatcher.keys())]
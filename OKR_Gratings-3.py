#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import collections
from functools import partial
import QDS
import math

# Define global stimulus parameters
okr = {'_sName': "Prey_Vibration",
       '_sDescr': "horizontal vibrating 'moving ellipse'",
       "nTrials": 1,

       "DirList": [0, 180],  # controls the directionality in which the dot moves in order
       "vel_umSec": 20.0,  # speed of moving bar in um/sec
       "tMoveDur_s": 10,  # duration of movement (defines distance the bar travels, not its speed)

       "BoxDx_um": 400.0,  # bar dimensions in um width
       "BoxDy_um": 120.0,  # height

       "bkgColor": (0, 0, 0),  # background color
       "ellipseColor": (255, 255, 255),  # bar color
       "durFr_s": 1 / 60.0,  # Frame duration
       "nFrPerMarker": 0,

       "perLen_um": 0.0,
       "perDur_s": 1.0,
       "minRGB": (0, 0, 0, 255),
       "maxRGB": (255, 255, 255, 255)
       }


def buildStimulus(okr):
    okr['durMarker_s'] = okr["durFr_s"] * okr["nFrPerMarker"]
    okr['freq_Hz'] = round(1.0 / okr["durFr_s"])
    okr['umPerFr'] = float(okr["vel_umSec"]) / okr['freq_Hz']
    okr['moveDist_um'] = okr["vel_umSec"] * okr["tMoveDur_s"]
    okr['nFrToMove'] = float(okr['moveDist_um']) / okr['umPerFr']
    # print  ("okr['durMarker_s']:", okr['durMarker_s'],
    #         "okr['freq_Hz']:", okr['freq_Hz'],
    #         "okr['umPerFr']:", okr['umPerFr'],
    #         "okr['moveDist_um']:", okr['moveDist_um'],
    #         "okr['nFrToMove']:", okr['nFrToMove'])
    # Define stimulus objects

    QDS.DefObj_BoxEx(_iobj = 1, _dx=okr["BoxDx_um"], _dy=okr["BoxDy_um"], _enShader = 1)

def MoveEllipseSeq():
    # A function that presents the moving bar in the given number of
    # directions (= moving bar sequence)
    for rot_deg in okr["DirList"]:
        # Calculate rotation angle and starting position of bar
        # x and y determines where the stimulus starts
        # with respect to the center of the screen (0,0) as well as "vel_umSec" & "tMoveDur_s"
        # and "DirList" lists out the angles
        rot_rad = (rot_deg) / 360.0 * 2 * math.pi
        x = math.cos(rot_rad) * (okr['moveDist_um'] / 2.0)
        y = math.sin(rot_rad) * (-okr['moveDist_um'] / 2.0)

        # Move the bar stepwise across the screen (as smooth as permitted
        # by the refresh frequency)
        # QDS.Scene_Clear(okr['durMarker_s'], 0) #Clears the scene for 'durMarker_s' number of seconds beore the start of the stimulus
        for iStep in range(int(okr['nFrToMove'])):
            QDS.Scene_RenderEx(okr["durFr_s"], [1], [(x, y)], [(1.0, 1.0)], [rot_deg], 0)
            x -= math.cos(rot_rad) * okr['umPerFr']
            y += math.sin(rot_rad) * okr['umPerFr']


def iterateStimulus(okr):
    QDS.DefShader(_ishd =2 ,_shType="SQUARE_WAVE_GRATING")
    QDS.SetShaderParams(_ishd=2 , _shParams= [0.0, 1.0, (0, 0, 0, 255), (255, 255, 255, 255)])
    QDS.SetObjShader(_iobjs = [1] , _ishds = [2])
    QDS.SetObjColor(1, [1], [okr["ellipseColor"]])
    QDS.SetBkgColor(okr["bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(okr["nTrials"], MoveEllipseSeq)


# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize, okr['_sName'], okr['_sDescr'])),
    ('log', partial(QDS.LogUserParameters, okr)),
    ('build', partial(buildStimulus, okr)),
    ('start', QDS.StartScript),
    ('clear1', partial(QDS.Scene_Clear, 1.0, 0)),
    ('iter1', partial(iterateStimulus, okr)),
    # ('clear2', partial(QDS.Scene_Clear, 1.0, 0)),
    # ('iter2', partial(iterateStimulus, p)),
    ('clear3', partial(QDS.Scene_Clear, 1.0, 0)),
    ('stop', QDS.EndScript)]
)

[dispatcher[process]() for process in list(dispatcher.keys())]

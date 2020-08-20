#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import collections
from functools import partial
import QDS
import math

# Define global stimulus parameters
okr = {'_okr_sName': "Prey_Vibration",
       '_okr_sDescr': "horizontal vibrating 'moving ellipse'",
       "okr_nTrials": 1,

       "_okrDirList": [90, 270],  # controls the directionality in which the dot moves in order
       "okr_vel_umSec": 50.0,  # speed of moving bar in um/sec
       "okr_tMoveDur_s": 5,  # duration of movement (defines distance the bar travels, not its speed)

       "BoxDx_um": 30,  # height
       "BoxDy_um": 150,  # width

       "okr_bkgColor": (0, 0, 0),  # background color
       "BoxColor": (255, 255, 255),  #
       "durFr_s": 1 / 60.0,  # Frame duration
       "nFrPerMarker": 0,

       "_ShType": "SQUARE_WAVE_GRATING",
       "perLen_um": 8.0,
       "phase_um": 2.0,
       "minRGB": (0, 0, 0, 255),
       "maxRGB": (255, 0, 255, 255)
       }

def buildStimulus(okr):
    okr['durMarker_s'] = okr["durFr_s"] * okr["nFrPerMarker"]
    okr['freq_Hz'] = round(1.0 / okr["durFr_s"])
    okr['umPerFr'] = float(okr["okr_vel_umSec"]) / okr['freq_Hz']
    okr['moveDist_um'] = okr["okr_vel_umSec"] * okr["okr_tMoveDur_s"]
    okr['nFrToMove'] = float(okr['moveDist_um']) / okr['umPerFr']

    QDS.DefObj_BoxEx(_iobj= 1, _dx = okr["BoxDx_um"], _dy = okr["BoxDy_um"], _enShader = 1)
    QDS.DefShader(_ishd=1, _shType=okr["_ShType"])
    QDS.SetShaderParams(_ishd=1, _shParams=[okr["perLen_um"], okr["phase_um"], okr["minRGB"], okr["maxRGB"]])
    QDS.SetObjShader(_iobjs=[1], _ishds=[1])

def OKR_Seq():
    for rot_deg in okr["_okrDirList"]:
        for iStep in range(int(okr['nFrToMove'])):
            QDS.Scene_RenderEx(okr["durFr_s"], [1], [(0, 0)], [(1.0, 1.0)], [rot_deg], 0)

def okr_iterateStimulus(okr):
    QDS.SetObjColor(1, [1], [okr["BoxColor"]])
    QDS.SetBkgColor(okr["okr_bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(okr["okr_nTrials"], OKR_Seq)

# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize, okr['_okr_sName'], okr['_okr_sDescr'])),
    ('log', partial(QDS.LogUserParameters, okr)),
    ('build', partial(buildStimulus, okr)),
    ('start', QDS.StartScript),
    ('clear1', partial(QDS.Scene_Clear, 0.0, 0)),
    ('iter1', partial(okr_iterateStimulus, okr)),
    # ('clear2', partial(QDS.Scene_Clear, 1.0, 0)),
    # ('iter2', partial(okr_iterateStimulus, p)),
    ('clear3', partial(QDS.Scene_Clear, 0.0, 0)),
    ('stop', QDS.EndScript)]
)

[dispatcher[process]() for process in list(dispatcher.keys())]

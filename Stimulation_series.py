#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
import collections
from functools import partial
import QDS
import math
# import sys
# import time
# import os
# import pickle
# from   ctypes import windll
# from   PyQt5 import uic
# from   PyQt5.QtWidgets import QMessageBox, QMainWindow, QLabel, QApplication
# from   PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QWidget
# from   PyQt5.QtGui     import QPalette, QColor, QBrush, QTextCharFormat, QTextCursor
# from   PyQt5.QtCore    import QRect, QSize
# from   multiprocessing import Process
# import QDSpy_stim as stm
# import QDSpy_stim_support as ssp
# import QDSpy_config as cfg
# import QDSpy_GUI_support as gsu
# from   QDSpy_GUI_cam import CamWinClass
# import QDSpy_multiprocessing as mpr
# import QDSpy_stage as stg
# import QDSpy_global as glo
# import QDSpy_core
# import QDSpy_core_support as csp

# Define global stimulus parameters
########## Looming Dot Parameters ##########
loom = {'loom_sName': "Looming Dot",
        'loom_sDescr': "Dot of increasing size",

        "loom_nTrials": 10,

        "initial_dot_um": 1, # dot size
        "max_size": 30, #maxium for max_size * mag_rate is 800
        "mag_rate": 1, # rate at which it magnifies

         "origin_x": 0,
         "origin_y": 0,

         "loom_bkgColor": (0, 0, 0),  # background color
         "DotColor": (255, 0, 255),  # bar color

        "durFr_s": 1 / 60.0,  # Frame duration
        "nFrPerMarker": 0 # afffects the math in durMarker_s
        }
########## Prey like stimulus parameters ##########
p = {'_sName': "Prey_Vibration",
     '_sDescr': "horizontal vibrating 'moving ellipse'",
     "p_nTrials": 4,

     "DirList":[0, 180], #controls the directionality in which the dot moves in order
     "vel_umSec": 500.0,  # speed of moving bar in um/sec
     "tMoveDur_s": 1.25,  # duration of movement (defines distance
     # the bar travels, not its speed)

     "ellipseDx_um": 10.0,  # bar dimensions in um width
     "ellipseDy_um": 7.0,  # height

     "p_bkgColor": (0, 0, 0),  # background color
     "p_ellipseColor": (255, 0, 255),  # bar color

     "durFr_s"         : 1/60.0, # Frame duration
     "nFrPerMarker"    : 0
     }
########## OKR Gratings Parameters ##########
okr = {'_okr_sName': "Prey_Vibration",
       '_okr_sDescr': "horizontal vibrating 'moving ellipse'",
       "okr_nTrials": 1,

       "_okrDirList": [90, 270],  # controls the directionality of the gratings and object
       "okr_vel_umSec": 50.0,  # speed of moving bar in um/sec
       "okr_tMoveDur_s": 5,  # duration of movement (defines distance the bar travels, not its speed)

       "BoxDx_um": 50,  # height
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

def buildStimulus(okr):
    okr['durMarker_s'] = okr["durFr_s"] * okr["nFrPerMarker"]
    okr['freq_Hz'] = round(1.0 / okr["durFr_s"])
    okr['umPerFr'] = float(okr["okr_vel_umSec"]) / okr['freq_Hz']
    okr['moveDist_um'] = okr["okr_vel_umSec"] * okr["okr_tMoveDur_s"]
    okr['nFrToMove'] = float(okr['moveDist_um']) / okr['umPerFr']

    QDS.DefObj_BoxEx(_iobj= 3, _dx = okr["BoxDx_um"], _dy = okr["BoxDy_um"], _enShader = 1)
    QDS.DefShader(_ishd=1, _shType=okr["_ShType"])
    QDS.SetShaderParams(_ishd=1, _shParams=[okr["perLen_um"], okr["phase_um"], okr["minRGB"], okr["maxRGB"]])
    QDS.SetObjShader(_iobjs=[3], _ishds=[1])
#
def LoomingDotSeq():
    # A function that presents the dot and increases its size by increasing the magnification in Scene_RenderEx
    for dot_size in range(loom['max_size']):
        a = dot_size * (loom['mag_rate'])
        b = dot_size * (loom['mag_rate'])
        # print ("(", x, y, ")")
        for iStep in range(1):
            QDS.Scene_RenderEx(loom["durFr_s"], [1], [(loom["origin_x"], loom["origin_y"])], [(a, b)], [0], 0)
    QDS.Scene_Clear(0.5, 0)

def MoveEllipseSeq(): # A function that presents the moving bar in the given number of directions (= moving bar sequence)
    for rot_deg in p["DirList"]:
        rot_rad = (rot_deg) / 360.0 * 2 * math.pi
        x = math.cos(rot_rad) * (p['moveDist_um'] / 2.0)
        y = math.sin(rot_rad) * (-p['moveDist_um'] / 2.0)
        # print ("a:", x, y)
        for iStep in range(int(p['nFrToMove'])):
            QDS.Scene_RenderEx(p["durFr_s"], [2], [(x, y)], [(1.0, 1.0)], [rot_deg], 0)
            x -= math.cos(rot_rad) * p['umPerFr']
            y += math.sin(rot_rad) * p['umPerFr']
            # print ("b:", x, y)

def OKR_Seq():
    for rot_deg in okr["_okrDirList"]:
        for iStep in range(int(okr['nFrToMove'])):
            QDS.Scene_RenderEx(okr["durFr_s"], [3], [(0, 0)], [(1.0, 1.0)], [rot_deg], 0)

def loom_iterateStimulus(loom):
    QDS.SetObjColor([1],[1,2,3], [loom["DotColor"], p["p_ellipseColor"], okr["BoxColor"]])
    QDS.SetBkgColor(loom["loom_bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(loom["loom_nTrials"], LoomingDotSeq)

def prey_iterateStimulus(p):
    QDS.SetObjColor([1],[1,2,3], [loom["DotColor"], p["p_ellipseColor"], okr["BoxColor"]])
    QDS.SetBkgColor(p["p_bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(p["p_nTrials"], MoveEllipseSeq)

def okr_iterateStimulus(okr):
    QDS.SetObjColor([1], [1,2,3], [loom["DotColor"], p["p_ellipseColor"], okr["BoxColor"]])
    QDS.SetBkgColor(okr["okr_bkgColor"])
    QDS.Scene_Clear(0, 0)
    QDS.Loop(okr["okr_nTrials"], OKR_Seq)
# --------------------------------------------------------------------------
dispatcher = collections.OrderedDict([
    ('init', partial(QDS.Initialize, p['_sName'], p['_sDescr'])),
    ('init1', partial(QDS.Initialize, loom['loom_sName'], loom['loom_sDescr'])),
    ('init2', partial(QDS.Initialize, okr['_okr_sName'], okr['_okr_sDescr'])),
    ('log', partial(QDS.LogUserParameters, p)),
    ('log1', partial(QDS.LogUserParameters, loom)),
    ('log2', partial(QDS.LogUserParameters, okr)),
    ('build', partial(prey_buildStimulus, p)),
    ('build1', partial(build_loomingstimulus, loom)),
    ('build2', partial(buildStimulus, okr)),
    ('start', QDS.StartScript),
    ('clear', partial(QDS.Scene_Clear, 10.0, 0)),
    ('iter', partial(okr_iterateStimulus, okr)),
    ('clear1', partial(QDS.Scene_Clear, 10.0, 0)),
    ('iter1', partial(loom_iterateStimulus, loom)),
    ('clear2', partial(QDS.Scene_Clear, 10.0, 0)),
    ('iter2', partial(prey_iterateStimulus, p)),
    ('clear3', partial(QDS.Scene_Clear, 10.0, 0)),
    ('stop', QDS.EndScript)]
)

[dispatcher[process]() for process in list(dispatcher.keys())]
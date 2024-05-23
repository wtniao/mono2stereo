import numpy as np
import numpy.ctypeslib as npct
import ctypes
from ctypes import *

array_3d_uint8 = npct.ndpointer(dtype = np.uint8, ndim = 3, flags = 'CONTIGUOUS')

array_2d_float32 = npct.ndpointer(dtype = np.float32, ndim = 2, flags = 'CONTIGUOUS')

libmodule = npct.load_library('libStereFlow.so','.')

libmodule.genStereFlow.restype = None
libmodule.genStereFlow.argtypes = [array_2d_float32, array_2d_float32, array_2d_float32, c_int, c_int]

libmodule.warpFlow.restype = None
libmodule.warpFlow.argtypes = [array_3d_uint8, array_3d_uint8, array_2d_float32, c_int, c_int]

def genStereFlow(depth):
    h,w = depth.shape
    leftFlow = np.zeros_like(depth, dtype=np.float32)
    rightFlow = np.zeros_like(depth, dtype=np.float32)
    libmodule.genStereFlow(leftFlow, rightFlow, depth, h, w)
    return leftFlow,rightFlow

def warpFlow(img, flow):
    h,w = flow.shape
    out = np.zeros_like(img, dtype=np.uint8)
    libmodule.warpFlow(out, img, flow, h, w)
    return out
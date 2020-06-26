import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import glob as glob

import pandas as pd
import json
from scipy.interpolate import interp1d
from scipy import interp
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from skimage import exposure,img_as_ubyte
from moviepy.editor import VideoClip
from moviepy.editor import ImageSequenceClip
from skimage import color
import datetime
import time
import argparse
import os

fileNames = glob.glob('./data/out*.dat')
params = np.loadtxt('param.txt')
fN = pd.DataFrame(fileNames)
fN['time'] = fN[0].str.extract(r'(\d*)\.dat').astype('int')
fN.sort_values(by=['time'],inplace=True)



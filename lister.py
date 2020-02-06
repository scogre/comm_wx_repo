import pygrib
import matplotlib
import netCDF4
from netCDF4 import Dataset
import datetime
import os,sys
import numpy as np

from datetime import datetime

grbfile=pygrib.open('gdas.t06z.pgrb2.1p00.f009')

for line in grbfile:
   print('line=',line)



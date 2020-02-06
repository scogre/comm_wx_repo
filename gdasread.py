import pygrib
import matplotlib
import netCDF4
from netCDF4 import Dataset
import datetime
import os,sys
import numpy as np

from datetime import datetime

#grbfile=pygrib.open('gdas.t06z.pgrb2.1p00.f009')
grbfile=pygrib.open('gdas.t06z.sfluxgrbf000.grib2')
#grbfile=pygrib.open('gec00.t06z.pgrb2f00')
#grbfile=pygrib.open('gfs_4_20181215_0000_000.grb2')
###Orography



for line in grbfile:
   print('line=',line)

Ustar = grbfile.select(name='Frictional velocity')[:]
Rough= grbfile.select(name='Surface roughness')[:]
Orography = grbfile.select(name='Orography')[:]
lats,lons=Ustar[0].latlons()
nlat=lats.shape[0]
nlon=lats.shape[1]
print('nlat,nlon=',nlat,nlon)
print('lats=',lats)

############################
grbfile2=pygrib.open('gdas.t12z.sfluxgrbf000.grib2')
Ustar2 = grbfile2.select(name='Frictional velocity')[:]
Rough2= grbfile2.select(name='Surface roughness')[:]
Orography2 = grbfile2.select(name='Orography')[:]
lats2,lons2=Ustar2[0].latlons()
nlat2=lats2.shape[0]
nlon2=lats2.shape[1]
print('nlat2,nlon2=',nlat2,nlon2)
print('lats2=',lats2)

############################
print('len rough=',len(Rough))
print('len rough2=',len(Rough2))

rough  = Rough[0].values
rough2 = Rough2[0].values
rough_rat=rough/rough2
print('rough_rat=',rough_rat)
print('maxroughrat=',np.max(rough_rat))
print('maxrough=',np.max(rough))
print('maxrough2=',np.max(rough2))

ustar=Ustar[0].values
ustar2=Ustar2[0].values
ustar_rat=ustar/ustar2
print('ustar_rat=',ustar_rat)
print('maxustarrat=',np.max(ustar_rat))
print('maxustar=',np.max(ustar))
print('maxustar2=',np.max(ustar2))


#print('lenoro=',len(Orography))
#orog  = Orography[0].values
#print('maxoro=',np.max(orog))
#print('minoro=',np.min(orog))
#print('meanoro=',np.mean(orog))
#
#print('lenoro=',len(Orography2))
#orog2  = Orography2[0].values
#print('maxoro=',np.max(orog2))
#
#print('orog=',orog)







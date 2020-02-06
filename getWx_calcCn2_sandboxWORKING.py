import pygrib
import matplotlib
import netCDF4
from netCDF4 import Dataset
import datetime
import os,sys
import numpy as np


R=287
g=9.8
p0=1000
cp=1004
nan=float('nan')



#####################
YEARRUN=2019
MORUN=12
DAYRUN_start=18
DAYRUN_end=20
HOURincrmnt=6
#/pub/data/nccf/com/gfs/prod/gfs.20191207/00
#https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20191207/00/gfs.t00z.pgrb2.1p00.f000


yr_str=str(YEARRUN)

if MORUN<10:
   mo_str='0'+str(MORUN) 
else:
   mo_str=str(MORUN)

for d in range(DAYRUN_start,DAYRUN_end+1):
   if d<10:
      da_str='0'+str(d)
   else:
      da_str=str(d)
   
   for h in range(0,24,HOURincrmnt):
      if h<10:
         hr_str='0'+str(h)
      else:
         hr_str=str(h)
      
      print('yr='+yr_str+',mo='+mo_str+'da='+da_str+'hr='+hr_str)

      yrmo_str = yr_str + mo_str
      yrmoda_str = yr_str + mo_str + da_str
      yrmodahr_str = yr_str + mo_str + da_str + hr_str

      GFSpath='https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.'+yr_str+mo_str+da_str+'/'+hr_str+'/'
      ####### 1degree
      file='gfs.t'+hr_str+'z.pgrb2.1p00.f000'
      newfile=yr_str+mo_str+da_str+file
            
      os.system('rm '+file)
      os.system('rm '+newfile)
      xx=os.system('wget '+GFSpath+file)
      os.system('mv '+file+' '+newfile)

      grbfile=pygrib.open(newfile)

      TCC = grbfile.select(name='Total Cloud Cover',typeOfLevel='isobaricInhPa')[:]
      Ucow = grbfile.select(name='U component of wind',typeOfLevel='isobaricInhPa')[:]
      Vcow = grbfile.select(name='V component of wind',typeOfLevel='isobaricInhPa')[:]
      Txyz = grbfile.select(name='Temperature',typeOfLevel='isobaricInhPa')[:]

      lats,lons=TCC[0].latlons()
      nlat=lats.shape[0]
      nlon=lats.shape[1]

      plevelUcow=[]
      nlevU=len(Ucow)
      print('nlevU=',nlevU)
      for nz in range(nlevU):
         plevelUcow.append(Ucow[nz].level)
      print('plevU=',plevelUcow)

      plevelVcow=[]
      nlevV=len(Vcow)
      print('nlevV=',nlevV)
      for nz in range(nlevV):
         plevelVcow.append(Vcow[nz].level)
      print('plevVcow=',plevelVcow)

      plevelTxyz=[]
      nlevT=len(Txyz)
      print('nlevT=',nlevT)
      for nz in range(nlevT):
         plevelTxyz.append(Txyz[nz].level)
      print('plevT=',plevelTxyz)

      plevUset=set(plevelUcow)
      plevVset=set(plevelVcow)
      plevTset=set(plevelTxyz)
      plevsets=[plevUset, plevVset, plevTset]
      plevcommon = list(set.intersection(*plevsets))
      plevcommon.sort(reverse = True) #reverse to match matlab order
      print('plevcommon=',plevcommon)
      print('lencommon=',len(plevcommon))
      nlev_all=len(plevcommon)

      uindx=nan*np.ones(len(plevcommon))
      vindx=nan*np.ones(len(plevcommon))
      Tindx=nan*np.ones(len(plevcommon))
      for nn in range(len(plevcommon)):
         uindx[nn]=plevelUcow.index(plevcommon[nn])
         vindx[nn]=plevelVcow.index(plevcommon[nn])
         Tindx[nn]=plevelTxyz.index(plevcommon[nn])
      print('uindcs=',uindx)
      print('vindcs=',vindx)
      print('Tindcs=',Tindx)

      Ucow_data=np.zeros([nlev_all,nlat,nlon])
      for nz in range(nlev_all):
         indx=int(uindx[nz])
         print('Uindx=',indx)
         Ucow_data[nz,:,:]=Ucow[indx].values

      Vcow_data=np.zeros([nlev_all,nlat,nlon])
      for nz in range(nlev_all):
         indx=int(vindx[nz])
         print('Vindx=',indx)
         Vcow_data[nz,:,:]=Vcow[indx].values

      Txyz_data=np.zeros([nlev_all,nlat,nlon])
      for nz in range(nlev_all):
         indx=int(Tindx[nz])
         print('Tindx=',indx)
         Txyz_data[nz,:,:]=Txyz[indx].values

sys.exit()




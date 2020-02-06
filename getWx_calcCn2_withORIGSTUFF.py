import pygrib
import matplotlib
import netCDF4
import datetime
import os,sys
import numpy as np


lat_target = 34.646
lon_target = -86.706

lat_round=np.round(lat_target)
lon_round=np.round(lon_target)
lat_floor=np.floor(lat_target)
lon_floor=np.floor(lon_target)
lat_ceil=np.ceil(lat_target)
lon_ceil=np.ceil(lon_target)

lat_half_floor=np.floor(2*lat_target)/2
lon_half_floor=np.floor(2*lon_target)/2
lat_half_ceil=np.ceil(2*lat_target)/2
lon_half_ceil=np.ceil(2*lon_target)/2



#####################
#YEARRUN=2015
#MORUN=5
#DAYRUN_start=4
##DAYRUN_end=8
#DAYRUN_end=5
#HOURincrmnt=6
#####################
YEARRUN=2019
MORUN=12
DAYRUN_start=6
DAYRUN_end=8
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



#      REANpath='https://nomads.ncdc.noaa.gov/data/gfsanl/'+yr_str+mo_str+'/'+yr_str+mo_str+da_str+'/'
      REANpath='https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.'+yr_str+mo_str+da_str+'/'+hr_str+'/'
      ####### 1degree
#      file='gfsanl_3_'+yr_str+mo_str+da_str+'_'+hr_str+'00_000.grb'
      file='/gfs.t'+hr_str+'z.pgrb2.1p00.f000'
      try:
         xx=os.system('wget '+REANpath+file)
         print('got it')
         gr=pygrib.open(file)
         #CW=gr.select(name='Cloud water',typeOfLevel='entireAtmosphere')
         #CW=gr(name='Cloud water')
         #lats,lons=CW.latlons()
#         CLWMR=[grb for grb in gr if (str.find(str(grb),'153:153')>=0)]
#         lats,lons=CLWMR[0].latlons()
#         nlev=len(CLWMR)

         print('open complete')
         for grb in gr:
            grb
         print('list complete')
         TCC = gr.select(name='Total Cloud Cover')[0]
         print('TCC found')
         lats,lons=TCC.latlons()
         print('latalons found')
         nlev=len(TCC)
         print('nlev=',nlev)
         print('latshape=',lats.shape)


         level=[]
         for nz in range(nlev):
            #level.append(CLWMR[nz].level)
            level.append(TCC[nz].level)


#         for g in gr:
#            #print('g=',g)
#            #print(g.name)
#            temp_vals=g.values
#            tempshape=temp_vals.shape
#            print('name,tempshape=',g.name,tempshape)
#         gr.close()
      except:
         print('missing file:'+file)
      

#      ######0.5 degree
#      file='gfsanl_4_'+yr_str+mo_str+da_str+'_'+hr_str+'00_000.grb2'
#      try:
#         xx=os.system('wget '+REANpath+file)
#         print('got it')
#         gr=pygrib.open(file)
#         for g in gr:
#            #print('g=',g)
#            print(g.name)
#            temp_vals=g.values
#            tempshape=temp_vals.shape
#            #print('tempshape=',tempshape)
#         gr.close()
#      except:
#         print('missing file:'+file)
#
#      print('advancing to next hr')
#      print('advancing to next hr')
#      print('advancing to next hr')
#      print('advancing to next hr')


sys.exit()


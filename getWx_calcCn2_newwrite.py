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
YEARRUN=2019
MORUN=12
DAYRUN_start=14
DAYRUN_end=17
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
#      for grbline in grbfile:
#         print('grbline=',grbline)

      TCC = grbfile.select(name='Total Cloud Cover',typeOfLevel='isobaricInhPa')[:]
      Ucow = grbfile.select(name='U component of wind',typeOfLevel='isobaricInhPa')[:]
      Vcow = grbfile.select(name='V component of wind',typeOfLevel='isobaricInhPa')[:]
      Txyz = grbfile.select(name='Temperature',typeOfLevel='isobaricInhPa')[:]

      lats,lons=TCC[0].latlons()
      nlat=lats.shape[0]
      nlon=lats.shape[1]

      nlev_all=21### the first 21 levels of variables in GFS are the same 1000mb-100mb
      print('nlev_all=',nlev_all)


      plevelTCC=[]
      nlevTCC=len(TCC)
      print('nlevTCC=',nlevTCC)
#      TCC_data=np.zeros([nlevTCC,nlat,nlon])
      TCC_data=np.zeros([nlev_all,nlat,nlon])
      pressure=nan*np.ones(nlev_all)
#      for nz in range(nlevTCC):
      for nz in range(nlev_all):
         plevelTCC.append(TCC[nz].level)
         TCC_data[nz,:,:]=TCC[nz].values
         pressure[nz]=TCC[nz].level
         #print('levelTCC=',TCC[nz].level)
      print('plevs=',plevelTCC)

      plevelUcow=[]
      nlevU=len(Ucow)
      print('nlevU=',nlevU)
#      Ucow_data=np.zeros([nlevU,nlat,nlon])
      Ucow_data=np.zeros([nlev_all,nlat,nlon])
#      for nz in range(nlevU):
      for nz in range(nlev_all):
         plevelUcow.append(Ucow[nz].level)
         Ucow_data[nz,:,:]=Ucow[nz].values
         #print('levelU=',Ucow[nz].level)
      print('plevU=',plevelUcow)

      plevelVcow=[]
      nlevV=len(Vcow)
      print('nlevV=',nlevV)
#      Vcow_data=np.zeros([nlevV,nlat,nlon])
      Vcow_data=np.zeros([nlev_all,nlat,nlon])
#      for nz in range(nlevV):
      for nz in range(nlev_all):
         plevelVcow.append(Vcow[nz].level)
         Vcow_data[nz,:,:]=Vcow[nz].values
#         print('levelV=',Vcow[nz].level)
      print('plevVcow=',plevelVcow)

      plevelTxyz=[]
      nlevT=len(Txyz)
      print('nlevT=',nlevT)
#      Txyz_data=np.zeros([nlevT,nlat,nlon])
      Txyz_data=np.zeros([nlev_all,nlat,nlon])
#      for nz in range(nlevT):
      for nz in range(nlev_all):
         plevelTxyz.append(Txyz[nz].level)
         Txyz_data[nz,:,:]=Txyz[nz].values
#         print('levelT=',Txyz[nz].level)
      print('plevT=',plevelTxyz)





      ##########################################################
      ##########################################################
      ##########################################################
      ##########################################################
      ##########################################################
      ##########################################################
      T=Txyz_data
      Txy=np.mean(T,0)
      Tavgprofile=np.mean(np.mean(T,2),1)
      print('Tprofile=',Tavgprofile)
      print('Tshape=',T.shape)
      T_equator=np.squeeze(T[:,90,:])
      #print('T_equator=',T[:,90,:])
      print('T_equator_profile=',np.mean(T_equator,1))
      Hxy=R*Txy/g
#      print('Hxy.shape=',Hxy.shape)
      ##########################################################
#      pressure=plevelTCC
#      print('phape',pressure.shape)
      z=nan*np.ones([nlev_all,nlat,nlon])
#      print('zshape=',z.shape)
      z_mid=nan*np.ones([nlev_all-1,nlat,nlon])
#      print('zmidshape=',z_mid.shape)
      z_mid_2=nan*np.ones([nlev_all-1,nlat,nlon])
      p_mid=nan*np.ones(nlev_all-1)
      Hstack=nan*np.ones([nlev_all-1,nlat,nlon])
      for h in range(nlev_all):
         z[h,:,:]=Hxy*np.log(p0/pressure[h])
         if h>0:
            p_mid[h-1]=0.5*(pressure[h]+pressure[h-1])
            z_mid[h-1,:,:]=Hxy*np.log(p0/p_mid[h-1])
            z_mid_2[h-1,:,:]=0.5*(z[h,:,:]+z[h-1,:,:])
            T_mid=0.5*(T[h,:,:]+T[h-1,:,:])
            Hstack[h-1,:,:]=Hxy
#      print('Hstackshape=',Hstack.shape)

      print('pmidshape=',p_mid.shape)
      print('pmid=',p_mid)
      p2d=np.repeat(p_mid[:,np.newaxis],nlat,1)
      p_mid3d=np.repeat(p2d[:,:,np.newaxis],nlon,2)

      vx=Ucow_data
      vy=Vcow_data
      nlev=nlev_all
      dvx=vx[1:nlev_all,:,:]-vx[0:nlev_all-1,:,:]
      dvy=vy[1:nlev_all,:,:]-vy[0:nlev_all-1,:,:]
      dz=z[1:nlev_all,:,:]-z[0:nlev_all-1,:,:]
      dT=T[1:nlev_all,:,:]-T[0:nlev_all-1,:,:]

      S1=dvx/dz
      print('S1shape=',S1.shape)
      S=np.sqrt((dvx/dz)**2 + (dvy/dz)**2)
      print('Sshape=',S.shape)

      Lo_4_3rds=0.1**(4/3)*10**(1.64+42*S)
      dTHETAdz=(dT/dz + R*T_mid/(cp*Hstack))*np.exp(z_mid*R/(cp*Hstack))
      CHI=dTHETAdz
      Ct2 = 2.8 * Lo_4_3rds * CHI**2;
      Cn2 = ((80e-6 * p_mid3d)/(T_mid**2))**2 * Ct2;

      print('cn2shape=',Cn2.shape)
      #print('cn2=',Cn2)

      ##########################################################
      nlev_mid=nlev_all-1
      ##########################################################
      print('making netcdf file for '+yrmodahr_str)
      print('making netcdf file for number=',yrmodahr_str)
      Cn2_filename = 'cn2_'+yrmodahr_str+'.nc'
   
      Cn2_data_nc = Dataset(Cn2_filename,'w',format='NETCDF4')
      Cn2_data_nc.createDimension('nlat',nlat)
      Cn2_data_nc.createDimension('nlon',nlon)
      Cn2_data_nc.createDimension('nlev',nlev_mid)
      Cn2_data_nc.createDimension('ntime',1)
      ncDate=Cn2_data_nc.createVariable('Date',np.int,('ntime',),zlib=False)
      nclats=Cn2_data_nc.createVariable('lats',np.float32,('nlat','nlon',),zlib=False)
      nclons=Cn2_data_nc.createVariable('lons',np.float32,('nlat','nlon',),zlib=False)
      nclevs=Cn2_data_nc.createVariable('levs',np.float32,('nlev',),zlib=False)
      ncCn2=Cn2_data_nc.createVariable('Cn2',np.float32,('nlev','nlat','nlon',),zlib=False)

      print('NOW WRITING')

      ncDate[:]=int(yrmodahr_str)
      nclats[:]=lats
      nclons[:]=lons
      nclevs[:]=p_mid
      ncCn2[:]=Cn2 
      Cn2_data_nc.close()

      ##########################################################
      ##########################################################

sys.exit()


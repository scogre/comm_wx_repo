import pygrib
import matplotlib
import netCDF4
from netCDF4 import Dataset
import datetime
import os,sys
import numpy as np


####################
R=287
g=9.8
p0=1000
cp=1004
nan=float('nan')
####################


from datetime import datetime
now = datetime.utcnow()
print("now =", now)
currenttime_string = now.strftime("%m/%d/%Y %H:%M:%S")
currmo=currenttime_string[0:2]
currda=currenttime_string[3:5]
curryr=currenttime_string[6:10]
currhr=currenttime_string[11:13]
currmin=currenttime_string[14:16]
currsec=currenttime_string[17:19]

FCST_IH=6 ## IH=Interval Hour
last_IH= int(np.floor((int(currhr)-4)/FCST_IH) * FCST_IH) #subtracting 4 hours... time to post GFS forecast
if last_IH<10:
   last_IH_str='0'+str(last_IH)
else:
   last_IH_str=str(last_IH)


mo_str=currmo
da_str=currda
hr_str=last_IH_str
yr_str=curryr

yrmo_str = yr_str + mo_str
yrmoda_str = yr_str + mo_str + da_str
yrmodahr_str = yr_str + mo_str + da_str + hr_str

#####################
WXpath='https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.'+yr_str+mo_str+da_str+'/'+hr_str+'/'
file='gfs.t'+hr_str+'z.pgrb2.1p00.f000'
starfile='gfs.t'+hr_str+'z.pgrb2.1p00.f*'
newfile=yrmodahr_str+file

os.system('rm '+file)
os.system('rm '+newfile)
xx=os.system('wget '+WXpath+file)
os.system('mv '+file+' '+newfile)

grbfile=pygrib.open(newfile)

#for line in grbfile:
#   print('line=',line)
Ucow = grbfile.select(name='U component of wind',typeOfLevel='isobaricInhPa')[:]
Vcow = grbfile.select(name='V component of wind',typeOfLevel='isobaricInhPa')[:]
Txyz = grbfile.select(name='Temperature',typeOfLevel='isobaricInhPa')[:]

lats,lons=Ucow[0].latlons()
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
   Ucow_data[nz,:,:]=Ucow[indx].values

Vcow_data=np.zeros([nlev_all,nlat,nlon])
for nz in range(nlev_all):
   indx=int(vindx[nz])
   Vcow_data[nz,:,:]=Vcow[indx].values

Txyz_data=np.zeros([nlev_all,nlat,nlon])
for nz in range(nlev_all):
   indx=int(Tindx[nz])
   Txyz_data[nz,:,:]=Txyz[indx].values

##########################################################
lats=np.flip(lats,0)
Ucow_data=np.flip(Ucow_data,1)
Vcow_data=np.flip(Vcow_data,1)
Txyz_data=np.flip(Txyz_data,1)
##########################################################
##########################################################
##########################################################
pressure=plevcommon
T=Txyz_data
Txy=np.mean(T,0)
Tavgprofile=np.mean(np.mean(T,2),1)
print('Tprofile=',Tavgprofile)
print('Tshape=',T.shape)
T_equator=np.squeeze(T[:,90,:])
#print('T_equator=',T[:,90,:])
print('T_equator_profile=',np.mean(T_equator,1))
Hxy=R*Txy/g
print('Hxy.shape=',Hxy.shape)
##########################################################
z=nan*np.ones([nlev_all,nlat,nlon])
T_mid=nan*np.ones([nlev_all-1,nlat,nlon])
z_mid=nan*np.ones([nlev_all-1,nlat,nlon])
z_mid_2=nan*np.ones([nlev_all-1,nlat,nlon])
p_mid=nan*np.ones(nlev_all-1)
Hstack=nan*np.ones([nlev_all-1,nlat,nlon])
for h in range(nlev_all):
   z[h,:,:]=Hxy*np.log(p0/pressure[h])
   if h>0:
      p_mid[h-1]=0.5*(pressure[h]+pressure[h-1])
      z_mid[h-1,:,:]=Hxy*np.log(p0/p_mid[h-1])
      z_mid_2[h-1,:,:]=0.5*(z[h,:,:]+z[h-1,:,:])
      T_mid[h-1,:,:]=0.5*(T[h,:,:]+T[h-1,:,:])
      Hstack[h-1,:,:]=Hxy

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
nclevs=Cn2_data_nc.createVariable('p_mid',np.float32,('nlev',),zlib=False)
ncCn2=Cn2_data_nc.createVariable('Cn2',np.float32,('nlev','nlat','nlon',),zlib=False)


ncHxy=Cn2_data_nc.createVariable('Hxy',np.float32,('nlat','nlon',),zlib=False)
ncTxy=Cn2_data_nc.createVariable('Txy',np.float32,('nlat','nlon',),zlib=False)
ncLo_4_3rds=Cn2_data_nc.createVariable('Lo_4_3rds',np.float32,('nlev','nlat','nlon',),zlib=False)
ncS=Cn2_data_nc.createVariable('S',np.float32,('nlev','nlat','nlon',),zlib=False)
ncT=Cn2_data_nc.createVariable('T_mid',np.float32,('nlev','nlat','nlon',),zlib=False)
ncZ=Cn2_data_nc.createVariable('z_mid',np.float32,('nlev','nlat','nlon',),zlib=False)
ncZ2=Cn2_data_nc.createVariable('z_mid_2',np.float32,('nlev','nlat','nlon',),zlib=False)
ncdTHETAdz=Cn2_data_nc.createVariable('dTHETAdz',np.float32,('nlev','nlat','nlon',),zlib=False)
ncCt2=Cn2_data_nc.createVariable('Ct2',np.float32,('nlev','nlat','nlon',),zlib=False)
ncHstack=Cn2_data_nc.createVariable('Hstack',np.float32,('nlev','nlat','nlon',),zlib=False)
ncdT=Cn2_data_nc.createVariable('dT',np.float32,('nlev','nlat','nlon',),zlib=False)
ncdz=Cn2_data_nc.createVariable('dz',np.float32,('nlev','nlat','nlon',),zlib=False)

print('NOW WRITING')
ncDate[:]=int(yrmodahr_str)
nclats[:]=lats
nclons[:]=lons
nclevs[:]=p_mid
ncCn2[:]=Cn2

ncHxy[:]=Hxy
ncTxy[:]=Txy
ncLo_4_3rds[:]=Lo_4_3rds
ncS[:]=S
ncT[:]=T_mid
ncZ[:]=z_mid
ncZ2[:]=z_mid_2
ncdTHETAdz[:]=dTHETAdz
ncCt2[:]=Ct2
ncHstack[:]=Hstack
ncdT[:]=dT
ncdz[:]=dz

Cn2_data_nc.close()

##########################################################
##########################################################

sys.exit()




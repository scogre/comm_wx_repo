
clear
close all

setup_nctoolbox

%Tpath='C:\Users\Scott_Gregory\Documents\GFS_GEFS_sample_WEATHER_DATA\gep01.t00z.pgrb2af06'
Tpath='/Users/scottgregory/Documents/Projects/Comm_Wx/Surface_Layer_Turbulence_Model/BLS_Data_May_4to8/gfsanl_3_20150504_0000_000.grb'



refcst=ncgeodataset(Tpath);
listvarb=refcst.variables;


varbcount=0;
for m=1:length(listvarb);
    varb=char(listvarb(m));
    dum=refcst{varb};
    if strfind(varb,'-')
        varb(strfind(varb,'-'))='_';
        listvarb(m)=cellstr(varb);
    end
    try
        eval([  varb 'dum=dum.data;']);
        eval([  varb '=' varb 'dum.data(varb);']);
        eval([ 'clear ' varb 'dum']);
        varbcount=varbcount+1;
        datavarb(varbcount)=cellstr(varb);
    catch
        sprintf('%s %s','unable to process',varb)
    end
    clear varb
    clear dum
    listvarb(m);
    %pause
end
varbcount;
length(listvarb);


nlat=length(lat);
nlon=length(lon);
lats=makemat(lat,nlat,nlon);
lons=makemat(lon,nlat,nlon);

tindx=1;
fhindx=1;

RH=squeeze(Relative_humidity);
size(RH);


for plev_indx=1:length(isobaric);
    figure(plev_indx)
    Tsamp=squeeze(RH(plev_indx,:,:));
    contourf(lons,lats,Tsamp,50, 'LineColor', 'none')
    %title('Temperature fhr=' num2str(fhour(fhindx)) ' ,plev=' num2str(pressure(plev_indx)) 'mb')
    eval(['title(''Relative humidity; plev=' num2str(isobaric(plev_indx)) 'mb'')'])
    colormap(jet)
    addcoast2;
    colorbar
    caxis([0 100])
    %pause
end




SCALE=1 %scaling the maximum at any level
e_scale=5

%low1000-700
lowindx=find(isobaric>=700);
lowlevs=isobaric(lowindx);
RHl_sum=squeeze(sum(RH(lowindx,:,:),1));
RHl_max= SCALE * max(max(RHl_sum));
RHL=RHl_sum/RHl_max;
RHL(RHL>1.0)=1.0;
%RHL=1-exp(-RHL*e_scale);
figure(100)
contourf(lons,lats,RHL,50, 'LineColor', 'none')
title('low clouds')
colormap(jet)
addcoast2
colorbar


%mid700-400
midindx=find(isobaric<700 & isobaric>=400);
midlevs=isobaric(midindx);
RHm_sum=squeeze(sum(RH(midindx,:,:),1));
RHm_max= SCALE * max(max(RHm_sum));
RHM=RHm_sum/RHm_max;
RHM(RHM>1.0)=1.0;
%RHM=1-exp(-RHM*e_scale);
figure(200)
contourf(lons,lats,RHM,50, 'LineColor', 'none')
title('mid clouds')
colormap(jet)
addcoast2
colorbar

%high400-0
hiindx=find(isobaric<400);
highlevs=isobaric(hiindx);
RHh_sum=squeeze(sum(RH(hiindx,:,:),1));
RHh_max= SCALE * max(max(RHh_sum));
RHH=RHh_sum/RHh_max;
RHH(RHH>1.0)=1.0;
%RHH=1-exp(-RHH*e_scale);
figure(300)
contourf(lons,lats,RHH,50, 'LineColor', 'none')
title('High clouds')
colormap(jet)
addcoast2
colorbar



%figure(3)
%Tsamp=squeeze(Total_cloud_cover)
%contourf(lons,lats,Tsamp,50, 'LineColor', 'none')
%title('cloudcover' )
%colormap(jet)
%addcoast2
%colorbar

cw=squeeze(Cloud_water);
figure(5)
for plev_indx=1:length(isobaric2);
    maxcw(plev_indx)=max(max(cw(plev_indx, :, :)));
    Tsamp=squeeze(cw(plev_indx,:,:));
    Tsamp=Tsamp/maxcw(plev_indx);
    contourf(lons,lats,Tsamp,50, 'LineColor', 'none')
    %title('Temperature fhr=' num2str(fhour(fhindx)) ' ,plev=' num2str(pressure(plev_indx)) 'mb')
    eval(['title(''Cloud water; ' num2str(isobaric2(plev_indx)) 'mb'')'])
    colormap(jet)
    addcoast2;
    colorbar
    %caxis([0 100])
    pause
end




SCALE=0.75 %scaling the maximum at any level
e_scale=5

%low1000-700
lowindx=find(isobaric2>=700);
lowlevs=isobaric2(lowindx);
cwl_sum=squeeze(sum(cw(lowindx,:,:),1));
cwl_max= SCALE * max(max(cwl_sum));
CWL=cwl_sum/cwl_max;
CWL(CWL>1.0)=1.0;
%CWL=1-exp(-CWL*e_scale);
figure(100)
contourf(lons,lats,CWL,50, 'LineColor', 'none')
title('low clouds')
colormap(jet)
addcoast2
colorbar


%mid700-400
midindx=find(isobaric2<700 & isobaric2>=400);
midlevs=isobaric2(midindx);
cwm_sum=squeeze(sum(cw(midindx,:,:),1));
cwm_max= SCALE * max(max(cwm_sum));
CWM=cwm_sum/cwm_max;
CWM(CWM>1.0)=1.0;
%CWM=1-exp(-CWM*e_scale);
figure(200)
contourf(lons,lats,CWM,50, 'LineColor', 'none')
title('mid clouds')
colormap(jet)
addcoast2
colorbar

%high400-0
hiindx=find(isobaric2<400);
highlevs=isobaric2(hiindx);
cwh_sum=squeeze(sum(cw(hiindx,:,:),1));
cwh_max= SCALE * max(max(cwh_sum));
CWH=cwh_sum/cwh_max;
CWH(CWH>1.0)=1.0;
%CWH=1-exp(-CWH*e_scale);
figure(300)
contourf(lons,lats,CWH,50, 'LineColor', 'none')
title('High clouds')
colormap(jet)
addcoast2
colorbar


dx=0.001;
x=dx:dx:1;
y=x;
yy=1-exp(-x*5);
figure(500)

plot(x,y,'--',x,yy)








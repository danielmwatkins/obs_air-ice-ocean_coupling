%
%read Polarstern soundings & plot
%
clear all
%dir_PS_sndgdata='C:\Users\obper\Documents\MOSAiC\Data\radiosondes';
dir_PS_sndgdata='D:\MOSAiC\Data\radiosondes';
%dir_wxdata='C:\Users\obper\Documents\MOSAiC\Data\Polarstern_metdata\';
dir_wxdata='D:\MOSAiC\Data\Polarstern_metdata\';
moddystr=[1 32 60 91 121 152 182 213 244 274 305 335];
moddystrl=[1 32 61 92 122 153 183 214 245 275 306 336];
monam=['Jan' 'Feb' 'Mar' 'Apr' 'May' 'Jun' 'Jul' 'Aug' 'Sep' 'Oct' 'Nov' 'Dec'];
grav=9.81;
event_time=244+25-1+7/24+7/1440; %photo at time of entering ice 2019

if_plot=1; %select plt style: 0-no plots, 1-single plots, 2-two elongated plots per page, 4-four-panel plots
%plot_top=2000; %height of plot top
plot_top=4000; %height of plot top
%plot_top=12000; %height of plot top
np=50;%starting plot number
np0=np;
isotachs_on_T=1; %put isotachs on T TH section? (1=y);

%select plots
pltt=1;pltthav=1;pltthe=1;pltrhi=1;pltrhw=1;pltws=1;pltbrb=1;pltwd=0;
pltnsq=0;pltri=0;pltqv=1;

%define plotting time
%str_dat=input('start date_hr (e.g., 19092506)')
%str_dat='19101200';str_date=str2num(str_dat);
%end_dat='19101500';end_date=str2num(end_dat);
str_dat='20091200';str_date=str2num(str_dat);
end_dat='20091500';end_date=str2num(end_dat);
%str_dat='20012000';str_date=str2num(str_dat);
%end_dat='20012700';end_date=str2num(end_dat);
%str_dat='20090100';str_date=str2num(str_dat);
%str_dat='20012900';str_date=str2num(str_dat);
%str_dat='20021800';str_date=str2num(str_dat);
%str_dat='20031000';str_date=str2num(str_dat);
%str_dat='20041500';str_date=str2num(str_dat);
%str_dat='20050800';str_date=str2num(str_dat);
%str_dat='20081300';str_date=str2num(str_dat);
%str_dat='20082112';str_date=str2num(str_dat);
%str_dat='20090312';str_date=str2num(str_dat);
%str_dat='20092622';str_date=str2num(str_dat);
if str_dat(1:2)=='20'
  yrpl=2020;
  xlabl='Year Day 2020 (UTC)';
elseif str_dat(1:2)=='19'
  yrpl=2019;
  xlabl='Year Day 2019 (UTC)';
end
%end_dat=input('end date_hr (e.g., 19092612)')
%end_dat='20020212';end_date=str2num(end_dat);
%end_dat='20022600';end_date=str2num(end_dat);
%end_dat='20031600';end_date=str2num(end_dat);
%end_dat='20042112';end_date=str2num(end_dat);
%end_dat='20051600';end_date=str2num(end_dat);
%end_dat='20082112';end_date=str2num(end_dat);
%end_dat='20090612';end_date=str2num(end_dat);
%end_dat='20091512';end_date=str2num(end_dat);
%end_dat='20092012';end_date=str2num(end_dat);

%PS_wxdat_file=[dir_wxdata 'PS_metdata_319_342'];
%PS_wxdat_file=[dir_wxdata 'PS_metdata_335_593'];%Dec 1_2019-Aug16_2020
%PS_wxdat_file=[dir_wxdata 'PS_metdata_226_275'];%Aug13-Oct1_2020
PS_wxdat_file=[dir_wxdata 'PS_metdata_263_640'];%Sep20_2019-Oct1_2020

if yrpl==2019 & end_dat(1:2)=='19'
  plt_str=str_date-19000000;plt_end=end_date-19000000;
elseif yrpl==2019 & end_dat(1:2)=='20'
  plt_str=str_date-19000000;plt_end=end_date-20000000;
elseif yrpl==2020
  plt_str=str_date-20000000;plt_end=end_date-20000000;
end
mostpl=floor(plt_str/10000);moenpl=floor(plt_end/10000);
day_stpl=floor((plt_str-mostpl*10000)/100);day_enpl=floor((plt_end-moenpl*10000)/100);
hr_stpl=mod(plt_str,100);hr_enpl=mod(plt_end,100);
if yrpl==2019 & end_dat(1:2)=='19'
  yd_stpl=moddystr(mostpl)+day_stpl-1+hr_stpl/24;yd_enpl=moddystr(moenpl)+day_enpl-1+hr_enpl/24;
elseif yrpl==2019 & end_dat(1:2)=='20'
  yd_stpl=moddystr(mostpl)+day_stpl-1+hr_stpl/24;yd_enpl=moddystrl(moenpl)+day_enpl-1+hr_enpl/24+365;
elseif yrpl==2020
  yd_stpl=moddystrl(mostpl)+day_stpl-1+hr_stpl/24;yd_enpl=moddystrl(moenpl)+day_enpl-1+hr_enpl/24; 
end

%specify plot characteristics
%set(gca,'fontsize',fntsz, 'TickDir','in', 'xtick',xtick_arr, 'XMinorTick','on','YMinorTick','on')
%set(gca,'fontsize',fntsz, 'TickDir','in','XMinorTick','on','YMinorTick','on')
%time series plots
fntsz=12; %font size for time series
%xtick_arr=[yd_stpl:dyintpl:yd_enpl]; %

if plot_top>=8000
  tvc=[-66:3:-12 -10:2:20];%for 12 km height  
elseif plot_top>3000
   tvc=[-56:2:-12 -10:1:6];%for 8 km height 
else
   tvc=[-44:1:6];%for 2 km height
end
tv0=[0]; %heavy contour
brb_tv=1; %wind barbs on temp cross-section?

%thc=[-20:1:32];%theta contours
%thc=[-10:1:25];
if plot_top>8000
  thc=[-44:4:116];%for >8 km height
elseif plot_top>3000
  thc=[-45:3:75];%for 3-8 km height
else
  thc=[-44:2:36];%for <3 km height
end
    
brb_th=1; %wind barbs on theta cross-section?

%thec=[-5:1:30];%the contours
%thec=[-10:2:44];%the contours
thec=[-44:4:100]; % for 12 km height
brb_the=1; %wind barbs on thetae cross-section?

%mixing ratio
qqc=[0:0.2:8];
wsc=[0:2:60];%isotachs
%wsc=[0:1:20];%isotachs
%wind barbs plots
ndypl=(yd_enpl-yd_stpl); % number of days for plotting barb scaling
xscl=.025*ndypl; %scaling for wind barbs
brb_intx=floor((yd_enpl-yd_stpl)/12) + 1;
brb_inty=round(plot_top/500);

%for rhw
rhwc=[70:5:105];
%rhwc=[95 100];
%for rhi
rhic=[0:10:120];


%com_filnam_in=[dir_wxdata '\' filnam 'ed.txt'];
cd(dir_PS_sndgdata)
files=dir(['Sondierung20*.txt']);
nf=length(files);
for i=1:nf
  sndg_times(i)=str2num(files(i).name(13:20));
end
%
%find soundings at or after start date/hr and before or at end date/hr
%
itest=find(sndg_times >= str_date & sndg_times<= end_date);
if itest(1)>1
  if itest(end)<nf
    isndg=[itest(1)-1 itest itest(end)+1];
  else
    isndg=[itest(1)-1 itest];
  end
else
  isndg=itest;
end
%found the desired soundings - now read these in
nsn=length(isndg);
for n=1:nsn
  if n==1 | n==nsn
     filnam=[dir_PS_sndgdata '\Sondierung20' num2str(sndg_times(isndg(n))) '.txt']
  else
     filnam=[dir_PS_sndgdata '\Sondierung20' num2str(sndg_times(isndg(n))) '.txt'];
  end
  fid=fopen(filnam,'r');
  if fid>0
    %
    % read in date, time, lat/lon
    %
    for nhd=1:4
      dum0=fgets(fid);
    end
    day=str2num(dum0(5:6));mo=str2num(dum0(8:9));yr(n)=str2num(dum0(11:12));
    dum0=fgets(fid);
    hh=str2num(dum0(5:6));mm=str2num(dum0(8:9));ss=str2num(dum0(11:12));
    if yrpl==2019
      yd_sndg(n)=moddystr(mo)-1+day+hh/24+(mm+ss/60)/1440;
    elseif yrpl==2020
      yd_sndg(n)=moddystrl(mo)-1+day+hh/24+(mm+ss/60)/1440;
    end
    ilrg=find(yd_sndg>366);
    if length(ilrg)>0
      yd_sndg(ilrg)=yd_sndg(ilrg)-366;
    end
    dum0=fgets(fid);
    lat_snd(n)=str2num(dum0(5:9));N_S=dum0(11);
    dum0=fgets(fid);
    ideg=findstr(dum0,'°');
    lon_snd(n)=str2num(dum0(ideg-5:ideg-1));E_W=dum0(ideg+1);
    %move past other header info
    for nhd=1:17
      dum0=fgets(fid);
    end
    %now scan in data
    [datsnd]=fscanf(fid,'%i %i %g %g %i %i %g',[7,inf]);
    [col kcnt]=size(datsnd);
    z1_sndg(n,1:kcnt)=datsnd(1,:);% Height above ground(m)
    z2_sndg(n,1:kcnt)=datsnd(2,:);% GPS height (m)
    %z_sndg(n,1:kcnt)=(z1_sndg(n,1:kcnt)+z2_sndg(n,1:kcnt))/2;
    z_sndg_avg=(z1_sndg(n,1:kcnt)+z2_sndg(n,1:kcnt))/2;
    z_sndg_avg(find(z_sndg_avg<0))=0;
    tst=find(z_sndg_avg>plot_top);
    if length(tst)==0
      klot=length(z_sndg_avg);
    else
      klot=tst(1);
    end
    clear tst
    [zuniq,ia,ic]=unique(z_sndg_avg(1:klot),'sorted'); %find the indeces of the unique, sorted heights
    kk(n)=length(zuniq);%index of top sounding
    z_sndg(n,1:kk(n))=zuniq;
    p_sndg(n,1:kk(n))=datsnd(3,ia);% pressure (hPa)
    T_sndg(n,1:kk(n))=datsnd(4,ia);% temperature (deg C)
    RHw_sndg(n,1:kk(n))=datsnd(5,ia);% Rel Hum wrt water(%)
    WD_sndg(n,1:kk(n))=datsnd(6,ia);% Wind Direction(deg)
    WS_sndg(n,1:kk(n))=datsnd(7,ia);% Wind Speed(m/s)
    alt=z_sndg(n,1:kk(n));
  else
    disp(['File identfier wrong. fid= ' num2str(fid) ' for file ' filnam])
  end
  clear datsnd filnam
end
z_sndg(find(z_sndg<0))=0;
kkmx=max(kk);%maximum number of levels in any sounding
for n=1:nsn
  z1_sndg(n,kk(n)+1:kkmx)=NaN;
  z2_sndg(n,kk(n)+1:kkmx)=NaN;
  z_sndg(n,kk(n)+1:kkmx)=NaN;
  p_sndg(n,kk(n)+1:kkmx)=NaN;
  T_sndg(n,kk(n)+1:kkmx)=NaN;
  RHw_sndg(n,kk(n)+1:kkmx)=NaN;
  WD_sndg(n,kk(n)+1:kkmx)=NaN;
  WS_sndg(n,kk(n)+1:kkmx)=NaN;
end
%edit data
p_sndg(find(p_sndg<10 | p_sndg>1100))=NaN;
z1_sndg(find(z1_sndg<0))=NaN;
z2_sndg(z2_sndg<0)=NaN;
z_sndg(find(z_sndg<0))=NaN;
T_sndg(find(abs(T_sndg)>100))=NaN;
%td(find(abs(td)>100))=NaN;
RHw_sndg(find(RHw_sndg>110 | RHw_sndg<0))=NaN;
WS_sndg(find(WS_sndg>200 | WS_sndg<0))=NaN;
WD_sndg(find(WD_sndg>370 | WD_sndg<0))=NaN;
lat_snd(find(lat_snd<70 |lat_snd>90))=NaN;
lon_snd(find(lon_snd<-60 |lon_snd>180))=NaN;

%
% find mixed-layer height for each sounding
%
mlh(1:nsn)=NaN;
thvgrd_thrsh=1/110; dz_thrsh=100; %threshold in thatv gradient (deg C/m) and depth of gradient layer (m) for defining mixed-layer top
for n=1:nsn
   thetav(1:kk(n))=NaN;
   for k=1:kk(n)
     %calculate vapor mixing ratio and RH wrt ice and water
     prs=p_sndg(n,k);
     tk=T_sndg(n,k)+273.15;
     qvsndg=wbol(tk,prs,RHw_sndg(n,k)/100);
     esi=(1.0003+prs*4.18e-6)*6.1115*exp(22.452*T_sndg(n,k)/(272.55+T_sndg(n,k)));
     qsi=0.622*esi/(prs-esi)*1000;
     rhisndg=100*1000*qvsndg*(1+qsi/622)/(qsi*(1+1000*qvsndg/622));
     
     %calculate potential temperature and equivalent potential temperature

     tha=thetab(prs,tk,qvsndg);
     thetav(k)=tha*(1.+.608*qvsndg);
%     the(k,i)=thebol(prs,tk,qvsndg);
   end

  tst=find(z_sndg(n,:)>=dz_thrsh); i=tst(1);clear tst; % start with obs at first height above dz_thresh to get away from ship effect
  ztst=z_sndg(n,i);
  while ztst<z_sndg(n,kk(n))
    i = i+1;
    thv1=thetav(i);
    dztst=z_sndg(n,i)-z_sndg(n,1:i-1);
    ilwtst=find(dztst>=dz_thrsh);
    if length(ilwtst)>0
      ilw=ilwtst(end);
      dz=z_sndg(n,i)-z_sndg(n,ilw);
      thv0=thetav(ilw);
      thvgrd=(thv1-thv0)/dz;
      if thvgrd>thvgrd_thrsh
         mlh(n)=z_sndg(n,ilw)+dz/2;
         ztst=z_sndg(n,kk(n));
      end
    end
    clear thv1 dztst ilwtst;
  end
end

%
% load MOSAiC/Polarstern met data file
%
load(PS_wxdat_file) 
  % yd_PS - decimal year day (UTC)
  % PS_hdg - ship heading (deg)
  % PS_cog - ship course over ground (deg)
  % PS_lat - ship latitude (deg)
  % PS_lon - ship longitude (deg)
  % PS_spd - ship speed(knots)
% met data
%  press - air Pressure (hPa)
%  Tair - air T (deg C)
%  cld_base - ceiling in m
%  Tdair - air dew Point (deg C)
%  SWdir - direct solar radiation (w/m2)
%  SWglob - %global solar radiation (w/m2)
%  WSmx - max wind last minute (m/s)
%  prcp - precip (mm/min)
%  RHw - relative humidity (%)
%  WDrel - relative wind direction (deg)
%  WSrel - relative wind velocity (m/s)
%  WDtrue - true wind direction (deg)
%  WStrue - true wind velocity (m/s)
%  vis - visibility (km)
%  Twat - water temperature (deg C)
%
%set for Day of Year 2020 based on plot start date
if yrpl==2020
  yd_PS=yd_PS-365;
end
%calculate floe drift velocity from ship location after 14 UTC Oct 4, 2019
%(277+14/24)
%jd_drift_str=277+14/24;
jd_drift_str=yd_PS(1);
idrft=find(yd_PS>=jd_drift_str);ndrft=length(idrft);
flo_spd(1:ndrft)=NaN;flo_dir(1:ndrft)=NaN;
for i=2:ndrft-1
  xy=distance_op(PS_lat(idrft(i-1)),PS_lat(idrft(i+1)),PS_lon(idrft(i-1)),PS_lon(idrft(i+1)));
  flo_spd(i)=xy(3)/((yd_PS(idrft(i+1))-yd_PS(idrft(i-1)))*2); % floe speed in km/12 hours
  flo_dir(i)=mod(xy(4)+180,360); % "from" floe direction (deg)-- to be compatible with wind convention
end
iinterf=find(flo_spd>25); flo_spd(iinterf)=NaN;flo_dir(iinterf)=NaN; %edit apparent gps interference points
clear xy iinterf

%load other data to plot on soundings


%Write data to file
sav_dat=0;
if sav_dat==1; % save soundings to file
   for i=1:nsn
     clear spec
%     g=['C:\Users\opersson\Documents\ACSE\Data\Rawinsondes\sounding_ts12km.txt'];
     g=['D:\ONRSeaState\Data\Rawinsondes\sounding_ts12km.txt'];     
     gidt=fopen(g,'a');                  
     datcol(1,1)=jd(i);
     hr=floor((jd(i)-floor(jd(i)))*24);
     datcol(2,1)=hr;
     mn=((jd(i)-floor(jd(i)))*24-hr)*60;
     datcol(3,1)=mn;                
     datcol(4,1)=n(i);
     datcol(5,1)=lats(i);
     datcol(6,1)=lons(i);
     fprintf(gidt,'%9.4f %4i %3i %5i %9.4f %10.4f \r',datcol);                  
 %   for spct=1:n(i)-1
       spec(1,1:n(i))=alt(i,1:n(i));
       spec(2,1:n(i))=p(i,1:n(i));
       spec(3,1:n(i))=t(i,1:n(i));
       spec(4,1:n(i))=td(i,1:n(i));
       spec(5,1:n(i))=rh(i,1:n(i));
       spec(6,1:n(i))=ws(i,1:n(i));
       spec(7,1:n(i))=wd(i,1:n(i));
 %   end;%for spct
 %vectorized print, 5 columns, spct rows
     fprintf(gidt,'%9.1f %9.1f %9.1f %9.1f %9.1f %9.1f %9.0f\r',spec);
     clear spec datcol
     fclose(gidt);
   end; %for i
end; %end sav_soundings  


%interpolation of sounding data onto T-H grid
zint=[0:5:40 50:10:160 175:25:plot_top];
nlv=length(zint);
wsint(1:nsn,1:nlv)=NaN;wdint(1:nsn,1:nlv)=NaN;tint(1:nsn,1:nlv)=NaN;rhint(1:nsn,1:nlv)=NaN;
pint(1:nsn,1:nlv)=NaN;tdint(1:nsn,1:nlv)=NaN;
wsr=WS_sndg;wdr=WD_sndg;t=T_sndg;rh=RHw_sndg;p=p_sndg;z=z_sndg;

if if_plot>0
  z(find(z<0))=NaN;
  for k=1:nsn
      %Interpolate data in the vertical to interpolated sounding levels
     zgd=find(abs(wsr(k,:))<70);
     tstgd=size(zgd,2);
      if tstgd > 1
        temp_data=wsr(k,zgd);
        temp_z=z(k,zgd);
        temp=interp1(temp_z,temp_data,zint,'linear');
        tempgd=find(abs(temp)<70);
        wsint(k,tempgd)=temp(tempgd);
      else
        wsint(k,1:nlv)=-999;
      end    
      clear zgd tstgd temp_data temp_z temp
      
     zgd=find(abs(wdr(k,:))<400);
     tstgd=size(zgd,2);
      if tstgd > 1
        temp_data=wdr(k,zgd);
        temp_z=z(k,zgd);
        temp=interp1(temp_z,temp_data,zint,'linear');
        tempgd=find(abs(temp)<400);
        wdint(k,tempgd)=temp(tempgd);
      else
        wdint(k,1:nlv)=-999;
      end    
      clear zgd tstgd temp_data temp_z temp
      
     zgd=find(abs(t(k,:))<100);
     tstgd=size(zgd,2);
      if tstgd > 1
        temp_data=t(k,zgd);
        temp_z=z(k,zgd);
        temp=interp1(temp_z,temp_data,zint,'linear');
        tempgd=find(abs(temp)<100);
        tint(k,tempgd)=temp(tempgd);
      else
        tint(k,1:nlv)=-999;
      end    
      clear zgd tstgd temp_data temp_z temp
      
     zgd=find(abs(rh(k,:))<110);
     tstgd=size(zgd,2);
      if tstgd > 1
        temp_data=rh(k,zgd);
        temp_z=z(k,zgd);
        temp=interp1(temp_z,temp_data,zint,'linear');
        tempgd=find(abs(temp)<110);
        rhint(k,tempgd)=temp(tempgd);
      else
        rhint(k,1:nlv)=-999;
      end    
      clear zgd tstgd temp_data temp_z temp
      
     zgd=find(p(k,:)> 50);
     tstgd=size(zgd,2);
      if tstgd > 1
        temp_data=p(k,zgd);
        temp_z=z(k,zgd);
        temp=interp1(temp_z,temp_data,zint,'linear');
        tempgd=find(temp>50);
        pint(k,tempgd)=temp(tempgd);
      else
        pint(k,1:nlv)=-999;
      end    
      clear zgd tstgd temp_data temp_z temp
      
  %   zgd=find(abs(td(k,:))<110);
  %   tstgd=size(zgd,2);
  %    if tstgd > 1
  %      temp_data=td(k,zgd);
  %      temp_z=z(k,zgd);
  %      temp=interp1(temp_z,temp_data,zint,'linear');
  %      tempgd=find(abs(temp)<110);
  %      tdint(k,tempgd)=temp(tempgd);
  %    else
  %       tdint(k,1:nlv)=-999;
  %    end    
  %    clear zgd tstgd temp_data temp_z temp

     % Now interpolate in the vertical across missing data
     igd=find(abs(tint(k,:))<100);
     if length(igd)>1
     temp_data=tint(k,igd);
     temp_z=zint(igd);
     temp=interp1(temp_z,temp_data,zint);
     tint(k,:)=temp;
     end
     clear igd temp_data temp_z temp
     
     igd=find(abs(rhint(k,:))<130);
     if length(igd)>1
     temp_data=rhint(k,igd);
     temp_z=zint(igd);
     temp=interp1(temp_z,temp_data,zint);
     rhint(k,:)=temp;
     end
     clear igd temp_data temp_z temp
     
     igd=find(abs(wsint(k,:))<100);
     if length(igd) >1
     temp_data=wsint(k,igd);
     temp_z=zint(igd);
     temp=interp1(temp_z,temp_data,zint);
     wsint(k,:)=temp;
     end
     clear igd temp_data temp_z temp

     igd=find(abs(wdint(k,:))<370);
     if length(igd)>1
     temp_data=wdint(k,igd);
     ichgt=find(temp_data<=180);
     temp_data(ichgt)=temp_data(ichgt)+360;
     temp_z=zint(igd);
     temp=interp1(temp_z,temp_data,zint);
     wdint(k,:)=mod(temp,360);
     end
     clear igd temp_data temp_z temp
     
     igd=find(pint(k,:)>50);
     if length(igd)>1
     temp_data=pint(k,igd);
     temp_z=zint(igd);
     temp=interp1(temp_z,temp_data,zint);
     pint(k,:)=temp;
     end
     clear igd temp_data temp_z temp
     
     igd=find(abs(tdint(k,:))<90);
     if length(igd)>1
     temp_data=tdint(k,igd);
     temp_z=zint(igd);
     temp=interp1(temp_z,temp_data,zint);
     tdint(k,:)=temp;
     end
     clear igd temp_data temp_z temp
              
     zint(find(zint<0))=NaN;
  end
  
  % find non-realistic values
  pint(find(pint>1100 | pint < 50))=NaN;
  wdint(find(wdint>360 | wdint < 0))=NaN;
  wsint(find(abs(wsint) > 70))=NaN;
  tint(find(abs(tint)>90))=NaN;
  rhint(find(rhint>120 | rhint<0))=NaN;
  
  %save interpolated sounding data
pint; 
tint;
sav_dat_int=0;
if sav_dat_int==1; % save soundings to file
  filnamsav=['C:\Users\opersson\Documents\ACSE\Data\Rawinsondes\ACSE_sonde_data_' num2str(alt_top/1000) 'km_0' num2str(date_st) '_0' num2str(date_en)]
  save(filnamsav,'nsn','jd','zint','pint','tint','rhint','wsint','wdint');
end; %end sav_soundings 

jd=yd_sndg;
if(jd(1)>200 & jd(end)<180)
  swtch=find(jd<180);
  jd(swtch)=jd(swtch)+365;
end
% interpolate temporally for each level
  for i=1:nlv
   
   kgd=find(abs(tint(:,i))<90);
   if size(kgd,1) > 1
     temp_data=tint(kgd,i);
     temp_t=jd(kgd);
     temp=interp1(temp_t,temp_data,jd,'linear');
     tint(1:nsn,i)=transpose(temp);
   end
     clear kgd temp_data temp_t temp
     
     kgd=find(abs(rhint(:,i))<130);
     if size(kgd,1) > 1
     temp_data=rhint(kgd,i);
     temp_t=jd(kgd);
     temp=interp1(temp_t,temp_data,jd,'linear');
     rhint(1:nsn,i)=transpose(temp);
     end
     clear kgd temp_data temp_t temp
     
     kgd=find(abs(wsint(:,i))<90);
     if size(kgd,1) > 1
     temp_data=wsint(kgd,i);
     temp_t=jd(kgd);
     temp=interp1(temp_t,temp_data,jd,'linear');
     wsint(1:nsn,i)=transpose(temp);
     end
     clear kgd temp_data temp_t temp
     
     kgd=find(abs(wdint(:,i))<400);
      if size(kgd,1) > 1
     temp_data=wdint(kgd,i);
     ichgt=find(temp_data<=180);
     temp_data(ichgt)=temp_data(ichgt)+360;
     temp_t=jd(kgd);
     temp=interp1(temp_t,temp_data,jd,'linear');
     wdint(1:nsn,i)=transpose(mod(temp,360));
     end
     clear kgd temp_data temp_t temp
          
     kgd=find(pint(:,i)<1100 & pint(:,i)>0);
     if size(kgd,1) > 1
     temp_data=pint(kgd,i);
     temp_t=jd(kgd);
     temp=interp1(temp_t,temp_data,jd,'linear');
     pint(1:nsn,i)=transpose(temp);
     end
     clear kgd temp_data temp_t temp
  end
  
% find non-realistic values
  pint(find(pint>1100 | pint < 50))=NaN;
  wdint(wdint>360 | wdint < 0)=NaN;
  wsint(find(abs(wsint) > 70))=NaN;
  tint(find(abs(tint)>90))=NaN;
  rhint(find(rhint>120 | rhint<0))=NaN;

%The soundings are interpolated.  Now calculate rhice, thetav, & thetae
for k=1:nsn
   for i=1:nlv
     %calculate vapor mixing ratio and RH wrt ice and water
     prs=pint(k,i);
     tk=tint(k,i)+273.15;
     qvint(k,i)=wbol(tk,prs,rhint(k,i)/100);
     esi=(1.0003+prs*4.18e-6)*6.1115*exp(22.452*tint(k,i)/(272.55+tint(k,i)));
     qsi=0.622*esi/(prs-esi)*1000;
     rhiint(k,i)=100*1000*qvint(k,i)*(1+qsi/622)/(qsi*(1+1000*qvint(k,i)/622));
     
     %calculate potential temperature and equivalent potential temperature

     tha=thetab(prs,tk,qvint(k,i));
     thav(k,i)=tha*(1.+.608*qvint(k,i));
     the(k,i)=thebol(prs,tk,qvint(k,i));
  end
end
%Calculate gradient diagnostics, e.g., Ri, and N-squared
for k=1:nsn
   for i=1:nlv-1
     dz=zint(i+1)-zint(i);
     nsq(k,i)=(grav/(thav(k,i)+thav(k,i+1)))*(thav(k,i+1)-thav(k,i))/dz;
   end
   for i=1:nlv-1
     dws=wsr(k,i+1)-wsr(k,i);
     dz=zint(i+1)-zint(i);
     z_ri(i)=zint(i)+dz/2;
     if abs(dws)<0.01
       ri(k,i)=NaN;
     else
        ri(k,i)=nsq(k,i)*dz*dz/(dws*dws);
        if ri(k,i)>2
           ri(k,i)=2;
        end
     end
   end
end 


%do contourf plots
%set axes
%x97=floor(jd(snd_st);
%y=z(1,:);
%yri=z_ri(1,:);
zb=0;zt=plot_top;

clear tst
tst=find(zint<=zt);
k2=-max(-tst(size(tst,2)),-size(z,2));
clear tst
tst=find(zint>=zb);
k1=tst(1);
y=zint(k1:k2);
yri=z_ri(k1:k2-1);

t1=floor(jd(1)*8)/8;t2=(ceil(jd(nsn)*8))/8;%auto start and end times to plot
clear tst
tst=find(jd>=t1);
x1=tst(1);
clear tst
tst=find(jd<=t2);
x2=tst(size(tst,2));
x=jd(1:nsn);
%iceilo=find(yd_PS>=jd(1) & yd_PS<=jd(nsn));
iceilo=find(yd_PS>=yd_stpl & yd_PS<=yd_enpl);
zbot(1:nsn)=zint(k1);

%find cloud top
testarrw=transpose(rhint(x1:x2,k1:k2));
testarri=transpose(rhiint(x1:x2,k1:k2));
for ii=x1:x2
    testw=find(testarrw(:,ii)>95);
    testi=find(testarri(:,ii)>99);
    if length(testw)>0
      cld_topw(ii)=y(testw(length(testw)));
    else
      cld_topw(ii)=NaN;
    end
    if length(testi)>0
      cld_topi(ii)=y(testi(length(testi)));
    else
      cld_topi(ii)=NaN;
    end
    clear testw testi
end
clear testarrw testarri

if if_plot==4 %4-panel plots
    %temperature plot
np=np+1;
figure(np)
v=[-60:3:12];
%v=[-25:1:5];
arr=transpose(tint(x1:x2,k1:k2));
subplot(2,2,1),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
%desc=[num2str(date(snd_st)) ' - ' num2str(date(snd_en))]
desc=[num2str(plt_str) ' - ' num2str(plt_end)];
title([' T (deg C); ' desc ]);
%axis([yd_stpl yd_enpl zb zt])
axis([yd_stpl yd_enpl zb zt])

hold on
plot(jd,zbot,'r*')
hold off
  
%thetav
if pltthav==1;
%np=np+1;
figure(np)
%v=[-14:2:30];
v=[-16:4:64];
arr=transpose(thav(x1:x2,k1:k2))-273.15;
subplot(2,2,2),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Thav (deg C); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltthe==1
%thetae
%np=np+1;
figure(np)
v=[-20:3:70];
%v=[-10:1:30];
arr=transpose(the(x1:x2,k1:k2))-273.15;
colormap default
subplot(2,2,3),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' THE (deg C); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltnsq==1
%N2
%np=np+1;
figure(np)
v=[-6:1:40];
arr=transpose(nsq(x1:x2,k1:k2-1)*1e4);
subplot(2,2,4),[C,h]=contourf(x,yri,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Brunt-Vaisala Frequency (x 10^-^4s^-^1); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltrhi==1
%relative humidity wrt ice
np=np+1;
figure(np)
v=rhic;
arr=transpose(rhiint(x1:x2,k1:k2));
subplot(2,2,1),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' RH wrt ice (%); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltrhw==1
%relative humidity wrt water
%np=np+1;
figure(np)
v=[0:5:120];
arr=transpose(rhint(x1:x2,k1:k2));
subplot(2,2,2),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' RH wrt water (%); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltqv==1
%water vapor mixing ratio
%np=np+1;
figure(np)
v=[0:0.3:9];
arr=transpose(qvint(x1:x2,k1:k2))*1000;
subplot(2,2,3),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Water Vapor Mixing Ratio (g/kg); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltws==1
%wind speed
%np=np+1;
figure(np)
v=[0:2:40];
arr=transpose(wsint(x1:x2,k1:k2));
subplot(2,2,4),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Wind Speed (m/s); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off

if pltbrb==1
    xscl=.09;yscl=xscl*(zt-zb)/((t2-t1)*0.9);
hold on
[ynarr xnarr]=size(arr);
for i=1:brb_intx:xnarr
    xlab=x(i);
    iwd=x1+i-1;
    for j=1:brb_inty:ynarr
       ylab=y(j);
       flg=barb2(xlab,ylab,arr(j,i),wdint(iwd,j),xscl,yscl);
%  num_lab=num2str(round(the(n_10ma(i))));
%  text(xlab,ylab,num_lab)
    end
end
hold off
end

end

if pltwd==1
%wind direction
np=np+1;
figure(np)
%dwst=find(wdint>180);
%wdint(dwst)=wdint(dwst)-360;
wdint(find(wdint<-360))=NaN;
%v=[-180:30:180];
v=[0:30:360];
arr=transpose(wdint(x1:x2,k1:k2));
[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Wind Direction (deg true); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltri==1
%Ri
np=np+1;
figure(np)
v=[-1:.25:2];
arr=transpose(ri(x1:x2,k1:k2-1));
[C,h]=contourf(x,yri,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Richardson Number; ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end
end %if if_plot==4

if if_plot==1 %single plots - color
    
if plot_top>8000
%calculate tropopause height
   for i=1:nsn
     tmin=min(tint(i,:));
     ktmin=find(tint(i,:)==tmin);
     ztrop(i)=zint(ktmin(1));
   end
end
np=np+1;
figure(np)
arr=transpose(tint(x1:x2,k1:k2));
mxT=max(arr,[],'all');mnT=min(arr,[],'all');
%v=[-60:3:6];
dtvc=round(mean(tvc(2:end)-tvc(1:end-1)));
v=[floor(mnT-dtvc/2):dtvc:ceil(mxT+2*dtvc)];
%v=tvc;
[C,h]=contourf(x,y,arr,v);caxis([v(1) v(end)]);clabel(C,h,v);colorbar('EastOutside');colormap jet
hold on
[C,h]=contour(x,y,arr,[tv0,tv0],'r-','LineWidth',2);clabel(C,h);
hold off
xlabel(xlabl);
ylabel('Height (m)');
%desc=[num2str(date(snd_st)) ' - ' num2str(date(snd_en))];
if plt_str<100000
  cplt_str=['0' num2str(plt_str)];
else
  cplt_str=num2str(plt_str);
end
if plt_end<100000
  cplt_end=['0' num2str(plt_end)];
else
  cplt_end=num2str(plt_end);
end
desc=['MOSAiC ' cplt_str ' ' num2str(yr(1)) ' - ' cplt_end ' ' num2str(yr(end))];
descsh=[num2str(yr(1)) cplt_str '-' num2str(yr(end)) cplt_end];
moind=[(mostpl-1)*3+1:(mostpl-1)*3+3];
%descmo=[monam(moind) num2str(yr(1))];
if mostpl<10
  monc=['0' num2str(mostpl)];
else
  monc=num2str(mostpl);
end
%descmo=[num2str(yr(1)) monc];
descmo=descsh;
if isotachs_on_T==1
  title([desc ';      T (deg C, color); isotachs (m/s, red); mixed layer height (solid yellow); cloud top (black dash); cloud base (black x)']);
else
  title([desc ';      T (deg C, color); mixed layer height (solid yellow); cloud top (black dash); cloud base (black x)']);
end
axis([yd_stpl yd_enpl zb zt])
if plot_top<3000
  tick_int=200;
elseif plot_top<6000
  tick_int=400;
else
  tick_int=500;
end
if yd_enpl-yd_stpl>=7
  fntsz=12; % for time periods >= 7 days use smaller axis label font
else
  fntsz=14;
end
set(gca,'fontsize',fntsz, 'TickDir','in','XMinorTick','on','YMinorTick','on')
hold on
plot(jd,zbot,'r*')
plot(yd_PS(iceilo),cld_base(iceilo),'kx')
plot(jd,cld_topw,'kx--','LineWidth',4)
plot(jd,mlh,'yx-','LineWidth',4)
if plot_top>8000 %plot tropopause height
  plot(jd,ztrop,'g-','LineWidth',4)
end
if brb_tv==1; %wind barbs on temp cross-section
  yscl=xscl*(zt-zb)/((t2-t1)*0.9);
  [ynarr xnarr]=size(arr);
  for i=1:brb_intx:xnarr
    xlab=x(i);
    iwd=x1+i-1;
    for j=1:brb_inty:ynarr
       ylab=y(j);
       flg=barb2(xlab,ylab,wsint(iwd,j),wdint(iwd,j),xscl,yscl);
%  num_lab=num2str(round(the(n_10ma(i))));
%  text(xlab,ylab,num_lab)
    end
  end 
end
hold off
if isotachs_on_T==1
%wind speed
  hold on
  v=[6:3:60];
  arr=transpose(wsint(x1:x2,k1:k2));
  [C,h]=contour(x,y,arr,v,'b-','LineWidth',2);clabel(C,h,'FontSize',12,'Color','b','FontWeight','bold');%colormap jet
 % xlabel('Year Day ');
 % ylabel('Height (m)');
%  title([' Wind Speed (m/s); ' desc ]);
  %axis([yd_stpl yd_enpl zb zt])
  hold off
end

%
%plot time series below
%
np=np+1;figure(np)
subplot(5,1,1),plot(yd_PS(iceilo),press(iceilo),'r.-',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[1000 1000],'k--');
%xlabel('Year Day (2019, UTC)');
ylabel('Press (hPa)')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))])
xlim([yd_stpl yd_enpl])
set(gca,'fontsize',fntsz, 'TickDir','in','XMinorTick','on','YMinorTick','on')

%subplot(5,1,2),plot(yd_PS(iceilo),Tair(iceilo),'r.-',yd_PS(iceilo),Tdair(iceilo),'b.-',yd_PS(iceilo),Twat(iceilo),'g.-',[event_time event_time],[-5 1],'r--',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[0 0],'k--');
%legend('T_a_i_r','T_d','T_w_t_r','Location','best')
subplot(5,1,2),plot(yd_PS(iceilo),Tair(iceilo),'r-',yd_PS(iceilo),Tdair(iceilo),'b-',yd_PS(iceilo),Twat(iceilo),'g--',[event_time event_time],[-5 1],'r--',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[0 0],'k--','LineWidth',2);
legend('T_a_i_r','T_d','T_w_a_t','Location','best')
legend('boxoff')
ymn=floor(min([Tair(iceilo) Tdair(iceilo) Twat(iceilo)])); ymx=ceil(max([Tair(iceilo) Tdair(iceilo) Twat(iceilo)]));
%ymn=floor(min([Tair(iceilo) Tdair(iceilo)])); ymx=ceil(max([Tair(iceilo) Tdair(iceilo)]));
%ylim([-10 1])
ylim([ymn ymx])
%xlabel('Year Day (2019, UTC)');
ylabel('T (deg C)')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))])
xlim([yd_stpl yd_enpl])
set(gca,'fontsize',fntsz, 'TickDir','in','XMinorTick','on','YMinorTick','on')
%subplot(5,1,3),plot(yd_PS(iceilo),WStrue(iceilo),'r.-',yd_PS(idrft),flo_spd(1:ndrft),'b.-');
subplot(5,1,3),plot(yd_PS(iceilo),WStrue(iceilo),'r.-');
%xlabel('Year Day (2019, UTC)');
%ylabel('m/s or km/12h')
ylabel('WS(m/s)')
%legend('Wind Speed','floe speed','Location','best')
%legend('boxoff')
ymxpl=2*max(ceil(WStrue(iceilo))/2);
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))]);
xlim([yd_stpl yd_enpl]);
ylim([0 ymxpl])
set(gca,'fontsize',fntsz, 'TickDir','in','XMinorTick','on','YMinorTick','on')
%subplot(5,1,4),plot(yd_PS(iceilo),WDtrue(iceilo),'r.-',yd_PS(idrft),flo_dir(1:ndrft),'b.-');
WDt_plot=WDtrue(iceilo);
mxwdpl=max(WDt_plot);mnwdpl=min(WDt_plot);
%if mxwdpl-mnwdpl>270
%  ichg=find(WDt_plot>180);
%  WDt_plot(ichg)=WDt_plot(ichg)-360;
%end
mnpl=5*min(floor(WDt_plot/5));
mxpl=5*max(ceil(WDt_plot/5));
subplot(5,1,4),plot(yd_PS(iceilo),WDt_plot,'r.-',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[0 0],'k:');
%xlabel('Year Day (2019, UTC)');
%ylabel('deg')
ylabel('WD(deg)')
%legend('Wind Dir','floe dir','Location','best')
%legend('boxoff')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))]);
xlim([yd_stpl yd_enpl])
%ylim([0 360])
ylim([mnpl mxpl])
set(gca,'fontsize',fntsz, 'TickDir','in','XMinorTick','on','YMinorTick','on')
%subplot(5,1,3),plot(yd_PS(iceilo),2*WStrue(iceilo),'r.-',yd_PS(iceilo),WDtrue(iceilo)/10,'b.-');xlabel('Year Day (2019, UTC)');ylabel('Wind Speed or Dir (knots or deg/10)')
%legend('WS','WD/10')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))]);ylim([0 36])
%subplot(4,1,4),plot(yd_PS(iceilo),WDtrue(iceilo),'r.-');xlabel('Year Day (2019, UTC)');ylabel('Wind Direction true (deg)');ylim([0 360])
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))])
%np=np+1;figure(np)
%subplot(4,1,1),plot(yd_PS(iceilo),RHw(iceilo),'r.-',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[100 100],'k--');xlabel('Year Day (2019, UTC)');ylabel('Relative Humidity wrt water (%)')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))])
%subplot(5,1,4),plot(yd_PS(iceilo),SWglob(iceilo),'r.-',yd_PS(iceilo),SWdir(iceilo),'b.-',[event_time event_time],[0 50],'b--');
%legend('SW_g_l_o_b','SW_d_i_r')
%xlabel('Year Day (2019, UTC)');ylabel('Solar Radiation (W/m2)')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))])
%subplot(4,1,3),plot(yd_PS(iceilo),cld_base(iceilo),'r.-',yd_PS(iceilo),100*vis(iceilo),'b.-');xlabel('Year Day (2019, UTC)');ylabel('m or 10m')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))])
subplot(5,1,5),semilogy(yd_PS(iceilo),vis(iceilo),'b.-',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[10 10],'k--',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[1 1],'k--',[yd_PS(iceilo(1)) yd_PS(iceilo(end))],[0.3 0.3],'k--');
xlabel(xlabl);
ylabel('visibility (km)')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))]);
xlim([yd_stpl yd_enpl])
ylim([0.1 100])
%legend('cloud base(m)','visibility(100 m)')
%subplot(4,1,4),plot(yd_PS(iceilo),60*prcp(iceilo),'r.-');xlabel('Year Day (2019, UTC)');ylabel('Precip rate (mm/h)')
%xlim([yd_PS(iceilo(1)) yd_PS(iceilo(end))])
set(gca,'fontsize',fntsz, 'TickDir','in','XMinorTick','on','YMinorTick','on') 

%thetav
thvovrly='isotachs';cldbaspl=0;
if pltthav==1;
np=np+1;figure(np)
%v=[-10:2:50];
v=thc;
arr=transpose(thav(x1:x2,k1:k2))-273.15;
[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
%[C,h]=contourf(x,y,arr,v,'k-','LineWidth',2);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Thav (deg C); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
  if thvovrly=='isotachs'
    v=[10:2:wsc(end)];
    arrov=transpose(wsint(x1:x2,k1:k2));
    [C,h]=contour(x,y,arrov,v,'r-','LineWidth',2,'Showtext','off');clabel(C,h,'FontSize',12,'Color','r','FontWeight','bold');%colormap jet
  end
  plot(jd,zbot,'r*')
  if plot_top>8000 %plot tropopause height
    plot(jd,ztrop,'g-','LineWidth',4)
  end
  if cldbaspl==1;
    plot(yd_PS(iceilo),cld_base(iceilo),'kx')
  end
  plot(jd,mlh,'yx-','LineWidth',4)
  if brb_th==1; %wind barbs on thav cross-section
    yscl=xscl*(zt-zb)/((t2-t1)*0.9);
    [ynarr xnarr]=size(arr);
    for i=1:brb_intx:xnarr
      xlab=x(i);
      iwd=x1+i-1;
      for j=1:brb_inty:ynarr
         ylab=y(j);
         flg=barb2(xlab,ylab,wsint(iwd,j),wdint(iwd,j),xscl,yscl);
%  num_lab=num2str(round(the(n_10ma(i))));
%  text(xlab,ylab,num_lab)
      end
    end 
  end
hold off
end

if pltthe==1
%thetae
np=np+1;
figure(np)
%v=[-20:3:82];
v=thec;
arr=transpose(the(x1:x2,k1:k2))-273.15;
[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
lablc=v(1:3:end);
%[C,h]=contour(x,y,arr,v);%colormap jet
%h.LineColor='k';h.LineWidth=1;h.ShowText='on';
clabel(C,h,lablc);
xlabel(xlabl);
ylabel('Height (m)');
title([' THE (deg C); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
if plot_top>8000 %plot tropopause height
  plot(jd,ztrop,'g-','LineWidth',4)
end
if brb_the==1; %wind barbs on thetae cross-section
  yscl=xscl*(zt-zb)/((t2-t1)*0.9);
  [ynarr xnarr]=size(arr);
  for i=1:brb_intx:xnarr
    xlab=x(i);
    iwd=x1+i-1;
    for j=1:brb_inty:ynarr
       ylab=y(j);
       flg=barb2(xlab,ylab,wsint(iwd,j),wdint(iwd,j),xscl,yscl);
%  num_lab=num2str(round(the(n_10ma(i))));
%  text(xlab,ylab,num_lab)
    end
  end 
end
hold off
end

if pltnsq==1
%N2
np=np+1;
figure(np)
v=[-6:1:40];
arr=transpose(nsq(x1:x2,k1:k2-1)*1e4);
[C,h]=contourf(x,yri,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' Brunt-Vaisala Frequency (x 10^-^4s^-^1); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
if plot_top>8000 %plot tropopause height
  plot(jd,ztrop,'g-','LineWidth',4)
end
hold off
end

if pltrhi==1
%relative humidity wrt ice
np=np+1;
figure(np)
v=[0:10:120];
arr=transpose(rhiint(x1:x2,k1:k2));
[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' RH wrt ice (%); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
plot(yd_PS(iceilo),cld_base(iceilo),'kx')
if plot_top>8000 %plot tropopause height
  plot(jd,ztrop,'g-','LineWidth',4)
end
hold off
end

if pltrhw==1
%relative humidity wrt water
np=np+1;
figure(np)
%v=[0:5:120];
%v=[95 100];
v=rhwc;
arr=transpose(rhint(x1:x2,k1:k2));
%[C,h]=contourf(x,y,arr,v);clabel(C,h);
[C,h]=contourf(x,y,arr,v,'k-','LineWidth',2);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' RH wrt water (%); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
plot(yd_PS(iceilo),cld_base(iceilo),'kx')
if plot_top>8000 %plot tropopause height
  plot(jd,ztrop,'g-','LineWidth',4)
end
hold off
end

if pltqv==1
%water vapor mixing ratio
np=np+1;
figure(np)
%v=[0:0.3:9];
v=qqc;
arr=transpose(qvint(x1:x2,k1:k2))*1000;
[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' Water Vapor Mixing Ratio (g/kg); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltws==1
%wind speed
np=np+1;
figure(np)
v=wsc;
arr=transpose(wsint(x1:x2,k1:k2));
[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' Wind Speed (m/s); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
if plot_top>8000 %plot tropopause height
  plot(jd,ztrop,'g-','LineWidth',4)
end
hold off

if pltbrb==1
    yscl=xscl*(zt-zb)/((t2-t1)*0.9);
hold on
[ynarr xnarr]=size(arr);
for i=1:brb_intx:xnarr
    xlab=x(i);
    iwd=x1+i-1;
    for j=1:brb_inty:ynarr
       ylab=y(j);
       flg=barb2(xlab,ylab,arr(j,i),wdint(iwd,j),xscl,yscl);
%  num_lab=num2str(round(the(n_10ma(i))));
%  text(xlab,ylab,num_lab)
    end
end
hold off
end

end

if pltwd==1
%wind direction
np=np+1;
figure(np)
%dwst=find(wdint>180);
%wdint(dwst)=wdint(dwst)-360;
wdint(find(wdint<-360))=NaN;
%v=[-180:30:180];
v=[0:30:360];
arr=transpose(wdint(x1:x2,k1:k2));
[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' Wind Direction (deg true); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltri==1
%Ri
np=np+1;
figure(np)
v=[-1:.25:2];
arr=transpose(ri(x1:x2,k1:k2-1));
[C,h]=contourf(x,yri,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' Richardson Number; ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end
end %end if_plot=1


if if_plot==2 %2-panel contour plots for overlaying on remote sensing data    
%temperature plot
np=np+1;
figure(np)
v=[-60:3:12];
%v=[-20:1:5];
arr=transpose(tint(x1:x2,k1:k2));
subplot(2,1,1),[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
%desc=[num2str(date(snd_st)) ' - ' num2str(date(snd_en))]
desc=[num2str(plt_str) ' - ' num2str(plt_end)];
title([' T (deg C); ' desc ]);
axis([yd_stpl yd_enpl zb zt])

hold on
plot(jd,zbot,'r*')
hold off
  
%thetav

if pltthav==1;
%np=np+1;
figure(np)
v=[-30:3:60];
%v=[-14:2:30];
arr=transpose(thav(x1:x2,k1:k2))-273.15;
subplot(2,1,2),[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' Thav (deg C); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltthe==1
%thetae
np=np+1;
figure(np)
v=[-20:2:60];
%v=[-10:1:30];
arr=transpose(the(x1:x2,k1:k2))-273.15;
subplot(2,1,1),[C,h]=contourf(x,y,arr,v);clabel(C,h);colormap jet
xlabel(xlabl);
ylabel('Height (m)');
title([' THE (deg C); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltnsq==1
%N2
%np=np+1;
figure(np)
v=[-6:1:40];
arr=transpose(nsq(x1:x2,k1:k2-1)*1e4);
subplot(2,1,2),[C,h]=contourf(x,yri,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Brunt-Vaisala Frequency (x 10^-^4s^-^1); ' desc']);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltrhi==1
%relative humidity wrt ice
np=np+1;
figure(np)
v=[5:10:115];
arr=transpose(rhiint(x1:x2,k1:k2));
subplot(2,1,1),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' RH wrt ice (%); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltrhw==1
%relative humidity wrt water
%np=np+1;
figure(np)
v=[5:10:115];
arr=transpose(rhint(x1:x2,k1:k2));
subplot(2,1,2),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' RH wrt water (%); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltqv==1
%water vapor mixing ratio
np=np+1;
figure(np)
v=[0:0.3:9];
arr=transpose(qvint(x1:x2,k1:k2))*1000;
subplot(2,1,1),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Water Vapor Mixing Ratio (g/kg); ' desc ]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltws==1
%wind speed
%np=np+1;
figure(np)
%v=[0:2:40];
v=[0:3:60];
arr=transpose(wsint(x1:x2,k1:k2));
subplot(2,1,2),[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Wind Speed (m/s); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off

if pltbrb==1
   yscl=xscl*(zt-zb)/((t2-t1)*0.9);
hold on
[ynarr xnarr]=size(arr)
for i=1:brb_intx:xnarr
    xlab=x(i);
    iwd=x1+i-1;
    for j=1:brb_inty:ynarr
       ylab=y(j);
       flg=barb2(xlab,ylab,arr(j,i),wdint(iwd,j),xscl,yscl);
%  num_lab=num2str(round(the(n_10ma(i))));
%  text(xlab,ylab,num_lab)
    end
end
hold off
end

end

if pltwd==1
%wind direction
np=np+1;
figure(np)
%dwst=find(wdint>180);
%wdint(dwst)=wdint(dwst)-360;
wdint(find(wdint<-360))=NaN;
%v=[-180:30:180];
v=[0:30:360];
arr=transpose(wdint(x1:x2,k1:k2));
[C,h]=contourf(x,y,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Wind Direction (deg true); ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end

if pltri==1
%Ri
np=np+1;
figure(np)
v=[-1:.25:2];
arr=transpose(ri(x1:x2,k1:k2-1));
[C,h]=contourf(x,yri,arr,v);clabel(C,h);
xlabel(xlabl);
ylabel('Height (m)');
title([' Richardson Number; ' desc]);
axis([yd_stpl yd_enpl zb zt])
hold on
plot(jd,zbot,'r*')
hold off
end
end %if if_plot==2




end % if if_plot>0

sndgts_sav=0;
if sndgts_sav==1
    %save_fil=['C:\Users\opersson\Documents\ONRSeaState\analyses\SeaState_2015_prelimin_SEB_' num2str(dtim) 'min_2015_' chimo '_' chdy '_' num2str(jdin)];
%save_fil=['C:\Users\obper\Documents\MOSAiC\Analyses\MOSAiC_sndgs_mlh_' descmo];
%save_fil=['C:\Users\obper\Documents\MOSAiC\Analyses\MOSAiC_sndgs_mlh_' descmo];
save(save_fil,'jd','mlh');
end

plot_save=1;
if plot_save==1 & if_plot>0
    %plot_dir='C:\Users\obper\Documents\MOSAiC\Data\radiosondes\TH_sections_weekly'
    %plot_dir='C:\Users\obper\Documents\MOSAiC\Presentations\Journal_Articles\Atmos Overview'
    %plot_dir='D:\MOSAiC\Presentations\Journal_Articles\Atmos Overview'
    %plot_dir='D:\MOSAiC\Analyses\Cyclones\Jan 24_28'
    plot_dir='D:\MOSAiC\Analyses\Cyclones\Jan27_Feb4'
   % dycs=stdyrdt; mocs=stmordt; yrcs=styrrdt; jdstc=num2str(round(ydrdst));
   % dyce=endyrdt; moce=enmordt; yrce=enyrrdt; jdenc=num2str(round(ydrden));
    disp(['saving plots; YD: ' desc])
    cd(plot_dir)
    pltopc=num2str(plot_top/100);
    fignam1=['TH_T_isotach_mlh_' pltopc '_' descmo];
    fign1=np0+1;fign1c=['-f' num2str(fign1)];
    print(fign1c,fignam1,'-dpng')
    fignam2=['TS_T_winds_' descmo];
    fign2=np0+2;fign2c=['-f' num2str(fign2)];
    print(fign2c,fignam2,'-dpng')
    fignam3=['TH_thetav_mlh_' pltopc '_' descmo];
    fign3=np0+3;fign3c=['-f' num2str(fign3)];
    print(fign3c,fignam3,'-dpng')
    
    fignam4=['TH_thetae_' pltopc '_' descmo];
    fign4=np0+4;fign4c=['-f' num2str(fign4)];
    print(fign4c,fignam4,'-dpng')
    
    fignam5=['TH_RHw_' pltopc '_' descmo];
    fign5=np0+5;fign5c=['-f' num2str(fign5)];
    print(fign5c,fignam5,'-dpng')
    
    fignam6=['TH_RHi_' pltopc '_' descmo];
    fign6=np0+6;fign6c=['-f' num2str(fign6)];
    print(fign6c,fignam6,'-dpng')
    
    fignam7=['TH_mr_' pltopc '_' descmo];
    fign7=np0+7;fign7c=['-f' num2str(fign7)];
    print(fign7c,fignam7,'-dpng')
    
    fignam8=['TH_isotachs_barbs_' pltopc '_' descmo];
    fign8=np0+8;fign8c=['-f' num2str(fign8)];
    print(fign8c,fignam8,'-dpng')
    
    disp([' 8 plots saved to ' plot_dir]) 
  end %if plot_save

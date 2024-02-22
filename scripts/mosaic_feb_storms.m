%    mosaic_adcp.m
%
%     load merged data set and plot timeseries between sday and eday
%      For the Feb 1 MOSAiC event paper and others.....

buoyn = 46;
if buoyn == 46;buoy = 'CO';end

figoff = buoyn-43;     %   figure offset s for site comparisons

sday =  365+30 % 
eday =  400  
styear = 2019;
wkyear = 2020;

sbins = 2:32;        %   select ADCP depth bins
abins = [2 8 28 ];   %   select ADCP bins for timeseries
%bdepths = z(abins);

txtposx =+.03;txtposy =1.12;
setcolors     %  load typ_colors colarmap

gpath = 'G:\.shortcut-targets-by-id\1EGfeocGp11iqeSSuCMXDixJxlXXvF2D7\NPS Bill & Tim\';

%    Load CO Tower met data   including yyyyddd (yd overwritten below)
load ([gpath 'arctic_buoy\mlab_proc\ASFS\tower.mat'])
%     find met data between sday and eday
idxmet = find(ydunwrap(yyyyddd,styear) > sday & ydunwrap(yyyyddd,styear) <eday);
%wk = ydunwrap(ydunwrap(yyyyddd,styear));
ydselmet = yd_to_datenum(yyyyddd(idxmet)')';
yyyydddmet = yyyyddd;   

%   Load buoy mlab data structures:
load ([gpath 'arctic_buoy\mlab_proc\aofb\buoy' num2str(buoyn) '.mat'])
idxbuoy = find(ydunwrap(flux.yyyddd,styear) > sday & ydunwrap(flux.yyyddd,styear) <eday);
ydselbuoy = yd_to_datenum(flux.yyyddd(idxbuoy));
idxaltim = find(ydunwrap(altimeter.yyyddd,styear) > sday & ydunwrap(altimeter.yyyddd,styear) <eday);
ydselaltim = yd_to_datenum(altimeter.yyyddd(idxaltim));

%     Load comb mlab data including:
% yyyddd, yyyydddoc, N2,S, T, T-atm,pden, pos, ptmp,shear,u,u_atm,u_io, uw, uw_atm,uw_io,
% v, v_atm, vw_io, vw, vw_atm, vw_io, wake,yd to ydsel and idxoc  
load ([gpath 'arctic_buoy\mlab_proc\aofb\comb'  num2str(buoyn) '.mat'])
wk = pden;;pden = wk(:,:,1);clear wk
pden(4,:)=(pden(3,:)+pden(5,:))/2;
idxoc = find(yd > sday & yd <eday);
%    now form a yyyydddoc timeseries
nyr= fix(yd(end)/365);   %  number of years
yyyydddoc = ydwrap(styear,yd);
ydsel = yd_to_datenum(yyyydddoc(idxoc));    

pbinden = 1:32;
%  force pden above bin 10 (24m depth) to be monotonic
%  up............................
pdenfix = pden;
dend = .001;  % density deficit at the top bin when extrapolating
for ii = 1: length(idxoc)
    %   find first point from the 10th bin to have a negative slope upwards
    idxden = find(diff(pden(1:10,idxoc(ii)))<0);
    if length (idxden)>1
        % extrapolate up to surface with a small +ve slope...
        pdenfix(1:idxden(end)+1,idxoc(ii))= linspace(pden(idxden(end)+1,idxoc(ii))-dend,pden(idxden(end)+1,idxoc(ii)),idxden(end)+1);
    end
end

%   Calc MLD 
mldr = [];rbin = 4;    %    Reference surface density bin
dthr = .2;   %   sigma theta
wn = 0.1;    %  mld smoothing
[mld_p2] = mldcalc(pdenfix(:,idxoc),z,ydsel,rbin,dthr,wn);figure(96);plot(mld_p2,'.');hold on
dthr = .02;   %   sigma theta
[mld_p02] = mldcalc(pdenfix(:,idxoc),z,ydsel,rbin,dthr,-1);plot(mld_p02,'.g');hold on
[mld_p01] = mldcalc(pdenfix(:,idxoc),z,ydsel,rbin,.01,-1);plot(mld_p01,'.k');hold on


pbins = 2:32;
binsize = 2;    % m
spdlim = 0.25;

%   Calc ice speed and direction
 [gpsu, gpsv, gpsspeed] = ice_speed(pos(:,idxoc),yd(idxoc));

%  Calc departure from freezing
DF = T-swfreezetemp(S,-z);

%    Calc shear
curmag = sqrt(u(pbins,idxoc).^2 + v(pbins,idxoc).^2);
curdir = fangle(180/pi*(1.5*pi-atan2(v(pbins,idxoc),u(pbins,idxoc))));
vectv = u+i*v;
adcp_shear = abs((diff(vectv)))/binsize;
adcp_shear_u = abs((diff(u)))/binsize;
adcp_shear_v = abs((diff(v)))/binsize;

% Calc u* and HF and SF 
ustoc = (flux.uw_inst(idxbuoy).^2+flux.vw_inst(idxbuoy).^2).^.25;
cp = 3985;     %  specific heat of seawater
rho = nanmean(density(flux.S(idxbuoy),flux.T(idxbuoy),3*ones(size(flux.S(idxbuoy)))));
stressOC = rho*ustoc.^2;

%   Wind calcs
icedir = fangle(180/pi*(1.5*pi-atan2(gpsv,gpsu)));
windmag = sqrt(wspd_v_mean(idxmet).^2+wspd_u_mean(idxmet).^2);
idxwmag = find(windmag<5000);
winddir = fangle(180/pi*(1.5*pi-atan2(wspd_v_mean(idxmet),wspd_u_mean(idxmet))));
ustatmos = (wu_csp(idxmet).^2+ wv_csp(idxmet).^2  ).^.25;
rhoair = 1.204;
stressatmos = rhoair*ustatmos.^2;
idxatstress = find(stressatmos<100);
%   interpolate 
wspeedintp = interp1(ydselmet(idxwmag),windmag(idxwmag),ydsel);
ice_wind = gpsspeed./wspeedintp;idxiw = find(wspeedintp>1 );    %  avoid low ws values

figure(110);clf    %   Pcolor u/v profiles
h1 = subplot(3,1,1);pcolor(ydsel,z(pbins),v(pbins,idxoc))
shading interp;colorbar;ylabel('m');title ([buoy ' N/S absolute current (ms^{-1})']) 
ylabel('Depth (m)');caxis([-spdlim spdlim]);colorbar;pause(.1);ylim([-70 0])
pause(.1)
datetick('x',2);set(h1,'XMinorTick','on');set(h1,'Tickdir','out')%;axis tight
text(txtposx,txtposy,'a','units','normalized')    %  label panel
hold on;plot(ydsel,mld_p2,'r','linewidth',2)
pause(.1)

h2=subplot(3,1,2);pcolor(ydsel,z(pbins),u(pbins,idxoc))
shading interp;colorbar;ylabel('m');title ('E/W absolute current (ms^{-1})')
ylabel('Depth (m)');caxis([-spdlim spdlim]);colorbar;ylim([-70 0])
pause(.1);datetick('x',2);set(h2,'XMinorTick','on');set(h2,'Tickdir','out')%;axis tight
text(txtposx,txtposy,'b','units','normalized')    %  label panel
hold on;plot(ydsel,mld_p2,'r','linewidth',2)
%%sbins=pbins(2:length(pbins)-1);

h3=subplot(3,1,3);pcolor(ydsel,z(sbins)-binsize/2,adcp_shear_v(sbins,idxoc));
shading interp;colorbar;ylabel('m');title (['N/S current shear (s^{-1})'])
ylabel('Depth (m)');colorbar ;ylim([-70 0]);caxis([0 .04])
% hold on;plot([398.221 398.805],[-23.64 -33.64],'r','linewidth',3)
% plot([399.096 399.305 399.846 400.263],[-35.5 -21 -19 -42],'y','linewidth',3)
pause(.1)
datetick('x',2);set(h3,'XMinorTick','on');set(h3,'Tickdir','out');%;axis tight
%      add entrainment slope and eddy feature
%h3=drawline('Position',[398.221,398.805;-23.64 -33.64],'Selectedcolor','red');
text(txtposx,txtposy,'c','units','normalized')    %  label panel
%  add mld
hold on;plot(ydsel,mld_p2,'r','linewidth',2)
plot(ydsel,mld_p01,'*r');plot(ydsel,mld_p01,'or')

figuresize([.5 .5 7 10])
    %%opfil = 'Y:\Tim\arcticmon\Mosaic\Publications\Feb_2020_event\u_v_shear_den';
    opfil = 'D:\y disk\Tim\arcticmon\Mosaic\Publications\Feb_2020_event\fig16_u_v_shear_den';
    print (opfil,'-dpng') 

figure(120);clf   %   Plot mag / direction adcp, ice and atmosphere

h1=subplot(5,1,1);hh(3)=plot(ydsel, curmag(abins(1),:),'b','linewidth',2);hold on;
hh(4)=plot(ydsel, curmag(abins(2),:),'color',typ_color(8,:),'linewidth',2);
hh(5)=plot(ydsel, curmag(abins(3),:),'color',typ_color(1,:),'linewidth',2);
hh(2)=plot(ydsel, gpsspeed,'k','linewidth',2);ylabel('m s^{-1}');
yyaxis right; hh(1)=plot(ydselmet,windmag,'r','linewidth',2);ylabel('wind m s^{-1}')
ax=gca;ax.YAxis(2).Color ='r';
title([buoy ' Speeds'])
s1 = [' Windspeed ','color','r'];s2 = ['ice speed ','color','k'];s3 = ['5m ','color','b'];
lgd = legend(hh,'Windspeed','Ice speed','8m current','20m curremt','60m current','Location','NorthEast','numcolumns',2,'box','off');
ylabel('Wind m s^{-1}','color','r')%;ylim([0 1])
datetick('x',2);set(h1,'XMinorTick','on');%%set(h1,'Tickdir','out')%;axis tight
text(txtposx,txtposy,'a','units','normalized')    %  label panel

h2 = subplot(5,1,2);
plot(ydsel, curdir(1,:),'b','linewidth',2);hold on  ;plot(ydsel, curdir(2,:),'color',typ_color(8,:),'linewidth',2)
plot(ydsel, curdir(3,:),'color',typ_color(1,:),'linewidth',2)
plot(ydsel, icedir,'k','linewidth',2);ylabel('degrees true')
plot(ydselmet,winddir,'r','linewidth',2)
title(['Directions'])
ylabel('degrees true');
datetick('x',2);set(h2,'XMinorTick','on');%%set(h2,'Tickdir','out')
text(txtposx,txtposy,'b','units','normalized')    %  label panel

h3 = subplot(5,1,3);plot(ydsel,u(abins(1),idxoc),'b','linewidth',2);hold on
plot(ydsel,u(abins(2),idxoc),'color',typ_color(8,:),'linewidth',2)
plot(ydsel,u(abins(3),idxoc),'color',typ_color(1,:),'linewidth',2)
plot([ydsel(1) ydsel(end)],[0 0 ],'k')
title (['E/W absolute currents ']);xlabel('Day of year 2020');ylabel('m s^{-1}')
datetick('x',2);set(h3,'XMinorTick','on') %;axis tight
text(txtposx,txtposy,'c','units','normalized')    %  label panel

h4 = subplot(5,1,4);plot(ydsel,v(abins(1),idxoc),'b','linewidth',2);hold on
plot(ydsel,v(abins(2),idxoc),'color',typ_color(8,:),'linewidth',2)
plot(ydsel,v(abins(3),idxoc),'color',typ_color(1,:),'linewidth',2);
plot([ydsel(1) ydsel(end)],[0 0 ],'k')
title (['N/S absolute currents' ]);xlabel('Day of year 2020');ylabel('m s^{-1}')
datetick('x',2);set(h4,'XMinorTick','on') %;axis tight
text(txtposx,txtposy,'d','units','normalized')    %  label panel

h5 = subplot(5,1,5);plot(ydselmet(idxatstress),ustatmos(idxatstress),'.r','markersize',3);hold on
plot(ydselbuoy, stressOC,'.b','markersize',8)
title(['Atmosphere - Ocean stress'])
ylabel('N m^{-2}');datetick('x',2);set(h5,'XMinorTick','on')%%;set(h5,'Tickdir','out');axis tight
text(txtposx,txtposy,'e','units','normalized')    %  label panel
lgd5= legend('6m height atmosphere stress','5m depth ocean stress','box','off');

figuresize([.5 .5 7 10])
%%    opfil = 'D:\y disk\Tim\arcticmon\Mosaic\Publications\Feb_2020_event\fig15_WS_IS_currents';
%%    print (opfil,'-djpeg100') 


figure(130+figoff);clf  %   Plot u* stress HF SF
wn = .1;    %  lp filt fraction of Nyquist for 2 hour sampling

h1=subplot(2,1,1);plot(ydselbuoy, ustoc,'b');ylabel('ms^{-1}');%ylim([0 0.5])
hold on;plot(ydselbuoy, ustoc,'.b');axis tight
%%yyaxis right;plot(ydsel(idxiw),ice_wind(idxiw))
%title([buoy ' u* at 4m (b)  ice speed / wind speed  ratio (r)'])
title([buoy ' u* at 4m (b) '])

datetick('x',2);set(h1,'XMinorTick','on');set(h1,'Tickdir','out');axis tight
text(txtposx,txtposy,'a','units','normalized')    %  label panel

h2 = subplot(2,1,2);plot(ydselbuoy, stressOC,'.b','markersize',4);hold on
plot(ydselmet(idxatstress),ustatmos(idxatstress),'.r','markersize',3)
title(['4m ocean stress (b)   6m atmospheric stress (r)'])
ylabel('Nm^{-2}');datetick('x',2);set(h1,'XMinorTick','on');set(h2,'Tickdir','out');axis tight
text(txtposx,txtposy,'b','units','normalized')    %  label panel

%%opfil = 'Y:\Tim\arcticmon\Mosaic\Publications\Feb_2020_event\ust_stress';
%%print (opfil,'-djpeg100') 




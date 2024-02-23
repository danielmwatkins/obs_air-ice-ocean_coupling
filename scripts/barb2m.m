      function bend=barb2m(X, Y, WS, WD, xscl,yscl)

%      Common /Colors/ Idf, Ibarbc, Itmec

%     Plot a wind barb at (x,y)

      FLAG=25.; BAR=5.0; HBAR=2.5; ex=0;

      HFBAR = HBAR / 2.0;
      DIF = FLAG - HFBAR;
      DIF1 = BAR - HFBAR;
      IHBAR = HFBAR*10.0 + 0.5;
      IDIF1 = DIF1*10.0 + 0.5;

%     Call Frstd (X,Y)-moves pen to first point

%     Good wind to plot?
      bend=0;
      if WS >= HFBAR
        if WS < 300.0 & WD <= 360.0  & WD >= 0.0
          ex=0.;
          SWITCH = 0.;
          REMA = mod(WS,FLAG);
          IJ = (WS-REMA)/FLAG;%number of flags
          if REMA >= DIF 
            IJ = IJ + 1;
            SWITCH = 1.;
          end
          I = floor(REMA/BAR);
          IREM = mod(REMA,BAR)*10.0 + 0.5;
          if IREM >= IDIF1
            I=I+1;
          end
          if IREM < IHBAR | IREM >= IDIF1 
            C       = 1.;
          else
            C       = .5;
            I       = I + 1;
            if I==1
               ex=1;
            end
          end
          
          ALF     =  mod(450. - WD,360.);
          ALFA1   = cos(ALF/57.295);
          ALFA2   = sin(ALF/57.295);
          BET     =  mod(ALF + 280.,360.);
          BETA1   = cos(BET/57.295);
          BETA2   = sin(BET/57.295);
          HK      = .50;
          X1      = X;
          Y1      = Y;
         
          if IJ <= 0 | (REMA >= (HFBAR-.05) &  SWITCH ==0.)
            for K = 1:I
             X2      = X1 + HK*xscl*ALFA1;
             Y2      = Y1 + HK*yscl*ALFA2;
             x=[X1 X2];y=[Y1 Y2];
             plotm(y,x,'k-')
             X3      = X2 + C*.5*xscl*BETA1;
             Y3      = Y2 + C*.5*yscl*BETA2;
             x=[X2 X3];y=[Y2 Y3];
             plotm(y,x,'k-')
    %         Call Vectd (X3, Y3)
    %         Call Vectd (X2, Y2)
             HK   = .15;
             X1      = X2;
             Y1      = Y2;
             C       = 1.;
           end 
           if ex == 1
             X2      = X1 + HK*xscl*ALFA1;
             Y2      = Y1 + HK*yscl*ALFA2;
             x=[X1 X2];y=[Y1 Y2];
             plotm(y,x,'k-')
           end 
         end
         if IJ ~= 0;
            GAM=mod(ALF + 300.,360.);
            GAM1 = cos(GAM/57.295)*.5*xscl;
            GAM2 = sin(GAM/57.295)*.5*yscl;
            for K = 1:IJ
              X2 = X1 + HK*xscl*ALFA1;
              Y2 = Y1 + HK*yscl*ALFA2;
              x=[X1 X2];y=[Y1 Y2];
              plotm(y,x,'k-')
%             Call Vectd (X2, Y2)
              X3 = X2 + GAM1;
              Y3 = Y2 + GAM2;
              x=[X2 X3];y=[Y2 Y3];
              plotm(y,x,'k-')
%             Call Vectd (X3, Y3);
%             Call Vectd (X2, Y2);
              X1 = X2 + .25*xscl*ALFA1;
              Y1 = Y2 + .25*yscl*ALFA2;
              x=[X2 X1];y=[Y2 Y1];
              plotm(y,x,'k-')
              x=[X1 X3];y=[Y1 Y3];
              plotm(y,x,'k-')
%             Call Vectd (X1, Y1)
%             Call Vectd (X3, Y3)
%             Call Vectd (X1, Y1)
              HK      = 0.;
            end
          end
        end
      
 %      Call Frstd (X, Y)
 %       Call Sflush
 %       Call GSPLCI(Idf)       ! Default
        bend=1;
      end
     

%
%read_sacr_ppi
%
clear all

moddystr=[1 32 60 91 121 152 182 213 244 274 305 335];
moddystrl=[1 32 61 92 122 153 183 214 245 275 306 336];
noise_vs_range=[-24.3772  -22.9708  -23.1874  -23.3284  -23.5411  -23.8149  -24.1233  -24.3480  -24.4437  -24.6723  -24.9050  -25.0246  -25.0884  -25.2586  -25.5510...
  -25.6082  -25.7139  -25.8681  -25.9817  -26.3420  -26.7049  -27.2207  -27.4400  -27.7365  -28.0462  -28.1353  -28.0755  -28.0356  -28.0675  -28.0103...
-28.1818  -28.4184  -28.4111  -28.4430  -28.5009  -28.6444  -28.7362  -28.9522  -29.0964  -29.2865  -29.5152  -29.6129  -29.6800  -29.4872  -29.4653...
 -29.6733  -29.4939  -29.4992  -29.6760  -29.9485  -29.9405  -30.0735  -30.1825  -30.4258  -30.5201  -30.5733  -30.6438  -30.6544  -30.6531  -30.5600...
  -30.6079  -30.7129  -30.8937  -31.0991  -31.1742  -31.0572  -31.0153  -30.9489  -30.9841  -30.7528  -30.6385  -30.7461  -30.8465  -30.7834  -30.8963...
 -31.0346  -30.9189  -31.1622  -31.0665  -31.0253  -31.1037  -31.2247  -31.1137  -31.2539  -31.4168  -31.3590  -31.2898  -31.4706  -31.6022  -31.8960...
-31.8395  -31.7737  -31.8249  -31.7950  -31.8229  -31.8880  -31.7711  -31.7385  -31.6594  -31.5790  -31.5158  -31.6434  -31.6953  -31.7126  -31.5783...
-31.4866  -31.2932  -31.2719  -31.2473  -31.0778  -31.2181  -31.2300  -31.2938  -31.3829  -31.3231  -31.3855  -31.4015  -31.4128  -31.2712  -31.2493...
-31.3231  -31.3051  -31.2672  -31.2028  -31.1835  -31.2061  -31.2041  -31.1562  -31.0884  -31.2553  -31.2141  -31.0984  -31.1130  -31.1542  -31.1669...
-31.0851  -30.9947  -30.9854  -31.1037  -31.0785  -30.8831  -30.9083  -30.8671  -30.8498  -30.8850  -30.7275  -30.7209  -30.7222  -30.6797  -30.6411...
-30.7169  -30.5999  -30.6823  -30.7288  -30.6876  -30.5746  -30.5879  -30.5095  -30.5560  -30.4842  -30.6026  -30.5760  -30.4656  -30.3952  -30.4351...
-30.5029  -30.5866  -30.4617  -30.4769  -30.2928  -30.2171  -30.2649  -30.3148  -30.3360  -30.1978  -30.1905  -30.0788  -30.0456  -30.0801  -30.0283...
-30.0502  -30.0456  -29.9286  -29.9166  -29.9977  -30.0004  -29.7970  -29.8501  -29.8488  -29.7970  -29.7146  -29.5617  -29.6840  -29.6999  -29.6827...
-29.5497  -29.5191  -29.5796  -29.5045  -29.4793  -29.4487  -29.4194  -29.3078  -29.2772  -29.1908  -29.2473  -29.3211  -29.2214  -29.1669  -29.2187...
-29.1257  -29.0499  -29.1363  -29.0924  -29.0579  -29.1177  -29.0419  -28.9834  -28.8531  -28.9196  -28.8930  -28.7694  -28.7481  -28.8598  -28.7368...
 -28.6232  -28.7215  -28.6830  -28.6803  -28.5580  -28.5740  -28.6365  -28.6205  -28.5859  -28.4769  -28.4530  -28.4085  -28.3493  -28.3573  -28.3480...
-28.2855  -28.3852  -28.3440  -28.3241  -28.2722  -28.2602  -28.2111  -28.2283  -28.2018  -28.0675  -27.9930  -28.2230  -28.1147  -27.9877  -28.0369...
-27.9319  -27.9718  -27.9405  -27.8874  -27.8521  -27.8867  -27.7863  -27.7192  -27.7657  -27.8109  -27.7671  -27.7272  -27.6833  -27.7498  -27.6049...
-27.6687  -27.6089  -27.6527  -27.5996  -27.5318  -27.5451  -27.5796  -27.4427  -27.5849  -27.5025  -27.4719  -27.5191  -27.4706  -27.4547  -27.3669...
-27.3895  -27.3550  -27.3550  -27.3496  -27.3005  -27.2420  -27.2313  -27.2220  -27.2353  -27.2273  -27.1117  -27.1210  -27.1276  -27.0824  -26.9827...
 -26.9774  -27.0027  -27.0346  -26.9827  -26.9761  -26.9083  -26.9136  -26.9056  -26.9096  -26.8139  -26.8551  -26.8418  -26.7435  -26.7554  -26.7421...
-26.7421  -26.6690  -26.6783  -26.6477  -26.6743  -26.6225  -26.6677  -26.5640  -26.5454  -26.5321  -26.5746  -26.4856  -26.5161  -26.4164  -26.4231...
-26.3673  -26.3992  -26.3992  -26.2769  -26.2955  -26.3606  -26.2622  -26.2543  -26.2303  -26.2184  -26.1426  -26.2237  -26.0961  -26.1213  -26.1107...
 -26.0628  -26.0389  -26.0283  -26.0243  -25.9671  -25.9724  -25.9379  -25.8714  -25.9060  -25.8209  -25.8648  -25.8302  -25.7637  -25.8262  -25.7438...
-25.6880  -25.7172  -25.6959  -25.6786  -25.6361  -25.6321  -25.6241  -25.5457  -25.5364  -25.5298  -25.4726  -25.5151  -25.4925  -25.4925  -25.4925...
-25.3968  -25.4128  -25.4394  -25.4753  -25.3277  -25.3250  -25.3476  -25.2426  -25.2533  -25.2360  -25.2346  -25.1974  -25.1655  -25.0685  -25.0671...
-25.0406  -25.0313  -25.0685  -25.0485  -25.0273  -25.0432  -24.9861  -24.9329  -24.8212  -24.8996  -24.8877  -24.8850  -24.9023  -24.8225  -24.9090...
-24.8319  -24.8505  -24.7521  -24.7827  -24.7069  -24.6949  -24.6311  -24.6856  -24.5660  -24.5128  -24.5487  -24.6059  -24.5779  -24.5248  -24.5035...
-24.5434  -24.4437  -24.4277  -24.4942  -24.4344  -24.3626  -24.3599  -24.3453  -24.3466  -24.2775  -24.2283  -24.3347  -24.3068  -24.1911  -24.2376...
-24.1978  -24.1898  -24.1991  -24.1978  -24.1060  -24.1140  -24.0568  -24.1074  -24.0994  -24.0728  -24.0236  -23.9664  -23.9638  -23.9252  -23.9877...
-23.9266  -23.8907  -23.9532  -23.8827  -23.9345  -23.8681  -23.8747  -23.8362  -23.8189  -23.7790  -23.7777  -23.7963  -23.7777  -23.7684  -23.6873...
-23.6235  -23.6713  -23.5597  -23.5783  -23.6128  -23.6128  -23.6049  -23.5823  -23.5637  -23.5956  -23.5145  -23.4081  -23.5171  -23.4360  -23.3829...
-23.4188  -23.4001  -23.3523  -23.3975  -23.3709  -23.3177  -23.2898  -23.2313  -23.2752  -23.2366  -23.2965  -23.2340  -23.1968  -23.1715  -23.2207...
-23.1688  -23.0891  -23.1728  -23.1276  -23.1130  -23.0585  -23.0838  -23.0532  -23.0346  -23.0372  -22.9894  -22.9415  -22.9136  -22.9362  -22.9309...
-22.9083  -22.8724  -22.8365  -22.8697  -22.8378  -22.8285  -22.8405  -22.7966  -22.8671  -22.7461  -22.7727  -22.7208  -22.7022  -22.7395  -22.6850...
 -22.7262  -22.7089  -22.7448  -22.6517  -22.5228  -22.6078  -22.6198  -22.5480  -22.5627  -22.5799  -22.6225  -22.5627  -22.5866  -22.5042  -22.4470...
-22.5268  -22.5161  -22.4390  -22.4151  -22.4310  -22.4324  -22.3513  -22.3912  -22.3792  -22.4058  -22.4297  -22.3313  -22.3141  -22.3327  -22.2808...
-22.2396  -22.2170  -22.2503  -22.2915  -22.2423  -22.2303  -22.2157  -22.1519  -22.1120  -22.1904  -22.1971  -22.1306  -22.0854  -22.0721  -22.1638...
-22.0110  -22.0376  -22.0283  -22.0362  -21.9963  -22.0402  -22.0336  -22.0243  -21.9658  -21.9312  -21.9605  -21.8847  -21.8475  -21.8528  -21.9006...
-21.8528  -21.8634  -21.8900  -21.8834  -21.8395  -21.8328  -21.7757  -21.7930  -21.7717  -21.7105  -21.6999  -21.6986  -21.7757  -21.6667  -21.6374...
 -21.6746  -21.6707  -21.6587  -21.6228  -21.6241  -21.5763  -21.5497  -21.5922  -21.5736  -21.5337  -21.5391  -21.5377  -21.4845  -21.4261  -21.3968...
 -21.3609  -21.3689  -21.4088  -21.4646  -21.3649  -21.4513  -21.4261  -21.3476  -21.3224  -21.3436  -21.3476  -21.3264  -21.2798  -21.3038  -21.2466...
 -21.2652  -21.2546  -21.2493  -21.1722  -21.1908  -21.1708  -21.2067  -21.1974  -21.0871  -21.1230  -21.0911  -21.1057  -21.0379  -21.0658  -21.0818...
 -21.0472  -21.0432  -21.0871  -20.9914  -21.0472  -20.9887  -20.9834  -20.9980  -21.0007  -20.9369  -20.9767  -20.9196  -20.9169  -20.8810  -20.9182...
 -20.9023  -20.8730  -20.8398  -20.7959  -20.8305  -20.8358  -20.7308  -20.7999  -20.7468  -20.7494  -20.7614  -20.7547  -20.6989  -20.7188  -20.6457...
 -20.6457  -20.6710  -20.6869  -20.6165  -20.6976  -20.6830  -20.6245  -20.5779  -20.5766  -20.5327  -20.5168  -20.5181  -20.5753  -20.5088  -20.4862...
-20.5327  -20.4477  -20.3878  -20.4463  -20.4556  -20.5287  -20.4676  -20.4118  -20.3772  -20.4118  -20.4078  -20.3360  -20.3293  -20.3280  -20.3373...
 -20.3028  -20.3493  -20.2815  -20.1911  -20.2376  -20.2443  -20.2576  -20.1672  -20.2310  -20.1898  -20.2496  -20.2416  -20.1419  -20.1432  -20.1844...
-20.1512  -20.1406  -20.1180  -20.1326  -20.1047  -20.1060  -20.0701  -20.0156  -20.0316  -20.0781  -19.9438  -19.9717  -19.9558  -19.9079  -19.9598...
-20.0050  -19.9345  -19.9505  -19.9172  -19.9066  -19.8534  -19.9345  -19.8946  -19.8601  -19.8441  -19.7856  -19.8893  -19.8295  -19.8973  -19.7936...
 -19.7365  -19.8136  -19.7657  -19.7657  -19.7497  -19.7537  -19.6687  -19.7391  -19.6966  -19.7085  -19.6952  -19.6381  -19.6447  -19.6274  -19.6540...
-19.5676  -19.6168  -19.5690  -19.5557  -19.5530  -19.6328  -19.5809  -19.5464  -19.5424  -19.5251  -19.5690  -19.5809  -19.4599  -19.4639  -19.4759...
-19.4852  -19.4400  -19.5384  -19.4174  -19.3855  -19.3004  -19.3975  -19.3988  -19.3523  -19.3682  -19.3137  -19.3709  -19.3137  -19.3097  -19.3057...
-19.2526  -19.3616  -19.2619  -19.2685  -19.2552  -19.2526  -19.2353  -19.1356  -19.1569  -19.1515  -19.1954  -19.1702  -19.1502  -19.1941  -19.1289...
-19.1781  -19.1289  -19.1250  -19.1289  -19.0984  -19.1196  -19.0532  -19.0665  -19.0439  -19.0665  -19.1090  -19.0545  -19.0253  -19.0066  -18.9641...
-19.0093  -18.9561  -18.9362  -18.9947  -18.9455  -18.9255  -18.9242  -18.9016  -18.8883  -18.8551  -18.8578  -18.8697  -18.8764  -18.8591  -18.8804...
-18.8724  -18.7833  -18.7753  -18.8205  -18.8219  -18.8152  -18.8165  -18.7102  -18.7674  -18.7873  -18.7049  -18.7966  -18.6996  -18.7394  -18.6517...
-18.7035  -18.6663  -18.6663  -18.6477  -18.6291  -18.6770  -18.6716  -18.5999  -18.6490  -18.5719  -18.6012  -18.5706  -18.5826  -18.5733  -18.5427...
-18.5666  -18.5999  -18.4988  -18.4324  -18.4829  -18.4789  -18.4616  -18.4709  -18.4058  -18.4417  -18.4855  -18.4297  -18.4257  -18.4550  -18.4324...
-18.3991  -18.4244  -18.3885  -18.3380  -18.3526  -18.3220  -18.4111  -18.3061  -18.3592  -18.3300  -18.3127  -18.2476  -18.3047  -18.3420  -18.2050...
-18.2702  -18.1745  -18.1917  -18.1904  -18.1811  -18.1917  -18.1452  -18.1240  -18.1824  -18.1625  -18.1492  -18.1399  -18.1173  -18.1625  -18.1319...
-18.0734  -18.0881  -18.0721  -18.0708  -18.0229  -18.0189  -18.0894  -18.0442  -18.0615  -18.0814  -18.0615  -18.0282  -17.9990  -17.9179  -18.0495...
 -18.0282  -17.9498  -17.9538  -17.9884  -17.9764  -17.8887  -17.9245  -17.9392  -17.8328  -17.8687  -17.8528  -17.8727  -17.8754  -17.8381  -17.8381...
 -17.7943  -17.7929  -17.7903  -17.8009  -17.8129  -17.7743  -17.7783  -17.7903  -17.6946  -17.7451  -17.7384  -17.7305  -17.6560  -17.6693  -17.7172...
-17.6547  -17.7145  -17.6480  -17.7012  -17.6813  -17.6573  -17.6308  -17.6547  -17.5949  -17.6015  -17.5935  -17.6560  -17.6281  -17.5736  -17.5935...
-17.5563  -17.5324  -17.5350  -17.540];


azrng=[1:1:360];naz=length(azrng);
radar_data_dir='D:\MOSAiC\Data\ARM_radars\SACR_files\' ;
%radar_data_dir='F:\MOSAiC_data\ARM_radars\KaSACR\' ;
%tower_data_dir='F:\MOSAiC_data\tower\processed_data\level2\test_Jan27\'
tower_data_dir='F:\MOSAiC_data\tower\processed_data\level2\finalqc\'
%dir_wxdata='H:\MOSAiC\Data\Polarstern_metdata\';
dir_wxdata='F:\HomeOffice_Desktop\MOSAiC\Data\Polarstern_metdata\';
PS_wxdat_file=[dir_wxdata 'PS_metdata_263_640'];%Sep20_2019-Oct1_2020
%asfs30_data_dir='F:\MOSAiC_data\AF_Stations\asfs30\Processed_files\Level2\test\'
%asfs40_data_dir='F:\MOSAiC_data\AF_Stations\asfs40\Processed_files\Level2\test\'
%asfs50_data_dir='F:\MOSAiC_data\AF_Stations\asfs50\Processed_files\Level2\test\'
asfs30_data_dir='F:\MOSAiC_data\AF_Stations\Processed_ASFS_data\asfs30\2_level_product_asfs30\version2\finalqc\'
asfs40_data_dir='F:\MOSAiC_data\AF_Stations\Processed_ASFS_data\asfs40\2_level_product_asfs40\version2\finalqc\'
asfs50_data_dir='F:\MOSAiC_data\AF_Stations\Processed_ASFS_data\asfs50\2_level_product_asfs50\version2\finalqc\'
%data_vers='level2v2';
data_vers='level2.4';
data_avg='10min';
refl_calib=18;%estimated reflectivity error based on ARM estimates, June 2021 (dBz)

%
% edit these depending on whether out put iamges to be saved
% 
save_rad_out=1;
if save_rad_out==1
  %output_dir_refl='D:\MOSAiC\Analyses\Cyclones\Jan27_Feb4\SACR_refl\'
  output_dir_refl='D:\MOSAiC\Analyses\KA-SACR PPIs\reflectivity\'
  %output_dir_vel='D:\MOSAiC\Analyses\Cyclones\Jan27_Feb4\SACR_rvel\'
  output_dir_vel='D:\MOSAiC\Analyses\KA-SACR PPIs\radial velocity\'
end

%edit these to determine of reflectivity & Doppler velocity is edited
sn_thresh=-10;%signal-to-noise threshold used for removing noise in reflectivity data; abs must be < 11; if = -999, use reflectivity thresholding
sn_thresh_vel=-10;%signal-to-noise threshold used for removing noise in velocity data; abs must be < 11; if = -999, use reflectivity thresholding
ref_edit_offset=2; %additional reflectivity threshold offset - only if sn_thresh=-999

%yri='2019';moi='10';dyi='11';timi='081738';nfig=1;
%yri='2019';moi='10';dyi='20';timi='082537';nfig=1;
%yri='2019';moi='10';dyi='31';timi='233803';nfig=1;

%yri='2019';moi='11';dyi='18';timi='151856';nfig=1;
%yri='2019';moi='11';dyi='18';timi='153041';nfig=1;
%yri='2019';moi='11';dyi='18';timi='154225';nfig=1;

%yri='2019';moi='12';dyi='20';timi='002003';nfig=1;
%yri='2019';moi='12';dyi='21';timi='154743';nfig=1;
%yri='2019';moi='12';dyi='21';timi='210347';nfig=1;
%yri='2019';moi='12';dyi='22';timi='003358';nfig=1;
%yri='2019';moi='12';dyi='22';timi='030552';nfig=1;
%yri='2019';moi='12';dyi='22';timi='060108';nfig=1;
%yri='2019';moi='12';dyi='22';timi='073439';nfig=1;
%yri='2019';moi='12';dyi='22';timi='085631';nfig=1;
%yri='2019';moi='12';dyi='22';timi='110508';nfig=1;
%yri='2019';moi='12';dyi='22';timi='122701';nfig=1;
%yri='2019';moi='12';dyi='22';timi='180542';nfig=1;

yri='2019';moi='12';dyi='26';timi='224335';nfig=1;
%yri='2019';moi='12';dyi='26';timi='225515';nfig=1;
yri='2019';moi='12';dyi='26';timi='234158';nfig=1;
yri='2019';moi='12';dyi='26';timi='235338';nfig=1;
%yri='2019';moi='12';dyi='27';timi='000519';nfig=1;c
%yri='2019';moi='12';dyi='27';timi='001700';nfig=1;
%yri='2019';moi='12';dyi='27';timi='002842';nfig=1;
yri='2019';moi='12';dyi='27';timi='004023';nfig=1;
yri='2019';moi='12';dyi='27';timi='005203';nfig=1;
%yri='2019';moi='12';dyi='27';timi='010344';nfig=1;
yri='2019';moi='12';dyi='27';timi='011525';nfig=1;
yri='2019';moi='12';dyi='27';timi='012706';nfig=1;
yri='2019';moi='12';dyi='27';timi='013847';nfig=1;
yri='2019';moi='12';dyi='27';timi='015028';nfig=1;
yri='2019';moi='12';dyi='27';timi='020208';nfig=1;
yri='2019';moi='12';dyi='27';timi='021349';nfig=1;
yri='2019';moi='12';dyi='27';timi='022530';nfig=1;
yri='2019';moi='12';dyi='27';timi='023711';nfig=1;
yri='2019';moi='12';dyi='27';timi='024852';nfig=1;
yri='2019';moi='12';dyi='27';timi='030032';nfig=1;
yri='2019';moi='12';dyi='27';timi='033532';nfig=1;
yri='2019';moi='12';dyi='27';timi='035854';nfig=1;
yri='2019';moi='12';dyi='27';timi='041034';nfig=1;
yri='2019';moi='12';dyi='27';timi='043355';nfig=1;

%yri='2020';moi='01';dyi='08';timi='101835';nfig=1;
%yri='2020';moi='01';dyi='08';timi='103017';nfig=1;
%yri='2020';moi='01';dyi='08';timi='104159';nfig=1;c
%yri='2020';moi='01';dyi='08';timi='105342';nfig=1;
%yri='2020';moi='01';dyi='08';timi='110524';nfig=1;c
%yri='2020';moi='01';dyi='08';timi='111707';nfig=1;
%yri='2020';moi='01';dyi='08';timi='121348';nfig=1;
%yri='2020';moi='01';dyi='08';timi='122534';nfig=1;
%yri='2020';moi='01';dyi='08';timi='123719';nfig=1;
%yri='2020';moi='01';dyi='08';timi='124902';nfig=1;
%yri='2020';moi='01';dyi='08';timi='130044';nfig=1;
%yri='2020';moi='01';dyi='08';timi='131227';nfig=1;
%yri='2020';moi='01';dyi='08';timi='180522';nfig=1;
%yri='2020';moi='01';dyi='08';timi='201410';nfig=1;

yri='2020';moi='01';dyi='31';timi='042811';nfig=1;
yri='2020';moi='01';dyi='31';timi='045138';nfig=1;
yri='2020';moi='01';dyi='31';timi='051506';nfig=1;
yri='2020';moi='01';dyi='31';timi='053835';nfig=1;
yri='2020';moi='01';dyi='31';timi='055020';nfig=1;
yri='2020';moi='01';dyi='31';timi='060205';nfig=1;
%yri='2020';moi='01';dyi='31';timi='061349';nfig=1;
%yri='2020';moi='01';dyi='31';timi='062533';nfig=1;
%yri='2020';moi='01';dyi='31';timi='063718';nfig=1;
%yri='2020';moi='01';dyi='31';timi='064903';nfig=1;
%yri='2020';moi='01';dyi='31';timi='070047';nfig=1;
%yri='2020';moi='01';dyi='31';timi='071232';nfig=1;
%yri='2020';moi='01';dyi='31';timi='072416';nfig=1;
yri='2020';moi='01';dyi='31';timi='073600';nfig=1;
yri='2020';moi='01';dyi='31';timi='074744';nfig=1;
yri='2020';moi='01';dyi='31';timi='075929';nfig=1;
yri='2020';moi='01';dyi='31';timi='081113';nfig=1;
yri='2020';moi='01';dyi='31';timi='082258';nfig=1;
yri='2020';moi='01';dyi='31';timi='083442';nfig=1;
yri='2020';moi='01';dyi='31';timi='140336';nfig=1;
%yri='2020';moi='01';dyi='31';timi='141520';nfig=1;
%yri='2020';moi='01';dyi='31';timi='142705';nfig=1;
%yri='2020';moi='01';dyi='31';timi='145032';nfig=1;
%yri='2020';moi='01';dyi='31';timi='150215';nfig=1;
%yri='2020';moi='01';dyi='31';timi='151358';nfig=1;
%yri='2020';moi='01';dyi='31';timi='153724';nfig=1;
yri='2020';moi='01';dyi='31';timi='154908';nfig=1;
%yri='2020';moi='01';dyi='31';timi='160049';nfig=1;
yri='2020';moi='01';dyi='31';timi='164550';nfig=1;
%yri='2020';moi='01';dyi='31';timi='165734';nfig=1;
%yri='2020';moi='01';dyi='31';timi='170915';nfig=1;
yri='2020';moi='01';dyi='31';timi='172054';nfig=1;
%yri='2020';moi='01';dyi='31';timi='220044';nfig=1;
%yri='2020';moi='01';dyi='31';timi='221222';nfig=1;
%yri='2020';moi='01';dyi='31';timi='222404';nfig=1;
%yri='2020';moi='01';dyi='31';timi='223542';nfig=1;
%yri='2020';moi='01';dyi='31';timi='224724';nfig=1;
%yri='2020';moi='01';dyi='31';timi='225904';nfig=1;
%yri='2020';moi='01';dyi='31';timi='231044';nfig=1;
%yri='2020';moi='01';dyi='31';timi='232226';nfig=1;
%yri='2020';moi='01';dyi='31';timi='233407';nfig=1;
%yri='2020';moi='01';dyi='31';timi='234547';nfig=1;
%yri='2020';moi='01';dyi='31';timi='235729';nfig=1;
%yri='2020';moi='02';dyi='01';timi='000000';nfig=1c;
%yri='2020';moi='02';dyi='01';timi='000911';nfig=1;
%yri='2020';moi='02';dyi='01';timi='002051';nfig=1;
%yri='2020';moi='02';dyi='01';timi='003232';nfig=1;
%yri='2020';moi='02';dyi='01';timi='004414';nfig=1;
%yri='2020';moi='02';dyi='01';timi='005556';nfig=1;
%yri='2020';moi='02';dyi='01';timi='010738';nfig=1;
%yri='2020';moi='02';dyi='01';timi='011920';nfig=1;
%yri='2020';moi='02';dyi='01';timi='013102';nfig=1;
%yri='2020';moi='02';dyi='01';timi='014244';nfig=1;
%yri='2020';moi='02';dyi='01';timi='015427';nfig=1;
%yri='2020';moi='02';dyi='01';timi='020609';nfig=1;
%yri='2020';moi='02';dyi='01';timi='021752';nfig=1;
%yri='2020';moi='02';dyi='01';timi='022941';nfig=1;
%yri='2020';moi='02';dyi='01';timi='024131';nfig=1;
%yri='2020';moi='02';dyi='01';timi='025325';nfig=1;
%yri='2020';moi='02';dyi='01';timi='030515';nfig=1;
%yri='2020';moi='02';dyi='01';timi='031706';nfig=1;
%yri='2020';moi='02';dyi='01';timi='032858';nfig=1;
%yri='2020';moi='02';dyi='01';timi='034053';nfig=1;
%yri='2020';moi='02';dyi='01';timi='035247';nfig=1;
%yri='2020';moi='02';dyi='01';timi='040442';nfig=1;
%yri='2020';moi='02';dyi='01';timi='041639';nfig=6;c
%yri='2020';moi='02';dyi='01';timi='042833';nfig=1;
%yri='2020';moi='02';dyi='01';timi='044030';nfig=1;
%yri='2020';moi='02';dyi='01';timi='045226';nfig=1;
%yri='2020';moi='02';dyi='01';timi='062754';nfig=1;
%yri='2020';moi='02';dyi='01';timi='063953';nfig=1;
%
%yri='2020';moi='09';dyi='13';timi='042335';nfig=1;
%yri='2020';moi='09';dyi='13';timi='043512';nfig=1;
%yri='2020';moi='09';dyi='13';timi='044649';nfig=1;
%yri='2020';moi='09';dyi='13';timi='045822';nfig=1;
%yri='2020';moi='09';dyi='13';timi='050957';nfig=1;
%yri='2020';moi='09';dyi='13';timi='052131';nfig=1;
%yri='2020';moi='09';dyi='13';timi='053305';nfig=1;
%yri='2020';moi='09';dyi='13';timi='054437';nfig=1;
%yri='2020';moi='09';dyi='13';timi='060744';nfig=1;
%yri='2020';moi='09';dyi='13';timi='063054';nfig=1;
%yri='2020';moi='09';dyi='13';timi='070540';nfig=1;
%yri='2020';moi='09';dyi='13';timi='074019';nfig=1;
%yri='2020';moi='09';dyi='13';timi='080329';nfig=1;
%yri='2020';moi='09';dyi='13';timi='081501';nfig=1;X
%yri='2020';moi='09';dyi='13';timi='082635';nfig=1;
%yri='2020';moi='09';dyi='13';timi='090116';nfig=1;
%yri='2020';moi='09';dyi='13';timi='110310';nfig=1;
%yri='2020';moi='09';dyi='13';timi='111442';nfig=1;
%yri='2020';moi='09';dyi='13';timi='112617';nfig=1;
%yri='2020';moi='09';dyi='13';timi='113749';nfig=1;
%yri='2020';moi='09';dyi='13';timi='170134';nfig=1;

%yri='2020';moi='09';dyi='13';timi='171308';nfig=1;
%yri='2020';moi='09';dyi='13';timi='172443';nfig=11;
%yri='2020';moi='09';dyi='13';timi='173622';nfig=11;
%yri='2020';moi='09';dyi='13';timi='174759';nfig=11;
%yri='2020';moi='09';dyi='13';timi='175935';nfig=11;
%yri='2020';moi='09';dyi='13';timi='181111';nfig=15;

nfig_refl=nfig+5;%reflectivity figure number
nfig_velrw=nfig+6;
nfig_velda=nfig+7;

if yri=='2020'
  if moi=='08' | moi=='09'
    noise_vs_range=noise_vs_range+1.5;%change in noise threshold for Sep 13, 2020
  end
end

status30=1;
status40=1;
status50=1;
statusMC=1;

yr_ppi=str2num(yri);mo_ppi=str2num(moi);dy_ppi=str2num(dyi);hr_ppi=str2num(timi(1:2)); min_ppi=str2num(timi(3:4))+str2num(timi(5:6))/60;
if yr_ppi==2019
  jd_ppi=moddystr(mo_ppi)-1+dy_ppi+(hr_ppi+min_ppi/60)/24;
elseif yr_ppi==2020
  jd_ppi=moddystrl(mo_ppi)-1+dy_ppi+(hr_ppi+min_ppi/60)/24;
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

%
%calculate floe drift velocity from ship location after 14 UTC Oct 4, 2019
%(277+14/24)
%jd_drift_str=277+14/24;
%idrft=find(yd_PS>=jd_drift_str);ndrft=length(idrft);
idrft=find(yd_PS>=yd_PS(1));ndrft=length(idrft);
flo_spd(1:ndrft)=NaN;flo_dir(1:ndrft)=NaN;
for i=2:ndrft-1
  xy=distance_op(PS_lat(idrft(i-1)),PS_lat(idrft(i+1)),PS_lon(idrft(i-1)),PS_lon(idrft(i+1)));
  flo_spd(i)=xy(3)/((yd_PS(idrft(i+1))-yd_PS(idrft(i-1)))*2); % floe speed in km/12 hours
  flo_dir(i)=mod(xy(4)+180,360); % "from" floe direction (deg)-- to be compatible with wind convention
end
iinterf=find(flo_spd>25); flo_spd(iinterf)=NaN;flo_dir(iinterf)=NaN; %edit apparent gps interference points
clear xy iinterf

%set for Day of Year 2020 based on plot start date
if yr_ppi==2020
  yd_PS=yd_PS-365;
end
%interpolate to radar time
hdg_ppi=interp1(yd_PS,PS_cog,jd_ppi); %Polarstern true heading at the time of the PPI-heading and cog are switched in PS met file
tair_ppi=interp1(yd_PS,Tair,jd_ppi); %Polarstern air temperature at the time of the PPI
wsp_ppi=interp1(yd_PS,WStrue,jd_ppi); %Polarstern wind speed at the time of the PPI
wdr_ppi=interp1(yd_PS,WDtrue,jd_ppi); %Polarstern wind speed at the time of the PPI
press_ppi=interp1(yd_PS,press,jd_ppi); %Polarstern MSLP at the time of the PPI
cldbas_ppi=interp1(yd_PS,cld_base,jd_ppi); %Polarstern cloud base at the time of the PPI
flospd_ppi=interp1(yd_PS,flo_spd,jd_ppi)*1000/(12*3600); %Polarstern drift speed at the time of the PPI in m/s
flodir_ppi=interp1(yd_PS,flo_dir,jd_ppi); %Polarstern drift direction at the time of the PPI

%plot winds & ice motion around ppi time
iint=find(yd_PS>jd_ppi-0.5 & yd_PS<jd_ppi+0.5);
%yri='2020';moi='02';dyi='01';timi='030515'
figure(96);
subplot(2,1,1),plot(24*(yd_PS(iint)-floor(jd_ppi)),30*flo_spd(iint)*1000/(12*3600),'r-',24*(yd_PS(iint)-32),WStrue(iint),'b-',[24*(jd_ppi-floor(jd_ppi)) 24*(jd_ppi-floor(jd_ppi))],[0 6],'k--','LineWidth',2 )
xlabel(['hour from 00 UTC ' moi ' ' dyi ' ' yri]);ylabel('Wind Speed & 30x ice speed (m/s)')
subplot(2,1,2),plot(24*(yd_PS(iint)-floor(jd_ppi)),flo_dir(iint),'r-',24*(yd_PS(iint)-32),WDtrue(iint),'b-','LineWidth',2 )
xlabel(['hour from 00 UTC ' moi ' ' dyi ' ' yri]);ylabel('Wind Dir & Ice Dir (deg)')
%

ppi_file=['moskasacrcfrppivM1.a1.' yri moi dyi '.' timi '.nc'];
read_fil_ppi=[radar_data_dir ppi_file];
%ncdisp(read_fil_ppi,'/','min')
% base_time 1x1 int32'Base time in Epoch' 'seconds since 1970-1-1 0:00:00 0:00'
% time_offset 5368x1 'Time offset from base_time' 'seconds since 2020-02-01 01:19:20 0:00'
% time 5368x1 'Time in seconds since volume start' 'seconds since 2020-02-01 01:19:20 0:00'
% co_to_crosspol_correlation_coeff 979x5368 int16 'Copolar to cross-polar correlation coefficient (also known as rhoxh)'  add_offset= 0.83725 scale_factor= 2.5549e-05 FillValue= -32767
% crosspolar_differential_phase 979x5368 int16 'Cross-polar propagation phase shift' 'degree' (add_offset= 1.5259e-05 scale_factor= 0.0054935 FillValue = -32767
% linear_depolarization_ratio_v  979x5368 int16 'Linear depolarization ratio, vertical channel' 'dB'(add_offset= 8.1335 scale_factor= 0.00080228 FillValue = -32767
% mean_doppler_velocity 979x5368 int16 'Radial mean Doppler velocity,positive for motion away from the instrument' 'm/s'(add_offset= 0.076815  scale_factor= 0.00014769 FillValue= -32767)
% reflectivity 979x5368 int16 'Equivalent reflectivity factor' 'dBZ'(add_offset= -22.6285 scale_factor= 0.0012634 FillValue= -32767)
% signal_to_noise_ratio_copolar_h 979x5368 int16 'Signal-to-noise ratio,horizontal channel' 'dB' (add_offset= 10.6793 scale_factor= 0.0011197 FillValue= -32767)
% signal_to_noise_ratio_crosspolar_v 979x5368 int16 'Signal-to-noise ratio, Cross-polar for vertical channel'  'dB'(add_offset= 12.8958 scale_factor = 0.001132 FillValue= -32767)
% spectral_width 979x5368 int16 'Spectral width' 'm/s'; add_offset= 1.7759 scale_factor  = 5.42e-05 FillValue = -32767
% frequency 1x1 single 'Transmit center frequency' 'Hz'
% range 979x1 single 'Range to measurement volume' 'm' (meters_between_gates= 49.96; meters_to_center_of_first_gate = 506.949)
% antenna_transition 5368x1 int32 'Antenna is in transition between sweeps'[0 1]
% azimuth 5368x1 time single 'Azimuth angle from true north' 'degree'
% elevation 5368x1 single 'Elevation angle from horizontal plane'  'degree'
% fixed_angle 14x1 sweep single 'Ray target fixed angle' 'degree'
% group_intra_pulse_prt 3x1 group_pulse_number single 'Prt between group pulses' 's'
% instrument_type 22x1 string_length_22  char 'Type of instrument'
% n_samples 5368x1 time int32 'Number of Samples used to compute moments'
% nyquist_velocity 5368x1 time single 'Unambiguous doppler velocity' 'm/s'
% platform_type 22x1 string_length_22 char 'Platform type'
% polarization_mode 22x14 string_length_22,sweep char 'Polarization mode for sweep'
% primary_axis 22x1 string_length_22 char 'Primary axis of rotation'
% prt 5368x1 time single 'Pulse repetition time'  's'
% prt_mode 22x14 string_length_22,sweep char 'Transmit pulse mode'
% pulse_width 5368x1 time single 'Transmitter pulse width' 's'
% r_calib_index 5368x1 time int8 'Calibration data array index per ray'
% r_calib_noise_hc 1x1 r_calib single 'Measured noise level horizontal copolar channel' 'dBm'
% r_calib_noise_source_power_h 1x1  r_calib single 'Noise source power horizontal channel' 'dBm'
% r_calib_noise_source_power_v  1x1 r_calib single 'Noise source power vertical channel' 'dBm'
% r_calib_noise_vc 1x1 r_calib single 'Measured noise level vertical copolar channel'  'dBm'
% r_calib_pulse_width 1x1 r_calib single 'Calibrated Pulse Width'  's'
% r_calib_radar_constant_h  1x1 r_calib single 'Calibrated radar constant horizontal channel'  'dB'
% r_calib_radar_constant_v  1x1  r_calib single 'Calibrated radar constant vertical channel'  'dB'
% r_calib_receiver_gain_hc  1x1 r_calib single'Calibrated radar receiver gain horizontal copolar channel' 'dB'
% r_calib_receiver_gain_vc 1x1 r_calib single 'Calibrated radar receiver gain vertical copolar channel'  'dB'
% r_calib_two_way_radome_loss_h 1x1 r_calib single 'Radar calibration two way radome loss horizontal channel' 'dB'
% r_calib_xmit_power_h 1x1 r_calib single 'Transmit power horizontal channel'  'dBm'
% radar_antenna_gain_h 1x1 single 'Nominal Antenna gain, H Polarization' 'dB'
% radar_antenna_gain_v  1x1 single 'Nominal Antenna gain, Vertical Polarization' 'dB'
% radar_beam_width_h 1x1 single 'Half power radar beam width horizontal channel' 'degree'
% radar_beam_width_v 1x1 single 'Half power radar beam width vertical channel' 'degree'
% radar_measured_sky_noise_h 5368x1 time single 'Measured sky noise, horizontal channel' 'dBm'
% radar_measured_sky_noise_v 5368x1  time single 'Measured sky noise, vertical channel' 'dBm'
% radar_measured_transmit_power  5368x1 time single 'Radar measured transmit peak power' 'dBm'
% scan_rate 5368x1 time single 'Target scan rate for sweep'  'degree/s'
% sweep_end_ray_index 14x1 sweep int32 'Index of last ray in sweep'
% sweep_mode 22x14 string_length_22,sweep char 'Scan mode for sweep'
% sweep_number 14x1 sweep int32 'Sweep index number 0 based'
% sweep_start_ray_index 14x1 sweep int32 'Index of first ray in sweep'
% time_coverage_end 22x1 string_length_22 char 'Data volume end time UTC'
% time_coverage_start 22x1 string_length_22 char 'Data volume start time UTC'
% unambiguous_range 5368x1 time single 'Unambiguous Range' 'm'
% volume_number 1x1 int32 'Data volume index number'
% latitude 1x1 single 'Latitude' 'degree_N'
% longitude 1x1 single 'Longitude' 'degree_E'
% altitude 1x1 single'Altitude' 'm'
% altitude_agl 1x1 single 'Altitude above ground level' 'm'
% lat  1x1 single 'North latitude' 'degree_N'
% lon  1x1 single 'East longitude''degree_E'
% alt 1x1 single 'Altitude above mean sea level' 'm'

base_time=ncread(read_fil_ppi,'base_time');%'seconds since 1970-1-1 0:00:00 0:00'
tsec=ncread(read_fil_ppi,'time');%'Time in seconds since volume start' 'seconds since 2020-02-01 01:19:20 0:00'
nyqvel=ncread(read_fil_ppi,'nyquist_velocity');
% hrday(ist:ien)=tsec/3600;
% jdtwr(ist:ien)=jdstr-1+nd+hrday(ist:ien)/24;
lat_sacr=ncread(read_fil_ppi,'latitude');%'Latitude' 'degree_N'
lon_sacr=ncread(read_fil_ppi,'longitude');%'Longitude' 'degree_E'
hgt_sacr=ncread(read_fil_ppi,'altitude');%'Altitude above ground level' 'm'
time_vol_start=transpose(ncread(read_fil_ppi,'time_coverage_start')) %'Data volume start time UTC'
time_vol_end=transpose(ncread(read_fil_ppi,'time_coverage_end')) %'Data volume end time UTC'
tsec_vstr=str2num(time_vol_start(18:19));tmin_vstr=str2num(time_vol_start(15:16));thr_vstr=str2num(time_vol_start(12:13));

% sweep_mode 22x14 string_length_22,sweep char 'Scan mode for sweep'
% prt_mode 22x14 string_length_22,sweep char 'Transmit pulse mode'
% platform_type 22x1 string_length_22 char 'Platform type'
% polarization_mode 22x14 string_length_22,sweep char 'Polarization mode for sweep'
% primary_axis 22x1 string_length_22 char 'Primary axis of rotation'

elev_ang_est=ncread(read_fil_ppi,'fixed_angle'); % fixed_angle 14x1 sweep single 'Ray target fixed angle' 'degree'
% -0.0154 0.7867 1.4953 2.4676 2.9894 3.5003 4.4671 6.0217 9.0046 14.0254 19.5022 25.0064 36.4983 60.0149
% -0.0044 0.0341 -0.0209 0.7757 0.8031 1.5173 1.9842 2.5115 3.0114 3.5113 4.4781 6.0107 8.9991 13.9979 13.9979 19.5186 19.4802 25.0009 36.4653 36.4708 36.5092 59.9819

rnd_elev_ang=round(elev_ang_est*10)/10;
elev_req=0.75;
ichs=find(abs(rnd_elev_ang-elev_req)<0.28);%choose the elevation angle
if length(ichs)>1
  ichs1=ichs(1);
else
  ichs1=ichs;
end
nelev=length(elev_ang_est);
elevchs=rnd_elev_ang(min([ichs1 nelev]));
sweep_strt_ray=ncread(read_fil_ppi,'sweep_start_ray_index');% sweep_start_ray_index 14x1 sweep int32 'Index of first ray in sweep'
sweep_end_ray=ncread(read_fil_ppi,'sweep_end_ray_index');% sweep_end_ray_index 14x1 sweep int32 'Index of last ray in sweep'
sweep_ray_length=sweep_end_ray-sweep_strt_ray+1;
test=find(elev_ang_est>elevchs-0.2 & elev_ang_est<elevchs+0.2 & sweep_ray_length>267);
%test=find(elev_ang_est>0.25 & elev_ang_est<1.0 & sweep_ray_length>267);
if length(test)>0
  kelev_sel=test(1); %select the first elevation angle that meets the criteria
  sel_elev_ang=elev_ang_est(kelev_sel)
  display(['elevation angle plot = ' num2str(sel_elev_ang)])
  clear test
else
  display('no sweep meets criteria')
end

% group_intra_pulse_prt 3x1 group_pulse_number single 'Prt between group pulses' 's'
% instrument_type 22x1 string_length_22  char 'Type of instrument'
% frequency 1x1 single 'Transmit center frequency' 'Hz'
range=ncread(read_fil_ppi,'range');% 979x1 single 'Range to measurement volume' 'm' (meters_between_gates= 49.96; meters_to_center_of_first_gate = 506.949)
ngate=length(range);
ht(1:ngate,1:nelev)=NaN;
ht_rad=ncread(read_fil_ppi,'altitude_agl');%radar height above ground level (m)
er=6.37e6;%earth's radius (m)
cpr=0.375/er;
kaband_range=50000;
nyquist_kaband=10.8;%+/- m/s
for k=1:nelev
  for i=1:ngate
    ht(i,k)=ht_rad+range(i)*range(i)*cpr*cos(elev_ang_est(k)*pi/180)+range(i)*sin(elev_ang_est(k)*pi/180);%height above local surface (m)
  end
end
azm_sacr=ncread(read_fil_ppi,'azimuth');% 5368x1 time single 'Azimuth angle from true north' 'degree'
elev_sacr=ncread(read_fil_ppi,'elevation');% 5368x1 single 'Elevation angle from horizontal plane'  'degree'
Xmt_power=ncread(read_fil_ppi,'radar_measured_transmit_power');%  5368x1 time single 'Radar measured transmit peak power' 'dBm'
n_samples=ncread(read_fil_ppi,'n_samples');% 5368x1 time int32 'Number of Samples used to compute moments'
ant_trans=ncread(read_fil_ppi,'antenna_transition');% 5368x1 int32 'Antenna is in transition between sweeps'[0 1]
unambig_range=ncread(read_fil_ppi,'unambiguous_range'); %5368x1 'Unambiguous Range' 'm'
scan_rate=ncread(read_fil_ppi,'scan_rate');% 5368x1 time single 'Target scan rate for sweep'  'degree/s'
% co_to_crosspol_correlation_coeff 979x5368 int16 'Copolar to cross-polar correlation coefficient (also known as rhoxh)'  add_offset= 0.83725 scale_factor= 2.5549e-05 FillValue= -32767
% crosspolar_differential_phase 979x5368 int16 'Cross-polar propagation phase shift' 'degree' (add_offset= 1.5259e-05 scale_factor= 0.0054935 FillValue = -32767
% linear_depolarization_ratio_v  979x5368 int16 'Linear depolarization ratio, vertical channel' 'dB'(add_offset= 8.1335 scale_factor= 0.00080228 FillValue = -32767

%read & scale Doppler radial velocity
ncid = netcdf.open(read_fil_ppi,'NC_NOWRITE');
%varid = netcdf.inqVarID(ncid,'mean_doppler_velocity');
%vel_scalfact = netcdf.getAtt(ncid,varid,'scale_factor');
%vel_offset = netcdf.getAtt(ncid,varid,'add_offset');
%vel_scalfact=0.00014769;vel_offset=0.076815;
vel_scalfact=1;vel_offset=0;
%raw_doppl_vel=ncread(read_fil_ppi,'mean_doppler_velocity');
rad_vel=vel_scalfact*(ncread(read_fil_ppi,'mean_doppler_velocity'))+vel_offset; % 979x5368 'Radial mean Doppler velocity,positive for motion away from the instrument' 'm/s'(add_offset= 0.076815  scale_factor= 0.00014769 FillValue= -32767)

%read & scale radar reflectivity
%varid = netcdf.inqVarID(ncid,'reflectivity');
%ref_scalfact = netcdf.getAtt(ncid,varid,'scale_factor');
%ref_offset = netcdf.getAtt(ncid,varid,'add_offset');
%ref_scalfact=0.0012634;ref_offset=-22.6285;
ref_scalfact=1;ref_offset=0;
refl=ref_scalfact*(ncread(read_fil_ppi,'reflectivity'))+ref_offset; % 979x5368 int16 'Equivalent reflectivity factor' 'dBZ'(add_offset= -22.6285 scale_factor= 0.0012634 FillValue= -32767)
mdrng=median(refl,2,'omitnan');
mnrng=mean(refl,2,'omitnan');
minrng=min(refl,[],2,'omitnan');
%smminrng=smooth(minrng,20);
smminrng=smoothrm(minrng,20);

% read signal-to-noise ratio-h
%varid = netcdf.inqVarID(ncid,'signal_to_noise_ratio_copolar_h');
%sig2nsh_scalfact = netcdf.getAtt(ncid,varid,'scale_factor');
%sig2nsh_offset = netcdf.getAtt(ncid,varid,'add_offset');
%sig2nsh_scalfact=0.0011197;sig2nsh_offset=10.6793;
sig2nsh_scalfact=1;sig2nsh_offset=0;
sig2noise_h=sig2nsh_scalfact*(ncread(read_fil_ppi,'signal_to_noise_ratio_copolar_h'))+sig2nsh_offset; % 979x5368 int16 'Signal-to-noise ratio,horizontal channel' 'dB' (add_offset= 10.6793 scale_factor= 0.0011197 FillValue= -32767)
%varid = netcdf.inqVarID(ncid,'signal_to_noise_ratio_crosspolar_v');
%sig2nsv_scalfact = netcdf.getAtt(ncid,varid,'scale_factor');
%sig2nsv_offset = netcdf.getAtt(ncid,varid,'add_offset');
%sig2nsv_scalfact=1;sig2nsv_offset=0;
%sig2noise_v=sig2nsv_scalfact*(ncread(read_fil_ppi,'signal_to_noise_ratio_crosspolar_v'))+sig2nsv_offset; % 979x5368 int16 'Signal-to-noise ratio, Cross-polar for vertical channel'  'dB'(add_offset= 12.8958 scale_factor = 0.001132 FillValue= -32767)
% spec_width=ncread(read_fil_ppi,'spectral_width');% 979x5368 int16 'Spectral width' 'm/s'; add_offset= 1.7759 scale_factor  = 5.42e-05 FillValue = -32767


%ielev_selec=find(elev_sacr>=elev_ang_est(kelev_sel)-0.02 & elev_sacr<elev_ang_est(kelev_sel)+0.02 & ant_trans==0);
ielev_selec=find(elev_sacr==elev_ang_est(kelev_sel));

nfig=nfig+1; figure(nfig)
subplot(3,1,1),plot(tsec,azm_sacr,'r-');
xlabel('seconds');ylabel('azimuth (deg)')
subplot(3,1,2),plot(tsec,elev_sacr,'b-');
xlabel('seconds');ylabel('elevation (deg)')
subplot(3,1,3),plot(tsec,ant_trans,'kx');
xlabel('seconds');ylabel('antenna in transition = 1')

%reflc=refl+refl_calib;
reflc=refl;
nfig=nfig+1; figure(nfig)
subplot(2,1,1),plot(range,reflc(:,1000),'r.',range,reflc(:,1100),'b.',range,reflc(:,1200),'g.',range,reflc(:,1300),'m.',range,reflc(:,1400),'c.',range,mnrng,'r-',range,mdrng+3,'m-',...
    range,noise_vs_range,'b-',range,smminrng,'k-',[range(1) range(end)],[-22.6285 -22.6285],'k--')
xlabel('Range (m)')
ylabel('Refl (dBz)')
subplot(2,1,2),plot(tsec,nyqvel,'r.',range,rad_vel(:,200),'b.')
xlabel('Seconds)')
ylabel('Nyquist velocity (m/s)')

nfig=nfig+1; figure(nfig)
kmrange=range/1000;
subplot(2,1,1),plot(kmrange,sig2noise_h(:,1000),'r-',kmrange,sig2noise_h(:,1100),'b-',kmrange,sig2noise_h(:,1200),'g-',kmrange,sig2noise_h(:,1300),'m-',kmrange,sig2noise_h(:,1400),'c-',[kmrange(1) kmrange(end)],[0 0],'k--')
legend(['azm= ' num2str(round(10*azm_sacr(1000))/10)],['azm= ' num2str(round(10*azm_sacr(1100))/10)],['azm= ' num2str(round(10*azm_sacr(1200))/10)],['azm= ' num2str(round(10*azm_sacr(1300))/10)],['azm= ' num2str(round(10*azm_sacr(1400))/10)])
%subplot(2,1,1),plot(kmrange,sig2noise_h(:,1000),'r-',[kmrange(1) kmrange(end)],[0 0],'k--')
%legend(['azm= ' num2str(round(10*azm_sacr(1000))/10)])
xlabel('Range (km)')
ylabel('Horiz S/N (dBz)')
hold on
  text(30,30,['elev= ' num2str(round(100*elev_sacr(1000))/100)])
hold off
%subplot(2,1,2),plot(kmrange,sig2noise_v(:,1000),'r-',kmrange,sig2noise_v(:,1100),'b-',kmrange,sig2noise_v(:,1200),'g-',kmrange,sig2noise_v(:,1300),'m-',kmrange,sig2noise_v(:,1400),'c-',[kmrange(1) kmrange(end)],[0 0],'k--')
%legend(['azm= ' num2str(round(10*azm_sacr(1000))/10)],['azm= ' num2str(round(10*azm_sacr(1100))/10)],['azm= ' num2str(round(10*azm_sacr(1200))/10)],['azm= ' num2str(round(10*azm_sacr(1300))/10)],['azm= ' num2str(round(10*azm_sacr(1400))/10)])
%subplot(2,1,2),plot(kmrange,sig2noise_v(:,1000),'r-',[kmrange(1) kmrange(end)],[0 0],'k--')
%legend(['azm= ' num2str(round(10*azm_sacr(1000))/10)])
xlabel('Range (km)')
ylabel('Vert S/N (dBz)')


%Met & ASFS data
data_avg='10min';npdy=144; % 10-min average data
arrlen=npdy;%array size for one day
nd=1; %number of days
ist=(nd-1)*npdy+1;ien=ist+npdy-1;
jdstr=floor(jd_ppi);%day of ppi data

%tower data
jdtwr(1:arrlen)=NaN;hrday(1:arrlen)=NaN;
lat_twr(1:arrlen)=NaN;lon_twr(1:arrlen)=NaN;lat_mast(1:arrlen)=NaN;lon_mast(1:arrlen)=NaN;
hdg_twr(1:arrlen)=NaN;hdg_mast(1:arrlen)=NaN;shp_brng(1:arrlen)=NaN;shp_dis(1:arrlen)=NaN;
ta_2m(1:arrlen)=NaN;ta_6m(1:arrlen)=NaN;ta_10m(1:arrlen)=NaN;ta_mast(1:arrlen)=NaN;
rh_2m(1:arrlen)=NaN;rh_6m(1:arrlen)=NaN;rh_10m(1:arrlen)=NaN;rh_mast(1:arrlen)=NaN;
rhi_2m(1:arrlen)=NaN;rhi_6m(1:arrlen)=NaN;rhi_10m(1:arrlen)=NaN;rhi_mast(1:arrlen)=NaN;
wspd_2m(1:arrlen)=NaN; wspd_6m(1:arrlen)=NaN;wspd_10m(1:arrlen)=NaN;wspd_mast(1:arrlen)=NaN;
wdir_2m(1:arrlen)=NaN; wdir_6m(1:arrlen)=NaN;wdir_10m(1:arrlen)=NaN;wdir_mast(1:arrlen)=NaN;
hrday(1:arrlen)=NaN;jdtwr(1:arrlen)=NaN;lat_twr(1:arrlen)=NaN;lon_twr(1:arrlen)=NaN;
t_skin_rad(1:arrlen)=NaN;t_skin_Apogee(1:arrlen)=NaN;
mslp_twr(1:arrlen)=NaN;div_DN(1:arrlen)=NaN;
ww_2m(1:arrlen)=NaN;ww_6m(1:arrlen)=NaN;ww_10m(1:arrlen)=NaN;ww_mast(1:arrlen)=NaN;
Hs_cov_2m(1:arrlen)=NaN;Hs_cov_6m(1:arrlen)=NaN;Hs_cov_10m(1:arrlen)=NaN;Hs_cov_mast(1:arrlen)=NaN;
Hs_blk_10m(1:arrlen)=NaN;HlW_blk_10m(1:arrlen)=NaN;Hl_cov(1:arrlen)=NaN;HlW_cov(1:arrlen)=NaN;
ustr_cov_2m(1:arrlen)=NaN;ustr_cov_6m(1:arrlen)=NaN;ustr_cov_10m(1:arrlen)=NaN;ustr_cov_mast(1:arrlen)=NaN;
ustr_blk_10m(1:arrlen)=NaN;
sigU_2m(1:arrlen)=NaN;sigV_2m(1:arrlen)=NaN;sigW_2m(1:arrlen)=NaN;sigT_2m(1:arrlen)=NaN;%
sigU_6m(1:arrlen)=NaN;sigV_6m(1:arrlen)=NaN;sigW_6m(1:arrlen)=NaN;sigT_6m(1:arrlen)=NaN;
sigU_10m(1:arrlen)=NaN;sigV_10m(1:arrlen)=NaN;sigW_10m(1:arrlen)=NaN;sigT_10m(1:arrlen)=NaN;
sigU_mast(1:arrlen)=NaN;sigV_mast(1:arrlen)=NaN;sigW_mast(1:arrlen)=NaN;sigT_mast(1:arrlen)=NaN;
lwd_arm_mc(1:arrlen)=NaN;lwu_arm_mc(1:arrlen)=NaN;swd_arm_mc(1:arrlen)=NaN;swu_arm_mc(1:arrlen)=NaN;
Hs_cov_2m(1:arrlen)=NaN; Hs_cov_6m(1:arrlen)=NaN;Hs_cov_10m(1:arrlen)=NaN;Hs_cov_mast(1:arrlen)=NaN;
Hl_cov(1:arrlen)=NaN;HlW_cov(1:arrlen)=NaN;
Hs_blk_10m(1:arrlen)=NaN;HlW_blk_10m(1:arrlen)=NaN;
ustr_cov_2m(1:arrlen)=NaN;ustr_cov_6m(1:arrlen)=NaN;ustr_cov_10m(1:arrlen)=NaN;ustr_cov_mast(1:arrlen)=NaN;
ustr_blk_10m(1:arrlen)=NaN;

%yri='2020';moi='01';dyi='08';
date=[yri moi dyi];
%timi='105342';
hrrad=str2num(timi(1:2))+str2num(timi(3:4))/60+str2num(timi(5:6))/3600;

if yri=='2020'
  jdstr=moddystrl(str2num(moi))-1+str2num(dyi);
else
  jdstr=moddystr(str2num(moi))-1+str2num(dyi);
end
  %if jdstr+nd-1>=289 | (yearst==2020 & (str2num(date)~=20200324 & str2num(date)~=20200401))
 % if jdstr+nd-1>=289 | (yearst==2020 & (str2num(date)~=20200401)) & (str2num(date)~=20200821) & (str2num(date)~=20200822)& (str2num(date)~=20200823) & (str2num(date)~=20200824)
  if length(intersect(str2num(date),[20191011 20191013 20200324 20200401 20200821:1:20200824 20200919:1:20200930 20201001]))==0
%    filnamtwr=[tower_data_dir 'mosseb.metcity.level2v3.' data_avg '.' date '.000000.nc']
    filnamtwr=[tower_data_dir 'mosseb.metcity.level2.4.' data_avg '.' date '.000000.nc']
    tsectwr=ncread(filnamtwr,'time');
    hrday(ist:ien)=tsectwr/3600;
    jdtwr(ist:ien)=jdstr-1+nd+hrday(ist:ien)/24;
    lat_twr(ist:ien)=ncread(filnamtwr,'lat_tower');%
    lon_twr(ist:ien)=ncread(filnamtwr,'lon_tower');%
    lat_mast(ist:ien)=ncread(filnamtwr,'lat_mast');%
    lon_mast(ist:ien)=ncread(filnamtwr,'lon_mast');%
    hdg_twr(ist:ien)=ncread(filnamtwr,'heading_tower');% heading from gps at the tower deg true
    hdg_mast(ist:ien)=ncread(filnamtwr,'heading_mast');% heading from gps at the mast deg
    shp_brng(ist:ien)=ncread(filnamtwr,'ship_bearing');% rel to true north
    shp_dis(ist:ien)=ncread(filnamtwr,'ship_distance');% meters
    ta_2m(ist:ien)=ncread(filnamtwr,'temp_2m');%'Vaisala PTU300'
    ta_6m(ist:ien)=ncread(filnamtwr,'temp_6m');%'Vaisala HMT330'
    ta_10m(ist:ien)=ncread(filnamtwr,'temp_10m');%'Vaisala HMT330'
    ta_mast(ist:ien)=ncread(filnamtwr,'temp_mast');%'Vaisala WXT530'
    t_skin_rad(ist:ien)=ncread(filnamtwr,'skin_temp_surface');
    t_skin_Apogee(ist:ien)=ncread(filnamtwr,'brightness_temp_surface');
    rh_2m(ist:ien)=ncread(filnamtwr,'rh_2m');%'Vaisala PTU300'
    rh_6m(ist:ien)=ncread(filnamtwr,'rh_6m');%'Vaisala HMT330'
    rh_10m(ist:ien)=ncread(filnamtwr,'rh_10m');%'Vaisala HMT330'
    rh_mast(ist:ien)=ncread(filnamtwr,'rh_mast');%'Vaisala WXT530'
    rhi_2m(ist:ien)=ncread(filnamtwr,'rhi_2m');%'Vaisala PTU300'
    rhi_6m(ist:ien)=ncread(filnamtwr,'rhi_6m');%'Vaisala HMT330'
    rhi_10m(ist:ien)=ncread(filnamtwr,'rhi_10m');%'Vaisala HMT330'
    rhi_mast(ist:ien)=ncread(filnamtwr,'rhi_mast');%'Vaisala WXT530'
    wspd_2m(ist:ien)=ncread(filnamtwr,'wspd_vec_mean_2m');% 
    wspd_6m(ist:ien)=ncread(filnamtwr,'wspd_vec_mean_6m');%
    wspd_10m(ist:ien)=ncread(filnamtwr,'wspd_vec_mean_10m');%
    wspd_mast(ist:ien)=ncread(filnamtwr,'wspd_vec_mean_mast');%
    wdir_2m(ist:ien)=ncread(filnamtwr,'wdir_vec_mean_2m');% 
    wdir_6m(ist:ien)=ncread(filnamtwr,'wdir_vec_mean_6m');%
    wdir_10m(ist:ien)=ncread(filnamtwr,'wdir_vec_mean_10m');%
    wdir_mast(ist:ien)=ncread(filnamtwr,'wdir_vec_mean_mast');%
    ww_2m(ist:ien)=ncread(filnamtwr,'wspd_w_mean_2m');%
    ww_6m(ist:ien)=ncread(filnamtwr,'wspd_w_mean_6m');%
    ww_10m(ist:ien)=ncread(filnamtwr,'wspd_w_mean_10m');%
    ww_mast(ist:ien)=ncread(filnamtwr,'wspd_w_mean_mast');%
    mslp_twr(ist:ien)=ncread(filnamtwr,'atmos_pressure_2m');%
    
    %sigu_2m(ist:ien)=ncread(filnamtwr,'wspd_u_std_2m');% 
    %sigv_2m(ist:ien)=ncread(filnamtwr,'wspd_v_std_2m');%
    %sigw_2m(ist:ien)=ncread(filnamtwr,'wspd_w_std_2m');%
    sigU_2m(ist:ien)=ncread(filnamtwr,'sigU_2m');% 
    sigV_2m(ist:ien)=ncread(filnamtwr,'sigV_2m');%
    sigW_2m(ist:ien)=ncread(filnamtwr,'sigW_2m');%
    sigT_2m(ist:ien)=ncread(filnamtwr,'temp_acoustic_std_2m');%
    %sigu_6m(ist:ien)=ncread(filnamtwr,'wspd_u_std_6m');%
    %sigv_6m(ist:ien)=ncread(filnamtwr,'wspd_v_std_6m');%
    %sigw_6m(ist:ien)=ncread(filnamtwr,'wspd_w_std_6m');%
    sigU_6m(ist:ien)=ncread(filnamtwr,'sigU_6m');% 
    sigV_6m(ist:ien)=ncread(filnamtwr,'sigV_6m');%
    sigW_6m(ist:ien)=ncread(filnamtwr,'sigW_6m');%
    sigT_6m(ist:ien)=ncread(filnamtwr,'temp_acoustic_std_6m');%
    %sigu_10m(ist:ien)=ncread(filnamtwr,'wspd_u_std_10m');%
    %sigv_10m(ist:ien)=ncread(filnamtwr,'wspd_v_std_10m');%
    %sigw_10m(ist:ien)=ncread(filnamtwr,'wspd_w_std_10m');%
    sigU_10m(ist:ien)=ncread(filnamtwr,'sigU_10m');% 
    sigV_10m(ist:ien)=ncread(filnamtwr,'sigV_10m');%
    sigW_10m(ist:ien)=ncread(filnamtwr,'sigW_10m');%
    sigT_10m(ist:ien)=ncread(filnamtwr,'temp_acoustic_std_10m');%
    %sigu_mast(ist:ien)=ncread(filnamtwr,'wspd_u_std_mast');%
    %sigv_mast(ist:ien)=ncread(filnamtwr,'wspd_v_std_mast');%
    %sigw_mast(ist:ien)=ncread(filnamtwr,'wspd_w_std_mast');%
    sigU_mast(ist:ien)=ncread(filnamtwr,'sigU_mast');% 
    sigV_mast(ist:ien)=ncread(filnamtwr,'sigV_mast');%
    sigW_mast(ist:ien)=ncread(filnamtwr,'sigW_mast');%
    sigT_mast(ist:ien)=ncread(filnamtwr,'temp_acoustic_std_mast');%
    
    Hs_cov_2m(ist:ien)=ncread(filnamtwr,'Hs_2m');%
    Hs_cov_6m(ist:ien)=ncread(filnamtwr,'Hs_6m');%
    Hs_cov_10m(ist:ien)=ncread(filnamtwr,'Hs_10m');%
    Hs_cov_mast(ist:ien)=ncread(filnamtwr,'Hs_mast');%
    Hl_cov(ist:ien)=ncread(filnamtwr,'Hl');%
    HlW_cov(ist:ien)=ncread(filnamtwr,'Hl_Webb');%
    Hs_blk_10m(ist:ien)=ncread(filnamtwr,'bulk_Hs_10m');%
    HlW_blk_10m(ist:ien)=ncread(filnamtwr,'bulk_Hl_Webb_10m');%
    ustr_cov_2m(ist:ien)=ncread(filnamtwr,'ustar_2m');%
    ustr_cov_6m(ist:ien)=ncread(filnamtwr,'ustar_6m');%
    ustr_cov_10m(ist:ien)=ncread(filnamtwr,'ustar_10m');%
    ustr_cov_mast(ist:ien)=ncread(filnamtwr,'ustar_mast');%
    ustr_blk_10m(ist:ien)=ncread(filnamtwr,'bulk_ustar');%

    lwd_arm_mc(ist:ien)=ncread(filnamtwr,'down_long_hemisp');%144x1 'W/m2' 'net downward longwave flux' 'Eppley PIR' 'ARM' 'Met City'
    lwu_arm_mc(ist:ien)=ncread(filnamtwr,'up_long_hemisp');%144x1 'W/m2' 'net upward longwave flux' 'Eppley PIR' 'Radiation Station'
    swd_arm_mc(ist:ien)=ncread(filnamtwr,'down_short_hemisp');%144x1 'W/m2' 'net downward shortwave flux' 'Eppley PSP' 'ARM' 'Met City'
    swu_arm_mc(ist:ien)=ncread(filnamtwr,'up_short_hemisp');%144x1 'W/m2' 'net upward shortwave flux' 'Eppley PSP' 'Radiation Station'

    clear filnamtwr tsectwr
    if hrrad(1)+10/60>hrday(end)
        indtwr=length(hrday);
    else
        indtwr=find(hrday>=hrrad(1) & hrday<=hrrad(1)+10/60);
    end
  else
    jdtwr(ist:ien)=jdstr-1+nd+[0:npdy-1]*10/60/24;
  end

%
%ASFS30 data
%

ta_30(1:arrlen)=NaN;rh_30(1:arrlen)=NaN;
wspd_30(1:arrlen)=NaN; wdir_30(1:arrlen)=NaN; 
hrday_30(1:arrlen)=NaN;jd30(1:arrlen)=NaN;
lat_30(1:arrlen)=NaN;lon_30(1:arrlen)=NaN;
mslp_30(1:arrlen)=NaN;tskn_30(1:arrlen)=NaN;
lwd_30(1:arrlen)=NaN;swd_30(1:arrlen)=NaN;lwu_30(1:arrlen)=NaN;swu_30(1:arrlen)=NaN;%
alb_30(1:arrlen)=NaN;
Hs_cov_30(1:arrlen)=NaN;HlW_cov_30(1:arrlen)=NaN;%
shpbrg_30(1:arrlen)=NaN;shpdis_30(1:arrlen)=NaN;%
%
%ASFS40 data
%
ta_40(1:arrlen)=NaN;rh_40(1:arrlen)=NaN;
wspd_40(1:arrlen)=NaN; wdir_40(1:arrlen)=NaN; 
hrday_40(1:arrlen)=NaN;jd40(1:arrlen)=NaN;
lat_40(1:arrlen)=NaN;lon_40(1:arrlen)=NaN;
mslp_40(1:arrlen)=NaN;tskn_40(1:arrlen)=NaN;
lwd_40(1:arrlen)=NaN;swd_40(1:arrlen)=NaN;lwu_40(1:arrlen)=NaN;swu_40(1:arrlen)=NaN;%
alb_40(1:arrlen)=NaN;
Hs_cov_40(1:arrlen)=NaN;HlW_cov_40(1:arrlen)=NaN;%
shpbrg_40(1:arrlen)=NaN;shpdis_40(1:arrlen)=NaN;%

%
%ASFS50 data
%
ta_50(1:arrlen)=NaN;rh_50(1:arrlen)=NaN;
wspd_50(1:arrlen)=NaN; wdir_50(1:arrlen)=NaN; 
hrday_50(1:arrlen)=NaN;jd50(1:arrlen)=NaN;
lat_50(1:arrlen)=NaN;lon_50(1:arrlen)=NaN;
mslp_50(1:arrlen)=NaN;tskn_50(1:arrlen)=NaN;
lwd_50(1:arrlen)=NaN;swd_50(1:arrlen)=NaN;lwu_50(1:arrlen)=NaN;swu_50(1:arrlen)=NaN;%
alb_50(1:arrlen)=NaN;
Hs_cov_50(1:arrlen)=NaN;HlW_cov_50(1:arrlen)=NaN;%
shpbrg_50(1:arrlen)=NaN;shpdis_50(1:arrlen)=NaN;%
% 
% data exists if status=1

if status30==1
%    filnam30=[asfs30_data_dir 'mosasfs30met.' data_vers '.' data_avg '.' date '.000000.nc']
    filnam30=[asfs30_data_dir 'mosseb.asfs30.' data_vers '.' data_avg '.' date '.000000.nc']
%  ncdisp(filnam30)
% base_time 1x1 int32 '2020-01-25T00:00:00.000000' 'Base time since Epoch' 'seconds since 1970-01-01T00:00:00.000000' 'time_offset'
% time 144x1 double 'seconds since 2020-01-25T00:00:00.000000' '0000-00-00 00:01:00' 'Time offset from midnight'
% time_offset 144x1 double 'seconds since 2020-01-25T00:00:00.000000' 'Time offset from base_time'
% lat 144x1 double 'degrees_north' 'latitude from gps at station' 'Hemisphere V102' '2 m'
% lon 144x1 double 'degrees_east' 'longitude from gps at station' 'Hemisphere V102' '2 m'
% heading 144x1 double 'degrees_true' heading from gps at station' 'Hemisphere V102' '2 m'
% zenith_true 144x1 double 'degrees' 'true solar zenith angle' 'Hemisphere V102' 'Reda and Andreas, Solar position algorithm for solar radiation applications. Solar Energy, vol. 76, no. 5, pp. 577-589, 2004.'
% zenith_apparent 144x1 double 'degrees' 'estimated apprarent solar zenith angle due to atmospheric refraction' 'Hemisphere V102' 'Reda and Andreas, Solar position algorithm for solar radiation applications. Solar Energy, vol. 76, no. 5, pp. 577-589, 2004.'
% azimuth 144x1 double 'degrees' 'apprarent solar azimuth angle' 'Hemisphere V102' 'Reda and Andreas, Solar position algorithm for solar radiation applications. Solar Energy, vol. 76, no. 5, pp. 577-589, 2004.'
% ship_distance 144x1 double 'meters' 'distance between the ship and the tower' 'Hemisphere V102 & Polarstern Leica GPS'
% ship_bearing 144x1 double 'degrees' 'absolute bearing (rel. to true north) of ship from the position of the tower' 'Hemisphere V102 & Polarstern Leica GPS'
% sr50_dist 144x1 double 'meters' 'distance to surface from SR50; temperature compensation correction applied' 'Campbell Scientific SR50A' 'unheated, temperature correction applied' '2 m'
% snow_depth 144x1 double 'cm' 'snow depth near station base' 'Hukseflux HFP01' 'derived snow depth from temperature-corrected SR50 distance values based on initialization. footprint nominally 0.47 m radius.'
% atmos_pressure 144x1 double 'hPa' 'atmospheric pressure' 'Vaisala PTU 300' '2 m'
% temp 144x1 double 'deg C' 'air temperature' 'Vaisala HMT330' '2 m'
% rh 144x1 double 'percent' 'relative humidity' 'Vaisala PTU300' 'digitally polled from instument' '2 m'
% dew_point 144x1 double 'deg C' 'dewpoint temperature' 'Vaisala PTU300' 'digitally polled from instument'
% mixing_ratio 144x1 double 'g/kg' 'mixing ratio' 'Vaisala PTU300' 'calculated from measured variables following Wexler (1976)'
% vapor_pressure 144x1 double 'Pa' 'vapor pressure' 'Vaisala PTU300' 'calculated from measured variables following Wexler (1976)'
% rhi 144x1 double 'percent' 'relative humidity wrt ice' 'Vaisala PTU300' 'calculated from measured variables following Hyland & Wexler (1983)'
% brightness_temp_surface 144x1 double 'deg C' 'sensor target 8-14 micron brightness temperature' 'Apogee SI-4H1-SS IRT' 'digitally polled from instument. No emmisivity correction. No correction for reflected incident.'
% skin_temp_surface 144x1 double 'deg C' 'surface radiometric skin temperature assummed emissivity, corrected for IR reflection' 'Apogee SI-4H1-SS IRT, IR20 LWu, LWd' 'Eq.(2.2) Persson et al. (2002) https://www.doi.org/10.1029/2000JC000705; emis = 0.985'
% subsurface_heat_flux_A 144x1 double 'W/m2' 'conductive flux' 'Hukseflux HFP01' 'Sensitivity 63.00/1000 [mV/(W/m2)]' 'subsurface, variable' '10m south of station at met city'
% subsurface_heat_flux_B 144x1 double 'W/m2' 'conductive flux' 'Hukseflux HFP01' 'subsurface, variable' 'under Apogee and SR50 at station base'
% wspd_vec_mean 144x1 double 'm/s' 'average metek wind speed' 'Metek uSonic-Cage MP sonic anemometer' 'derived from hozirontal wind components after coordinate transformation from body to earth reference frame' '3.3 m'
% wdir_vec_mean 144x1 double 'degrees' 'average metek wind direction' 'Metek uSonic-Cage MP sonic anemometer' 'derived from hozirontal wind components after coordinate transformation from body to earth reference frame' '3.3 m'
% acoustic_temp 144x1 double 'deg C' 'acoustic temperature' 'Metek uSonic-Cage MP sonic anemometer' 'this is an acoustic temperature, not a thermodynamic temperature' '3.3 m'
% h2o_licor 144x1 double 'g/m3' 'Licor water vapor mass density' 'Licor 7500-DS' 'open-path optical gas analyzer, source data reported at 20 Hz' '3.3 m'
% co2_licor 144x1 double 'mg/m3' 'Licor CO2 gas density' 'Licor 7500-DS' 'open-path optical gas analyzer, source data reported at 20 Hz' '3.3 m'
% down_long_hemisp 144x1 double 'W/m2' 'net downward longwave flux' 'Hukseflux IR20 pyrgeometer' 'hemispheric longwave radiation' '2 m'
% down_short_hemisp 144x1 double 'W/m2' 'net downward shortwave flux' 'Hukseflux SR30 pyranometer' 'hemispheric shortwave radiation' '2 m'
% up_long_hemisp 144x1 double 'W/m2' 'net upward longwave flux' 'Hukseflux IR20 pyrgeometer' 'hemispheric longwave radiation' '2 m'
% up_short_hemisp 144x1 double 'W/m2' 'net upward shortwave flux' 'Hukseflux SR30 pyranometer' 'hemispheric shortwave radiation'
% net_radiation 144x1 double 'W/m2' 'cumulative surface radiative flux' 'SR30 and IR20 radiometers' 'combined hemispheric radiation measurements'

    if length(intersect(str2num(date),[20191113:1:20191129 20200822]))==0
      tsec30=ncread(filnam30,'time');
      hrday30(ist:ien)=tsec30/3600;
      jd30(ist:ien)=jdstr-1+nd+hrday30(ist:ien)/24;
      lat_30(ist:ien)=ncread(filnam30,'lat');%
      lon_30(ist:ien)=ncread(filnam30,'lon');%
      ta_30(ist:ien)=ncread(filnam30,'temp');%'Vaisala PTU300'
      wspd_30(ist:ien)=ncread(filnam30,'wspd_vec_mean');% 
      wdir_30(ist:ien)=ncread(filnam30,'wdir_vec_mean');% 
      mslp_30(ist:ien)=ncread(filnam30,'atmos_pressure');%
      tskn_30(ist:ien)=ncread(filnam30,'skin_temp_surface');%'surface radiometric skin temperature'
      lwd_30(ist:ien)=ncread(filnam30,'down_long_hemisp');%
      swd_30(ist:ien)=ncread(filnam30,'down_short_hemisp');%
      lwu_30(ist:ien)=ncread(filnam30,'up_long_hemisp');%
      swu_30(ist:ien)=ncread(filnam30,'up_short_hemisp');%
%      Hs_cov_30(ist:ien)=ncread(filnamtwr,'Hs_cov');%
%      HlW_cov_30(ist:ien)=ncread(filnamtwr,'HlW_cov');%
      shpbrg_30(ist:ien)=ncread(filnam30,'ship_bearing');%
      shpdis_30(ist:ien)=ncread(filnam30,'ship_distance');%
    end
    clear filnam30 tsec30
    if hrrad(1)+10/60>hrday30(end)
        ind30=length(hrday30);
    else
        ind30=find(hrday30>=hrrad(1) & hrday30<=hrrad(1)+10/60);
    end
end

  %
  if status40==1
  %read ASFS40
 %   filnam40=[asfs40_data_dir 'mosasfs40met.' data_vers '.' data_avg '.' date '.000000.nc']
    filnam40=[asfs40_data_dir 'mosseb.asfs40.' data_vers '.' data_avg '.' date '.000000.nc']
    if length(intersect(str2num(date),[20191109]))==0    
  %ncdisp(filnam40)
      tsec40=ncread(filnam40,'time');
      hrday40(ist:ien)=tsec40/3600;
      jd40(ist:ien)=jdstr-1+nd+hrday40(ist:ien)/24;
      lat_40(ist:ien)=ncread(filnam40,'lat');%
      lon_40(ist:ien)=ncread(filnam40,'lon');%
      ta_40(ist:ien)=ncread(filnam40,'temp');%'Vaisala PTU300'
      wspd_40(ist:ien)=ncread(filnam40,'wspd_vec_mean');% 
      wdir_40(ist:ien)=ncread(filnam40,'wdir_vec_mean');% 
      mslp_40(ist:ien)=ncread(filnam40,'atmos_pressure');%
      tskn_40(ist:ien)=ncread(filnam40,'skin_temp_surface');%'surface radiometric skin temperature'
      lwd_40(ist:ien)=ncread(filnam40,'down_long_hemisp');%
      swd_40(ist:ien)=ncread(filnam40,'down_short_hemisp');%
      lwu_40(ist:ien)=ncread(filnam40,'up_long_hemisp');%
      swu_40(ist:ien)=ncread(filnam40,'up_short_hemisp');%
      shpbrg_40(ist:ien)=ncread(filnam40,'ship_bearing');%
      shpdis_40(ist:ien)=ncread(filnam40,'ship_distance');%
    end
    clear filnam40 tsec40
    if hrrad(1)+10/60>hrday40(end)
        ind40=length(hrday40);
    else
        ind40=find(hrday40>=hrrad(1) & hrday40<=hrrad(1)+10/60);
    end
  end
  %
  if status50==1
  %read ASFS50
%    filnam50=[asfs50_data_dir 'mosasfs50met.' data_vers '.' data_avg '.' date '.000000.nc']
    filnam50=[asfs50_data_dir 'mosseb.asfs50.' data_vers '.' data_avg '.' date '.000000.nc']
  %ncdisp(filnam50)
    if length(intersect(str2num(date),[20200124 20200125 20200126 20200127 20200128 20200129 20200821]))==0
      tsec50=ncread(filnam50,'time');
      hrday50(ist:ien)=tsec50/3600;
      jd50(ist:ien)=jdstr-1+nd+hrday50(ist:ien)/24;
      lat_50(ist:ien)=ncread(filnam50,'lat');%
      lon_50(ist:ien)=ncread(filnam50,'lon');%
      ta_50(ist:ien)=ncread(filnam50,'temp');%'Vaisala PTU300'
      wspd_50(ist:ien)=ncread(filnam50,'wspd_vec_mean');% 
      wdir_50(ist:ien)=ncread(filnam50,'wdir_vec_mean');% 
      mslp_50(ist:ien)=ncread(filnam50,'atmos_pressure');%
      tskn_50(ist:ien)=ncread(filnam50,'skin_temp_surface');%'surface radiometric skin temperature'
      lwd_50(ist:ien)=ncread(filnam50,'down_long_hemisp');%
      swd_50(ist:ien)=ncread(filnam50,'down_short_hemisp');%
      lwu_50(ist:ien)=ncread(filnam50,'up_long_hemisp');%
      swu_50(ist:ien)=ncread(filnam50,'up_short_hemisp');%
      shpbrg_50(ist:ien)=ncread(filnam50,'ship_bearing');%
      shpdis_50(ist:ien)=ncread(filnam50,'ship_distance');%
    end
    clear filnam50 tsec50
    if hrrad(1)+10/60>hrday50(end)
        ind50=length(hrday50);
    else
        ind50=find(hrday50>=hrrad(1) & hrday50<=hrrad(1)+10/60);
    end
  end

  %
 %
shpdis_30=shpdis_30/1000;
shpdis_40=shpdis_40/1000;
shpdis_50=shpdis_50/1000;

x0(1)=0;y0(1)=0;%x,y of radar (Polarstern)
if status40==1
  L1rng=shpdis_40(ind40)/1000;L1az=mod(shpbrg_40(ind40)+180,360);mathaz=360-(L1az-90);x0(2)=L1rng*cos(mathaz*pi/180);y0(2)=L1rng*sin(mathaz*pi/180);
else
  x0(2)=NaN;y0(2)=NaN;
end
if status30==1
  L2rng=shpdis_30(ind30)/1000;L2az=mod(shpbrg_30(ind30)+180,360);mathaz=360-(L2az-90);x0(3)=L2rng*cos(mathaz*pi/180);y0(3)=L2rng*sin(mathaz*pi/180);
else
  x0(3)=NaN;y0(3)=NaN;
end
if status50==1
  L3rng=shpdis_50(ind50)/1000;L3az=mod(shpbrg_50(ind50)+180,360);mathaz=360-(L3az-90);x0(4)=L3rng*cos(mathaz*pi/180);y0(4)=L3rng*sin(mathaz*pi/180);
else
  x0(4)=NaN;y0(4)=NaN;
end


for k=kelev_sel:kelev_sel
  iray_sweep=[sweep_strt_ray(k):1:sweep_end_ray(k)];
  scan_rate_calc(iray_sweep)=(azm_sacr(iray_sweep)-azm_sacr(iray_sweep-1))./(tsec(iray_sweep)-tsec(iray_sweep-1));
  iray_sel=iray_sweep(find(scan_rate_calc(iray_sweep)>3));
  if length(iray_sel)<1
    iray_sel=iray_sweep(find(scan_rate_calc(iray_sweep)<-3));
  end
  elev_ch=num2str(round(100*elev_ang_est(k))/100);

  %calculate start time for selected ray sweep
  tsec_rstr=round(tsec_vstr+tsec(iray_sel(1)));
  minp=0;hrp=0;
  if tsec_rstr>=60
    minp=floor(tsec_rstr/60);
    tsec_rstr=tsec_rstr-minp*60;
  end
  tmin_rstr=tmin_vstr+minp;
  if tmin_rstr>=60
    hrp=floor(tmin_rstr/60);
    tmin_rstr=tmin_rstr-hrp*60;
  end
  thr_rstr=thr_vstr+hrp;
  formatSpec=['%02u'];
  time_start=[time_vol_start(1:11) num2str(thr_rstr,formatSpec) ':' num2str(tmin_rstr,formatSpec) ':' num2str(tsec_rstr,formatSpec) 'Z']
%calculate end time for selected ray sweep
  tsec_rend=round(tsec_vstr+tsec(iray_sel(end)));
  minp=0;hrp=0;
  if tsec_rend>=60
    minp=floor(tsec_rend/60);
    tsec_rend=tsec_rend-minp*60;
  end
  tmin_rend=tmin_vstr+minp;
  if tmin_rend>=60
    hrp=floor(tmin_rend/60);
    tmin_rend=tmin_rend-hrp*60;
  end
  thr_rend=thr_vstr+hrp;
  time_end=[time_vol_start(1:11) num2str(thr_rend,formatSpec) ':' num2str(tmin_rend,formatSpec) ':' num2str(tsec_rend,formatSpec) 'Z']

  nfig=nfig+1; figure(nfig)
  subplot(2,1,1),plot(tsec(iray_sel),azm_sacr(iray_sel),'r-',tsec(iray_sel),Xmt_power(iray_sel),'b-',tsec(iray_sel),n_samples(iray_sel),'g-',tsec(iray_sel),10*elev_sacr(iray_sel),'k-',tsec(iray_sel),10*scan_rate(iray_sel),'c-',tsec(iray_sel),10*scan_rate_calc(iray_sel),'c--')
  legend('azimuth','Xmt_p_o_w_e_r','samples','elevationX10','scan rate x10','scan rate calc x10')
  xlabel('seconds')
  ylabel('deg, dBm, number, deg/s')
  title(['sweep #' num2str(k) '; elev= ' elev_ch ' deg'])

  subplot(2,1,2),plot(range/1000,ht(:,k),'r-')
  xlabel('Range (km)')
  ylabel('Height (m)')
  title(['sweep #' num2str(k) '; elev= ' elev_ch ' deg'])

  %choose radar ppi configuration
  %

  %temp=((mod(90-(360-azm_sacr(iray_sel))-(180-hdg_ppi),360)))*pi/180;
  %azm1=((mod(90-(360-azm_sacr(iray_sel(1)))-(180-hdg_ppi),360)));
  %azmend=((mod(90-(360-azm_sacr(iray_sel(end)))-(180-hdg_ppi),360)));

  %temp=mod((90+azm_sacr(iray_sel)-(hdg_ppi-180)),360)*pi/180;%az =0 at stern and increases CCW; possible, but concern over cloud movement on Feb 1
  %azm1=mod((360-azm_sacr(iray_sel(1))+(hdg_ppi-180)),360);
  %azmend=mod((360-azm_sacr(iray_sel(end))+(hdg_ppi-180)),360);

  %temp=mod((90+azm_sacr(iray_sel)),360)*pi/180;%az =0 at true north and increases CCW; doesn't work with Leg 5 when PS heading is ~95 deg
  %azm1=mod((360-azm_sacr(iray_sel(1))),360);
  %azmend=mod((360-azm_sacr(iray_sel(end))),360);

  temp=mod((90-(hdg_ppi-(90-azm_sacr(iray_sel)))),360)*pi/180;%az=0 at port 90, increasing CW
  azm1=mod(hdg_ppi-(90-azm_sacr(iray_sel(1))),360);
  azmend=mod(hdg_ppi-(90-azm_sacr(iray_sel(end))),360);

  [theta rho]=meshgrid(temp,range/1000);
  [x,y] = pol2cart(theta,rho);
  htppi=ht(:,k);
  [xref yref]=size(refl);
  htarr(1:xref,1:yref)=NaN;
  for nn=1:yref
    htarr(1:xref,nn)=htppi(1:xref);
  end

  rngrng=[5 15 25 35 45];nrngrng=length(rngrng);%height rings
  for nn=1:nrngrng
    hgtrng(nn)=interp1(range,htppi,rngrng(nn)*1000);
    xrngrng(nn,1:naz)=rngrng(nn)*sin(azrng(1:naz)*pi/180);
    yrngrng(nn,1:naz)=rngrng(nn)*cos(azrng(1:naz)*pi/180);
  end

  azmrngln=[0:2:48];nazrng=length(azmrngln);
  for nn=1:nazrng
    xazrng1(nn)=azmrngln(nn)*sin(azm1*pi/180);
    yazrng1(nn)=azmrngln(nn)*cos(azm1*pi/180);
    xazrngend(nn)=azmrngln(nn)*sin(azmend*pi/180);
    yazrngend(nn)=azmrngln(nn)*cos(azmend*pi/180);
  end
  txt_fnt_size=20;%font size for data text on ppi plots
  dxt=-4;dyt=2.5; dxp=4;dyp=dyt;dxlwd=0;dylwd=-dyt;%offsets of data text
  nfig=nfig+1;f4=figure(nfig);
  fleft=0.05;fbot=2;fwidth=23.4;fheight=20.9;%positioning of figure windows
  f4.Units='centimeters';f4.Position=[fleft fbot fwidth fheight];
  arr1=refl(:,iray_sel);v1=[-25:2:20];%arr1(find(arr1)<v1(1))=NaN;
  snharr=sig2noise_h(:,iray_sel);
  arr0=arr1;%save original array
  htarr1=htarr(:,iray_sel);
  [xa1 ya1]=size(arr1);
  for kk=1:xa1
%    arr1(kk,find(arr1(kk,:)<(mdrng(kk)+ref_edit_offset)))=NaN;
    if sn_thresh==-999
      arr1(kk,find(arr0(kk,:)<(noise_vs_range(kk)+ref_edit_offset)))=NaN;  %edit reflectivity with noise_vs_range reflectivity threshold functions
    elseif abs(sn_thresh)<11
      arr1(kk,find(snharr(kk,:)<sn_thresh))=NaN;  %edit reflectivity based on horizontal S/N
    end
    %arr1(kk,find(arr1(kk,:)<-10))=NaN;
  end
  arr1=arr1+refl_calib; %add in calibration offset for Ka-SACR
  %[C,h]=contourf(tsec(iray_sel),range/1000,arr1,v1);clabel(C,h);colormap jet
 % [C,h]=contourf(azm_sacr(iray_sel),range/1000,arr1,v1);clabel(C,h);colormap jet
 % [C,h]=contourf(x,y,arr1,v1,'LineStyle','none');%clabel(C,h);colormap jet
  contourf(x,y,arr1,v1,'LineStyle','none');%clabel(C,h);colormap jet
  colorbar('EastOutside');%colormap jet
  hold on
    rngfntsz=14; %fontsize for range ring distances & heights
     for nn=1:nrngrng
       plot(xrngrng(nn,:),yrngrng(nn,:),'k--','LineWidth',1)
 %      text(xrngrng(nn,315)-1,yrngrng(nn,315),num2str(rngrng(nn)),'FontSize',rngfntsz);
 %      text(xrngrng(nn,45)-1,yrngrng(nn,45),num2str(round(hgtrng(nn),0)),'Color','magenta','FontSize',rngfntsz);
        text(xrngrng(nn,45)-1,yrngrng(nn,45),num2str(round(hgtrng(nn),0)),'Color','black','FontSize',rngfntsz);
       plot(xazrng1,yazrng1,'k-');%outline blocked azimuth range
       plot(xazrngend,yazrngend,'k-');
     end
     xscl=10.0;yscl=1.0*xscl*(max(max(y))-min(min(y)))/(max(max(x))-min(min(x)));
     text(x0(1),y0(1),'PS','FontSize',txt_fnt_size+2,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
     if statusMC==1
    % text(x0(1)-3,y0(1)+2,num2str(round(tair_ppi,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
    % text(x0(1),y0(1)-2,num2str(round(cldbas_ppi,0)),'FontSize',txt_fnt_size,'Color','green','HorizontalAlignment','center','VerticalAlignment','middle');
     text(x0(1)+dxt,y0(1)+dyt,num2str(round(ta_6m(indtwr),1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
    % text(x0(1)+dxlwd,y0(1)+dylwd,num2str(round(lwd_arm_mc(indtwr),0)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle'); 
     if press_ppi>=1000
       text(x0(1)+dxp,y0(1)+dyp,num2str(round(press_ppi-1000,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     else
       text(x0(1)+dxp,y0(1)+dyp,num2str(round(press_ppi-900,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     end
     %flg=barb3(x0(1),y0(1),wsp_ppi,wdr_ppi,xscl,yscl,2);
     flg=barb3(x0(1),y0(1),wspd_6m(indtwr),wdir_6m(indtwr),xscl,yscl,2);
     end
     
     if status40==1
       text(x0(2),y0(2),'L1','FontSize',txt_fnt_size+2,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(2)+dxt,y0(2)+dyt,num2str(round(ta_40(ind40),1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     %  text(x0(2)+dxlwd,y0(2)+dylwd,num2str(round(lwd_40(ind40),0)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_40(ind40)>=1000
         text(x0(2)+dxp,y0(2)+dyp,num2str(round(mslp_40(ind40)-1000,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
         text(x0(2)+dxp,y0(2)+dyp,num2str(round(mslp_40(ind40)-900,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       end
       flg=barb3(x0(2),y0(2),wspd_40(ind40),wdir_40(ind40),xscl,yscl,2);
     end

     if status30==1
       text(x0(3),y0(3),'L2','FontSize',txt_fnt_size+2,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(3)+dxt,y0(3)+dyt,num2str(round(ta_30(ind30),1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
      % text(x0(3)+dxlwd,y0(3)+dylwd,num2str(round(lwd_30(ind30),0)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_30(ind30)>=1000
         text(x0(3)+dxp,y0(3)+dyp,num2str(round(mslp_30(ind30)-1000,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
         text(x0(3)+dxp,y0(3)+dyp,num2str(round(mslp_30(ind30)-900,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       end
       flg=barb3(x0(3),y0(3),wspd_30(ind30),wdir_30(ind30),xscl,yscl,2);
     end

     if status50==1
       text(x0(4),y0(4),'L3','FontSize',txt_fnt_size+2,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(4)+dxt,y0(4)+dyt,num2str(round(ta_50(ind50),1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
      % text(x0(4)+dxlwd,y0(4)+dylwd,num2str(round(lwd_50(ind50),0)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_50(ind50)>=1000
         text(x0(4)+dxp,y0(4)+dyp,num2str(round(mslp_50(ind50)-1000,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
          text(x0(4)+dxp,y0(4)+dyp,num2str(round(mslp_50(ind50)-900,1)),'FontSize',txt_fnt_size,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');        
       end
       flg=barb3(x0(4),y0(4),wspd_50(ind50),wdir_50(ind50),xscl,yscl,2);
     end

  hold off
  titl_time=[time_start(1:4) time_start(6:7) time_start(9:10) '_' time_start(12:13) time_start(15:16) '_elev' num2str(round(100*str2num(elev_ch))) '_thrshm' num2str(abs(sn_thresh))]
  title(['Reflectivity (dBZ) ' time_start(1:4) time_start(6:7) time_start(9:10) ' ' time_start(12:13) time_start(15:16) '-'  time_end(12:13) time_end(15:16) ' UTC; elev= ' elev_ch])
  %xlabel('seconds')
  xlabel('distance E (km)')
  ylabel('distance N (km)')
  xmn=-35;xmx=35;ymn=-35;ymx=35; %shrink domain size
  xlim([xmn xmx]);ylim([ymn ymx])
  fntsz=18; %axis text font
  set(gca,'fontsize',fntsz,'FontWeight','bold','LineWidth',2,'TickDir','in','XMinorTick','on','YMinorTick','on')


  nfig=nfig+1;f5=figure(nfig);
  fleft=23.5;fbot=2;fwidth=23.4;fheight=20.9;%positioning of figure windows
  f5.Units='centimeters';f5.Position=[fleft fbot fwidth fheight];
  arr2=rad_vel(:,iray_sel);v2=[-12:1:12];%arr2(find(abs(arr2))>12)=NaN;
  for kk=1:xa1
    if sn_thresh_vel==-999
      arr2(kk,find(arr0(kk,:)<(noise_vs_range(kk)+ref_edit_offset)))=NaN;
    elseif abs(sn_thresh_vel)<11
      arr2(kk,find(snharr(kk,:)<sn_thresh_vel))=NaN;  %edit reflectivity based on horizontal S/N
    end
  end
  %[C,h]=contourf(tsec(iray_sel),range/1000,arr2,v2);caxis([v2(1) v2(end)]);clabel(C,h,v2);colorbar('EastOutside');colormap jet
  %[C,h]=contourf(azm_sacr(iray_sel),range/1000,arr2,v2);caxis([v2(1) v2(end)]);clabel(C,h,v2);colorbar('EastOutside');colormap jet
  contourf(x,y,arr2,v2,'LineStyle','none');%caxis([v2(1) v2(end)]);%clabel(C,h,v2);
  colorbar('EastOutside');%colormap jet
  hold on
 %   [C,h]=contour(tsec(iray_sel),range/1000,arr2,[0,0],'k-','LineWidth',2);%clabel(C,h);
 %    [C,h]=contour(azm_sacr(iray_sel),range/1000,arr2,[0,0],'k-','LineWidth',2);%clabel(C,h);
    [C,h]=contour(x,y,arr2,[0,0],'k-','LineWidth',2);%clabel(C,h);
  hold off
  title(['Radial Velocity (m/s) ' time_start(1:4) time_start(6:7) time_start(9:10) ' ' time_start(12:13) time_start(15:16) '-'  time_end(12:13) time_end(15:16) 'UTC; elev= ' elev_ch])
  %xlabel('seconds')
  xlabel('distance E (km)')
  ylabel('distance N (km)')
    hold on
     for nn=1:nrngrng
       plot(xrngrng(nn,:),yrngrng(nn,:),'k--')
       text(xrngrng(nn,300)-1,yrngrng(nn,300),num2str(rngrng(nn)));
       text(xrngrng(nn,100)-1,yrngrng(nn,100),num2str(round(hgtrng(nn),0)),'Color','red');
       plot(xazrng1,yazrng1,'k-');
       plot(xazrngend,yazrngend,'k-');
     end
     xscl=10.0;yscl=1.0*xscl*(max(max(y))-min(min(y)))/(max(max(x))-min(min(x)));
     text(x0(1),y0(1),'PS','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
    % text(x0(1)-3,y0(1)+2,num2str(round(tair_ppi,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
    % text(x0(1),y0(1)-2,num2str(round(cldbas_ppi,0)),'FontSize',12,'Color','green','HorizontalAlignment','center','VerticalAlignment','middle');
     text(x0(1)-3,y0(1)+2,num2str(round(ta_6m(indtwr),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     text(x0(1),y0(1)-2,num2str(round(lwd_arm_mc(indtwr),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle'); 
     if press_ppi>=1000
       text(x0(1)+3,y0(1)+2,num2str(round(press_ppi-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     else
       text(x0(1)+3,y0(1)+2,num2str(round(press_ppi-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     end
     %flg=barb3(x0(1),y0(1),wsp_ppi,wdr_ppi,xscl,yscl,2);
     flg=barb3(x0(1),y0(1),wspd_6m(indtwr),wdir_6m(indtwr),xscl,yscl,2);
     
     if status40==1
       text(x0(2),y0(2),'L1','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(2)-3,y0(2)+2,num2str(round(ta_40(ind40),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(2),y0(2)-2,num2str(round(lwd_40(ind40),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_40(ind40)>=1000
         text(x0(2)+3,y0(2)+2,num2str(round(mslp_40(ind40)-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
         text(x0(2)+3,y0(2)+2,num2str(round(mslp_40(ind40)-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       end
       flg=barb3(x0(2),y0(2),wspd_40(ind40),wdir_40(ind40),xscl,yscl,2);
     end

     if status30==1
       text(x0(3),y0(3),'L2','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(3)-3,y0(3)+2,num2str(round(ta_30(ind30),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(3),y0(3)-2,num2str(round(lwd_30(ind30),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_30(ind30)>=1000
         text(x0(3)+3,y0(3)+2,num2str(round(mslp_30(ind30)-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
         text(x0(3)+3,y0(3)+2,num2str(round(mslp_30(ind30)-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       end
       flg=barb3(x0(3),y0(3),wspd_30(ind30),wdir_30(ind30),xscl,yscl,2);
     end

     if status50==1
       text(x0(4),y0(4),'L3','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(4)-3,y0(4)+2,num2str(round(ta_50(ind50),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(4),y0(4)-2,num2str(round(lwd_50(ind50),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_50(ind50)>=1000
         text(x0(4)+3,y0(4)+2,num2str(round(mslp_50(ind50)-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
          text(x0(4)+3,y0(4)+2,num2str(round(mslp_50(ind50)-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');        
       end
       flg=barb3(x0(4),y0(4),wspd_50(ind50),wdir_50(ind50),xscl,yscl,2);
     end

  hold off

  %lat_range=double(90-range/1000);
  %temp=mod(azm_sacr(iray_sel)-(180-hdg_ppi),360);
  %lon_az=double(temp);clear temp
  %nfig=nfig+1;figure(nfig)
  clear arr1
  %arr1=double(refl(:,iray_sel));v1=[-18:2:20];

%map_txt1=['AMSR2 Ice Conc (0-100%): Date: 2015' chimo chdy ' (' num2str(jday) ')'];
%map_txt2=['Sikuliaq track (magenta: Sea State; green: AMSR2 date)'];
%worldmap([45 90],[0 360])
%load coast
%[c,hh]=contourfm(lat_range,lon_az,arr1,v1);
%caxis([0 100])
%contourcbar %toggle to match model output plots
%contourfm(double(loc.latitude),double(loc.longitude),double(file.sea_ice_concentration*.01),[0:10:100])
%plotm(lat,long,'Color','r','LineWidth',3)
%hold on
%  plotm(lat_ref(i10_shp_all),lon_ref(i10_shp_all),'Color','m','LineWidth',1) %entire ship track within domain
%  if length(i10_shp)>0
%    plotm(lat_ref(i10_shp),lon_ref(i10_shp),'Color','g','LineWidth',2)  %ship track for just this day
%  end
%hold off
%textm(lat_ref(ishv),lon_ref(ishv),'x','Color','g','HorizontalAlignment','center','VerticalAlignment','middle','FontSize',14,'FontWeight','bold')
%[c,hh]=contourm(file.XLAT,file.XLONG,file.PSFC/100,[960:1:1040],'m');
%clabelm(c,hh,[960:4:1040],'LabelSpacing',288)
%dytxt=(lat_end-lat_str)*0.05;
%dxtxt=(lon_end-lon_str)*0.05;
%textm(lat_str+0.6*dytxt,lon_str+dxtxt,map_txt1,'FontSize',14,'Color','r')
%textm(lat_str+1.5*dytxt,lon_str+dxtxt,map_txt2,'FontSize',14,'Color','r')

%  nfig=nfig+1;figure(nfig)
 % clear arr2
%  arr2=double(rad_vel(:,iray_sel));v2=[-12:3:12];
 % worldmap([45 90],[0 360])
%load coast
 % [c,hh]=contourfm(lat_range,lon_az,arr2,v2);
end

nfig2=89;
nyqveltmd=median(nyqvel(iray_sel));
[irngmx iazmx]=size(arr2);
radvel(1:360)=wsp_ppi*sin(([0:359]-wdr_ppi)*pi/180);

%plot radial velocity vs range for nbeam beams
nfig2=nfig2+1;f3=figure(nfig2);
f3.Units='centimeters';f3.Position=[1 23 22 15];
nbeam=6;
azstr=1;delaz=floor((iazmx-azstr)/(nbeam-1));iazpl=azstr-delaz;
for ib=1:nbeam
  iazpl=iazpl+delaz;
  subplot(nbeam,1,ib),plot(range/1000,arr2(:,iazpl),'r.',[range(1)/1000 range(end)/1000],[nyqveltmd nyqveltmd],'k:',...
      [range(1)/1000 range(end)/1000],[-nyqveltmd -nyqveltmd],'k:',[range(1)/1000 range(end)/1000],[0 0],'k--');
  xlabel('range distance (km)');ylabel('radial velocity (m/s)')
  azang=median(theta(:,iazpl))*(180/pi);
  text(5,4,['Azm= ' num2str(round(azang,1))]);
  hold on
    iazwd=mod(iazpl,360);
    plot(0,radvel(iazwd),'gx')
  hold off
end

arr2ed(1:irngmx,1:iazmx)=NaN;
iazpl=azstr-1;
nyqveltmd2=2*nyqveltmd;

for ib=1:iazmx
  iazpl=iazpl+1;
  iazwd=mod(iazpl,360);rvelgs=radvel(iazwd);%radial velocity guess based on PS wind vector
  for ii=1:irngmx
    diff=arr2(ii,iazpl)-rvelgs;
    if diff>nyqveltmd
      arr2ed(ii,iazpl)=arr2(ii,iazpl)-nyqveltmd2;
    elseif diff<-nyqveltmd
      arr2ed(ii,iazpl)=arr2(ii,iazpl)+nyqveltmd2;
    else
      arr2ed(ii,iazpl)=arr2(ii,iazpl);
    end
    iist=max([1 ii-30]);
    rvelgs=nanomed(arr2ed(iist:ii,iazpl));
  end
end
nfig2=nfig2+1;f3=figure(nfig2);
f3.Units='centimeters';f3.Position=[23 23 22 15];
iazpl=azstr-delaz;
for ib=1:nbeam
  iazpl=iazpl+delaz;
  iazwd=mod(iazpl,360);rvelgs=radvel(iazwd);%radial velocity guess based on PS wind vector
  subplot(nbeam,1,ib),plot(range/1000,arr2(:,iazpl),'r.',range/1000,arr2ed(:,iazpl),'b.',[range(1)/1000 range(end)/1000],[nyqveltmd nyqveltmd],'k:',...
      [range(1)/1000 range(end)/1000],[-nyqveltmd -nyqveltmd],'k:',[range(1)/1000 range(end)/1000],[0 0],'k--');
  xlabel('range distance (km)');ylabel('radial velocity (m/s)')
  azang=median(theta(:,iazpl))*(180/pi);
  text(5,4,['Azm= ' num2str(round(azang,1))]);
  hold on
    iazwd=mod(iazpl,360);
    plot(0,radvel(iazwd),'gx')
  hold off
end


%plot radial velocity vs azimuth for nrng ranges
nfig2=nfig2+1;f3=figure(nfig2);
f3.Units='centimeters';f3.Position=[45 23 22 15];
nrng=6;
rngstr=2;delrng=floor((irngmx-rngstr)/(nrng-1));irngpl=rngstr-delrng;
for ir=1:nrng
  irngpl=irngpl+delrng;
  subplot(nrng,1,ir),plot(azm_sacr(iray_sel),arr2ed(irngpl,:),'r.',[azm_sacr(iray_sel(1)) azm_sacr(iray_sel(end))],[nyqveltmd nyqveltmd],'k:',...
      [azm_sacr(iray_sel(1)) azm_sacr(iray_sel(end))],[-nyqveltmd -nyqveltmd],'k:',[azm_sacr(iray_sel(1)) azm_sacr(iray_sel(end))],[0 0],'k--');
  xlabel('azimuth (deg)');ylabel('radial velocity (m/s)')
  rangpl=median(rho(irngpl,:));
  ymin=floor(min([-nyqveltmd min(radvel) min(arr2ed(irngpl,:)) ]));ymax=ceil(max([nyqveltmd max(radvel) max(arr2ed(irngpl,:))]));dely=ymax-ymin;
  txty1=ymax-1*dely/10;
  txty2=ymax-2*dely/10;
  text(floor(azm_sacr(iray_sel(1)))+5,txty1,['Range= ' num2str(round(rangpl,1)) ' km']);
  htrng=interp1(range,htppi,rangpl*1000);
  text(floor(azm_sacr(iray_sel(1)))+5,txty2,['Height= ' num2str(round(htrng,0)) ' m']);
  ylim([ymin ymax])
%  xlim([floor(azm_sacr(iray_sel(1))) ceil(azm_sacr(iray_sel(end)))])
  xlim([0 360])
  if htrng<50 & rangpl<5
    hold on
      plot([0:359],radvel,'g-')
    hold off
  end
end

%plot edited radial velocities
  nfig=nfig+1;f6=figure(nfig);
  fleft=46.5;fbot=2;fwidth=23.4;fheight=20.9;%positioning of figure windows
  f6.Units='centimeters';f6.Position=[fleft fbot fwidth fheight];
  %arr2=rad_vel(:,iray_sel);v2=[-12:1:12];%arr2(find(abs(arr2))>12)=NaN;
  %for kk=1:xa1
  %  arr2(kk,find(arr0(kk,:)<(noise_vs_range(kk)+ref_edit_offset)))=NaN;
  %end
  %[C,h]=contourf(tsec(iray_sel),range/1000,arr2,v2);caxis([v2(1) v2(end)]);clabel(C,h,v2);colorbar('EastOutside');colormap jet
  %[C,h]=contourf(azm_sacr(iray_sel),range/1000,arr2,v2);caxis([v2(1) v2(end)]);clabel(C,h,v2);colorbar('EastOutside');colormap jet
  contourf(x,y,arr2ed,v2,'LineStyle','none');%caxis([v2(1) v2(end)]);%clabel(C,h,v2);
  colorbar('EastOutside');%colormap jet
  hold on
 %   [C,h]=contour(tsec(iray_sel),range/1000,arr2,[0,0],'k-','LineWidth',2);%clabel(C,h);
 %    [C,h]=contour(azm_sacr(iray_sel),range/1000,arr2,[0,0],'k-','LineWidth',2);%clabel(C,h);
    [C,h]=contour(x,y,arr2ed,[0,0],'k-','LineWidth',2);%clabel(C,h);
  hold off
  title(['Radial Velocity (m/s) ' time_start(1:4) time_start(6:7) time_start(9:10) ' ' time_start(12:13) time_start(15:16) '-'  time_end(12:13) time_end(15:16) 'UTC; elev= ' elev_ch])
  %xlabel('seconds')
  xlabel('distance E (km)')
  ylabel('distance N (km)')
  hold on
     for nn=1:nrngrng
       plot(xrngrng(nn,:),yrngrng(nn,:),'k--')
       text(xrngrng(nn,300)-1,yrngrng(nn,300),num2str(rngrng(nn)));
       text(xrngrng(nn,100)-1,yrngrng(nn,100),num2str(round(hgtrng(nn),0)),'Color','red');
       plot(xazrng1,yazrng1,'k-');
       plot(xazrngend,yazrngend,'k-');
     end
     xscl=10.0;yscl=1.0*xscl*(max(max(y))-min(min(y)))/(max(max(x))-min(min(x)));
     text(x0(1),y0(1),'PS','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
    % text(x0(1)-3,y0(1)+2,num2str(round(tair_ppi,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
    % text(x0(1),y0(1)-2,num2str(round(cldbas_ppi,0)),'FontSize',12,'Color','green','HorizontalAlignment','center','VerticalAlignment','middle');
     text(x0(1)-3,y0(1)+2,num2str(round(ta_6m(indtwr),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     text(x0(1),y0(1)-2,num2str(round(lwd_arm_mc(indtwr),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle'); 
     if press_ppi>=1000
       text(x0(1)+3,y0(1)+2,num2str(round(press_ppi-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     else
       text(x0(1)+3,y0(1)+2,num2str(round(press_ppi-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
     end
     %flg=barb3(x0(1),y0(1),wsp_ppi,wdr_ppi,xscl,yscl,2);
     flg=barb3(x0(1),y0(1),wspd_6m(indtwr),wdir_6m(indtwr),xscl,yscl,2);
     
     if status40==1
       text(x0(2),y0(2),'L1','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(2)-3,y0(2)+2,num2str(round(ta_40(ind40),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(2),y0(2)-2,num2str(round(lwd_40(ind40),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_40(ind40)>=1000
         text(x0(2)+3,y0(2)+2,num2str(round(mslp_40(ind40)-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
         text(x0(2)+3,y0(2)+2,num2str(round(mslp_40(ind40)-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       end
       flg=barb3(x0(2),y0(2),wspd_40(ind40),wdir_40(ind40),xscl,yscl,2);
     end

     if status30==1
       text(x0(3),y0(3),'L2','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(3)-3,y0(3)+2,num2str(round(ta_30(ind30),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(3),y0(3)-2,num2str(round(lwd_30(ind30),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_30(ind30)>=1000
         text(x0(3)+3,y0(3)+2,num2str(round(mslp_30(ind30)-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
         text(x0(3)+3,y0(3)+2,num2str(round(mslp_30(ind30)-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       end
       flg=barb3(x0(3),y0(3),wspd_30(ind30),wdir_30(ind30),xscl,yscl,2);
     end

     if status50==1
       text(x0(4),y0(4),'L3','FontSize',14,'Color','red','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(4)-3,y0(4)+2,num2str(round(ta_50(ind50),1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       text(x0(4),y0(4)-2,num2str(round(lwd_50(ind50),0)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       if mslp_50(ind50)>=1000
         text(x0(4)+3,y0(4)+2,num2str(round(mslp_50(ind50)-1000,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');
       else
          text(x0(4)+3,y0(4)+2,num2str(round(mslp_50(ind50)-900,1)),'FontSize',12,'Color','blue','HorizontalAlignment','center','VerticalAlignment','middle');        
       end
       flg=barb3(x0(4),y0(4),wspd_50(ind50),wdir_50(ind50),xscl,yscl,2);
     end

  hold off

  if save_rad_out==1
    filnam1=[output_dir_refl 'SACR_refl_' titl_time]
    print(['-f' num2str(nfig_refl)],filnam1,'-dpng')
    filnam2=[output_dir_vel 'SACR_velrw_' titl_time]
    print(['-f' num2str(nfig_velrw)],filnam2,'-dpng')
    filnam3=[output_dir_vel 'SACR_velda_' titl_time]
    print(['-f' num2str(nfig_velda)],filnam3,'-dpng')
  end
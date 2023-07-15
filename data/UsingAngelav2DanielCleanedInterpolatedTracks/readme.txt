Buoys are deployed during MOSAiC in an array, the Distributed Network (DN), to study horizontal deformation of the sea ice pack. The DN can be split into sub arrays, on a variety of length scales. Each buoy array (processed to date) is documented in a seperate subsection below call Sub Arrays. GPS position data is provided in .csv files, available at the Arctic Data Center. Strain-rate data for arrays is provided in .csv files.

This directory contains the arrays that Jenny Hutchings chose for her 2020 AGU and 2021 EGU presentations. The DN was triangulated by hand based on the buoy configuration on June 20 2020, only including buoys that were deployed by November 20 2019 and did not fail during the full period from November to June 20. Arrays that became overly skewed during the time were removed and not used. 

Strain-rate Data
================

During the time that buoy arrays maintained a shape suitable for calculation of horizontal deformation this data is provided. Strain rate is calculated for buoys array following the method of Hutchings et al. [2012], errata [2018] fixes a sign error and we follow that correction. 

Strain-rate data filename convention: strainrate_MOSAiC_DN_arrayid_n.csv
where arrayid is a lable identifying the ring of buoys, and n is an identifier listing the number of buoys in the array.

File format for strainrate data: CSV with columns:
Decimal day of year (0 at 00Z on Oct 4th 2019 except Ltriangle starts Oct 15th 0Z)
Mean Latitude, centre of the array, decimal
Mean Longitude, centre of the array, decimal
Divergence rate (/s)
Maximum Shear Strain rate (/s)
Vorticity rate (/s)
Pure Shear rate (/s)
Normal Shear rate (/s)
Area of buoy array (m2)
Flag
Shape Factor, ratio of largest and smallest distances across the buoy array.

The flag is set to various values depending on why data is not acceptable.
999 Velocity greater than 1 m/s or buoy array area = 0.
998 Buoy array area changes by more that 1 km2 over 1 hour.
997 Buoy array area < 1km2.
995 Data flagged for 1 time step either side of time when buoy array turns inside out (Only used for three buoy arrays)
994 Interpolation of at least 1 buoy position in array is more than 6 hours, or data is missing for one buoy at this timestep. This value is added to any flag found above.
 
For shape factor > 2, sub-mesoscale array strain rates can be considered inaccurate.

Please note that the strain rates are calculated using a green's theorem method, and line integrals are discretised around the buoy array in a right hand sense. However, should the buoys in the array change positions (for example the array can flip inside out), strain rate estimates may have the wrong sign. In particular, when an array flips inside out, the area becomes negative and strain rates have the wrong sign. We have not corrected for this in these data sets, except for arrays with only 3 buoys. These events can be identified as at the time of the flip the buoy array becomes skewed, shape factor becomes large and area becomes negative. 

It is possible to calculate strain rates for many subset arrays, for example see Stanton et al. 2012, Martini et al. [2016]. Should you be interested in such data please contact Jenny Hutchings (jhutchings@coas.oregonstate.edu). 


Sub Arrays
==========
MOSAiC_DN_subarrays_nov2020.pptx documents the arrays for which deformation is calculated.

yellow - Outer ring of three buoys outside of the DN
orange - Outer edge of the DN
green - 20km ring
blue - 10km ring

S1 through S46 - Buoy Triads and cover the DN region. 

S50 through S 56 - Medium sized buoy triads covering the DN region.

S57 and S 58 - Two large triangles spliting the DN in half.

Ltriangle - The triangle with L sites at each vertex. 



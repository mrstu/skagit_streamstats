
Overview
========

This repository consists of tools for computing hydrological statistics of extreme streamflows.  

The statistical code was largely developed by Hamlet and the timing code by Stumbaugh.

Included here are components that were applied for Skagit River basin project(s) collaborations
between Barandaoda, Raymond, Istanbulluoglu, Stumbaugh, and Hamlet.

Structure of Project I/O
========================

From daily time step source data, annual extreme event timing and magnitudes are tabulated.  Quantiles are derived using an unbiased estimator (Cunnane).

The source data may include time series for numerous stations, Global Climate Models (GCM), Representative Concentration Pathways.
Filenames uniquely identify the time series variants.  Within a source collection, it is assumed that individual time series share a common production method.  
Shared production is not critical, but if it is not shared, independent handling/tracking will de needed (or need to be added on). 

A collection of multiple time series with shared production shall be located in a unique directory,

::

$sourceUnique/

Within the source directory, processing will track across the set of time series with a naming pattern like, 

::

$sourceUnique/$stationName.$gcm.$rcp.$suffix

For a given time series, annual peak flood flow and annual low flow statistics and timing tables will be generated.

::

$sourceUnique.flood.$yearInitial-$yearFinal/$stationName.$gcm.$rcp.$suffix.{peak_flow_date,quantiles,strflw_flood_stats}
$sourceUnique.low.$yearInitial-$yearFinal/$stationName.$gcm.$rcp.$suffix.{7q10_cal_date,7q10_flow_date,quantiles,strflw_7q10_stats}

Managing Project(s)
===================

run.{bclff, nobc_lff, skaglo}/

master.bsh <-- setup.{1980-2010,2010-2040,2035-2065,2070-2099}.cfg

#. run.bsh <-- lib/sumoutput_{flood,7q10}_stats``*``.c

   * read setup config files
   * compile
   * loop across input times series and compute {flood,low} statistics
   
#. summ_stats.bsh

   * find {flood,low} stat outputs
   * extract distribution type 1 GEV-L for low  
   * extract distribution type 5 LN3 for flood
   * output flat file for flow type and time period (all stations/gcms/rcps)
   
#. scripts/bothex_{tables,tables_pctchg}.py

   * bothex_tables.py -- create station x gcm table for (flowtype/time/rcp)
   * bothex_tables_pctchg.py -- calculate percent changes relative to historic reference

Timing Visualizations
=====================

Primary

* timing/plot_tdeltaEns.bsh <-- timing/plot_yrpeak_enstops.py
* timing/plot_yrcum_stations.bsh <-- timing/panel_yrcum.py
* timing/plot_yrcum_stn-pers-gcms.bsh  <-- timing/panel_yrcum_stnper.py

Secondary

* timing/plot_yrpeak_support.py
* timing/plot_yrpeak_{gcmtops,gcmrawbc,enstops}.py
* timing/panel_yrcum{.py,_station.py,_stnper.py}

Primary Peak Flows / Low Flow Output Files
==========================================

* quantiles (peak, low) <rank, flow, probability exceedance>
* peak_flow_date (peak) <nrec, flow, wyday, year, month, day>
* 7q10_flow_date (low) <nrec, flow, wy day, wy day of month start, day in month, (nummonths)>
* 7q10_cal_date (low) <year, month, day, wy, (nummonths), flow>
* strflw_flood_stats (peak) <fileid, "dist", distnum, estimated peak flow magnitude for recurrence interval (1 10 20 50 100 200 500)>
* strflw_7q10_stats (low) <fileid, "dist", distnum, estimated 7-day averaged low flow magnitude for recurrence interval (500 200 100 50 20 10 2)>

Example pipeline
================

Station (Diablo), GCM (bcc-csm1-1-m), RCP (rcp45) in collection (outputs_Feb_1960_2099lowflow).  Compute statistics for 1980-2010.

outputs_Feb_1960_2099lowflow/Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out

::

   <year, month, day, flow>
   1961 10 2 2872.5
   1961 10 3 2073.8
   1961 10 4 1824.6
   ...
   2099 9 29 844.03
   2099 9 30 814.36
   
outputs_Feb_1960_2099lowflow.flood.1980-2010/Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out_peak_flow_date

::

   <nrec, flow, wyday, year, month, day>
   1 62170.0 88 1980 12 27
   2 18237.0 278 1982 7 4
   3 42151.0 287 1983 7 13
   ...
   28 18895.0 240 2008 5 27
   29 21417.0 246 2009 6 3
   30 13512.0 255 2010 6 12

outputs_Feb_1960_2099lowflow.low.1980-2010/Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out_7q10_flow_date

::

   <nrec, flow, wy day, wy day of month start, day in month, (nummonths)>
   1 938.070007 1 0 1 12
   2 1288.901611 132 123 9 12
   3 649.850159 353 335 18 12

outputs_Feb_1960_2099lowflow.low.1980-2010/Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out_7q10_cal_date

::

   <year, month, day, wy, (nummonths), flow>
   1980 11 1 1981 12 938.070007
   1982 3 9 1982 12 1288.901611
   1983 10 18 1983 12 649.850159
   ...
   
outputs_Feb_1960_2099lowflow.flood.1980-2010/Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out_quantiles

::

   <rank, flow, probability exceedance>
  30  9267.4 0.98013
  29 13512.0 0.94702
  28 14170.0 0.91391
  ...
   3 51580.0 0.08609
   2 62051.0 0.05298
   1 62170.0 0.01987

outputs_Feb_1960_2099lowflow.flood.1980-2010/Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out_strflw_flood_stats

* col1="Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out"
* col4-10: estimated peak flow magnitude for recurrence interval (1 10 20 50 100 200 500)
* dist 0-4 (index for type of fit):

  #. GEV distribution using L moments (parameters for gamma function estimator see Handbook of hydrology pp 18.18)
  #. GEV parameters based on LH2 moments (Wang 1997)
  #. GEV parameters based on LH4 moments (Wang 1997)
  #. calculate EV1 parameters based on L moments
  #. LN Type 3 (???)

::

   $col1 dist 0  9640.8 42563.0 53763.7 72011.0 89129.2 109819.0 143994.3
   $col1 dist 1 -3038.7 44471.2 52079.1 61329.3 67844.7 74001.9 81643.6 
   $col1 dist 2 -34607.1 46503.4 52580.9 58345.2 61509.5 63930.2 66287.4
   $col1 dist 3  4091.1 43745.5 51301.8 61082.7 68412.0 75714.7 85349.2 
   $col1 dist 4  7814.0 42598.5 50617.8 61465.8 69876.9 78428.5 89854.1 (LN3 used preferentially for peak flows)
   
outputs_Feb_1960_2099lowflow.low.1980-2010/Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out_strflw_7q10_stats 
   
   * col1="Diablo_output__glacier.bcc-csm1-1-m__streamflow.rcp45.daily.2.wy.day.bc.fx.aa.out"
   * col4-10: estimated 7-day averaged low flow magnitude for recurrence interval (500 200 100 50 20 10 2)

::

   $col1 dist 0 17.745857 80.233597 133.382034 193.193848 286.543304 373.394928 711.771484 (GEV L-moments used preferentially for most low flows)
   $col1 dist 1 -315.492065 -196.993652 -100.094559 4.706165 159.355988 293.578156 729.729736 
   $col1 dist 2 -1443.068481 -1136.786377 -897.201904 -649.409912 -306.023529 -30.450373 706.221863
   $col1 dist 3 179.410568 215.498642 247.219482 284.124664 344.500031 404.036133 675.645813 
   $col1 dist 4 194.625549 220.433929 245.012024 275.541107 329.154266 385.466217 667.988281


Aggregate Results by Distribution
=================================

Floods (**dist 4 = LN3**)

* sumtab_outputs_Feb_1960_2099lowflow.flood.1980-2010.txt
* sumtab_outputs_Feb_1960_2099noBC_lowflow.flood.1980-2010.txt

Lowflow (**dist 0 = GEV-L**)

* sumtab_outputs_Feb_1960_2099lowflow.low.1980-2010.txt
* sumtab_outputs_Feb_1960_2099noBC_lowflow.low.1980-2010.txt


For all (stations, gcms), pool by stat/rcp/T_recurrence triplet
===============================================================

Value and percent change tables

* tables.outputs_Feb_1960_2099lowflow.flood/
* tables.outputs_Feb_1960_2099lowflow.flood.pctchg/
* tables.outputs_Feb_1960_2099lowflow.low/
* tables.outputs_Feb_1960_2099lowflow.low.pctchg/
* tables.outputs_Feb_1960_2099noBC_lowflow.flood/
* tables.outputs_Feb_1960_2099noBC_lowflow.flood.pctchg/
* tables.outputs_Feb_1960_2099noBC_lowflow.low/
* tables.outputs_Feb_1960_2099noBC_lowflow.low.pctchg/

Example tables for 1-year and 100-year flood flows:

tables.outputs_Feb_1960_2099lowflow.flood/table-flood_outputs_Feb_1960_2099lowflow.flood.1980-2010_rcp45_p1-y1.csv

::

   ,CCSM4,CNRM-CM5,CSIRO-Mk-3-6-0,CanESM2,HadGEM2-CC365,HadGEM2-ES365,IPSL-CM5A-MR,MIROC5,NorESM1-M,bcc-csm1-1-m
   Diablo,8092.0,7819.0,7966.7,7794.4,8092.3,6711.6,7669.0,8152.8,8457.1,7814.0
   Gorge,8801.1,8485.0,8625.6,8509.5,8738.8,7291.2,8266.5,8811.6,9155.5,8522.5
   Newhalem2Marblemount,3467.5,3439.2,3175.1,3584.0,3322.0,3330.2,3079.6,3523.8,3620.5,3231.4
   Ross,6765.3,6457.9,6746.5,6386.8,6719.4,5681.9,6399.3,6849.7,7088.0,6579.5
   SaukRiver_nrSauk,13136.1,13713.3,11995.8,14280.0,14348.5,13019.2,12177.3,13506.3,13885.0,12223.6
   ThunderCreek,1639.3,1632.2,1579.3,1579.8,1615.7,1474.7,1585.3,1669.7,1665.7,1510.4
   Whitechuck,3292.6,3406.3,3160.9,3564.5,3597.9,3384.7,3361.0,3375.4,3438.5,3096.2

tables.outputs_Feb_1960_2099lowflow.flood/table-flood_outputs_Feb_1960_2099lowflow.flood.1980-2010_rcp45_p5-y100.csv

::

   ,CCSM4,CNRM-CM5,CSIRO-Mk-3-6-0,CanESM2,HadGEM2-CC365,HadGEM2-ES365,IPSL-CM5A-MR,MIROC5,NorESM1-M,bcc-csm1-1-m
   Diablo,72246.8,76195.6,69652.1,70466.4,70069.9,78851.9,70254.9,78236.3,73607.5,69876.9
   Gorge,78470.3,82884.5,75620.4,76344.4,76268.2,85183.8,76536.9,85188.0,79916.4,76017.5
   Newhalem2Marblemount,33418.2,32269.4,31549.7,30634.7,31106.9,31216.4,31849.4,33651.1,31019.8,31179.9
   Ross,62934.2,67067.8,61011.1,62553.5,61814.1,68279.7,61426.0,68070.4,64555.6,61247.5
   SaukRiver_nrSauk,82503.2,73691.8,75004.1,69640.4,69263.6,72752.2,74338.2,77438.2,72573.0,73730.5
   ThunderCreek,9039.4,9201.5,8609.8,8685.9,8548.4,8942.7,8536.0,9117.5,8701.3,8735.0
   Whitechuck,22855.1,21165.7,20464.7,19826.9,19741.9,20062.1,19866.0,21708.6,20788.1,20507.7


   

TODO
====

* re-direct to lib/*.c
* connect to scripts/*.py

* describe flood file formats (instead of adding headers?)

  * peak_flow_date
  * quantiles
  * strflw_flood_stats -- which statistics?
  
* describe lowflow file formats (instead of adding headers?)
  
  * 7q10_cal_date
  * 7q10_flow_date
  * quantiles
  * strflw_7q10_stats
  
* describe annual extreme selection by offset water year 
* describe summary and tabulation by (flood, lowflow) and respective statistics

* doc/git/test version for flood stat tools

* doc/git/test timing tools

* improve filename/directory conventions/structures

Streamflow to Extreme Stat Pipeline
===================================

Make a list of pipeline for one station/gcm/rcp (Diablo, bcc-csm1-1-m, rcp45)

* expose pipelines for (bc, raw=noBC) streamflow data to stat files

   :~/data/streamflows$ find outputs_Feb_1960_2099*/ -name "Diablo*bcc-csm1-1-m*rcp45*" > ~/Dropbox/tools/projects/skagit_streamstats/example_pipeline.bc.txt
   :~/data/streamflows$ find outputs_Feb_1960_2099noBC_lowflow*/ -name "DIABLO*bcc-csm1-1-m*rcp45*" > ~/Dropbox/tools/projects/skagit_streamstats/example_pipeline.noBC.txt

Isolate Runs for (noBC, bc, skaglo)
===================================

* run.id

  * setup*cfg
  * master*.bsh
  * run*.bsh
  * summ_stats.bsh
  * lib/*.c
  * scripts/*.py

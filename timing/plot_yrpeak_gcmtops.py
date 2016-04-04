#!/usr/bin/env python

import glob
import os.path
import sys

import pandas as pd
#import xray
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates
# matplotlib.style.use('ggplot')
import seaborn as sns
# from cdo import *
# import utils
# get_ipython().magic(u'matplotlib inline')

import plot_yrpeak_support as hytime

# sys.path.append('/home/matt/data/streamflows')

# base directory
bdir = '/mnt/data/WDRG/skagit2015/streamflows'
odir = 'figs.yrpeak'

# map bias corrected to raw
#    outputG_skagitHYDRO_lowflow.nobc_lff.rcp.flood.1980-2010/
#    outputs_11Nov_1960_2099.bclff.rcp.flood.1980-2010/
dbsrc = {'nobc':('outputG_skagitHYDRO_lowflow.nobc_lff.rcp.flood', 'm3s'),
      'bc':('outputs_11Nov_1960_2099.bclff.rcp.flood', 'cfs')}

# fileids = ['DIABLO bcc-csm1-1-m rcp45']
# SaukRiver nrSauk bcc-csm1-1-m.rcp45

statid = 'out_peak_flow_date out_quantiles out_strflw_flood_stats'.split(' ')

treatments = ['bc']
periods = '1980-2010 2010-2040 2035-2065 2070-2098'.split()
lcolors = ['k', 'b', 'c', 'r']

gcms='CCSM4,CNRM-CM5,CanESM2,HadGEM2-CC365,HadGEM2-ES365,IPSL-CM5A-MR,MIROC5,NorESM1-M,bcc-csm1-1-m'.split(',')
# for gcm in gcms[:1]:
scen='rcp45'
scen='rcp85'
r0=1
rF=6
r0=1
rF=28
r0=23
rF=28

# r0=1
# rF=9
r0=10
rF=19
# r0=20
# rF=28

inds=range(r0,rF)

hemicount=2.*len(inds)*2 #20
rlim = 2000.

for gcm in gcms:
    fileids = ['DIABLO %s %s'%(gcm,scen)]
    plt.clf()
    fig = plt.figure(2, figsize=(8,8))
    ax = fig.add_subplot(111, polar=True)
    # ax = fig.add_subplot(111, projection='polar')
#     treatments = ['nobc', 'bc']
#     periods = ['1980-2010', '1980-2010']
#     lcolors = ['k']
     
    for ifp in fileids:
        print gcm, statid
        dd = hytime.get_periods(ifp, bdir, dbsrc[treatments[0]][0], periods, statid, treatments[0])

    for nper, period in enumerate(periods):
        print periods[nper]
         
        hytime.add_group(dd[nper], inds, ax, *[lcolors[nper]])
        for seas in ['fall','winter','spring','summer']:
#         for seas in ['fall','winter']:            
#         for seas in ['summer','spring']:
            sinds = dd[nper].iloc[inds][dd[nper].iloc[inds]['season']==seas]
    #         sinds = dd[nper].ix[inds][dd[nper].ix[inds,'season']=='fall']
            print sinds
    #         print dd[nper].ix[inds][sinds]
    # #         print dd[nper].loc[inds]
     
            x,y = hytime.polar2xy(sinds['yrad'], sinds['Q'])
            X,Y = hytime.meanvector(x,y)
            itheta,irad= hytime.xy2polar(X,Y)
            print itheta*180./np.pi, irad
    #         ax.plot([itheta,itheta], [0.,irad], color=lcolors[nper], linewidth=4)        
            width = np.pi/hemicount*len(sinds)
            bars = ax.bar(itheta-width/2., irad, width=width, bottom=0.0)
            for bar in bars:
                bar.set_facecolor('None')
                bar.set_edgecolor(lcolors[nper])
                bar.set_linewidth(2)
                #bar.set_alpha(0.2)        

    hytime.format_polar(ax)
#     rmax = ax.set_rmax(rlim)
    hytime.add_season_sectors(ax,rlim)    
#     plt.title(periods[0])    
    #     rmax2 = ax.get_rmax()
     
    plt.suptitle(fileids[0])
    plt.savefig(os.path.join(odir,'tdelta_r-%s-%s_%s.svg'%(str(r0).zfill(2), str(rF).zfill(2),'-'.join(fileids))))

# 
#     for nper, period in enumerate(periods):
#         inds=range(1,6)
#         hytime.add_group(dd[nper], inds, ax, *[lcolors[nper]])





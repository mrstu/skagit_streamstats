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

# map historic to future
trang = '1980-2010 2010-2040 2035-2065 2070-2098'.split()

fileids = ['DIABLO bcc-csm1-1-m rcp45']
# SaukRiver nrSauk bcc-csm1-1-m.rcp45
statid = 'out_peak_flow_date out_quantiles out_strflw_flood_stats'.split(' ')

treatments = ['nobc', 'bc']
periods = ['1980-2010', '1980-2010']

treatments = ['bc', 'bc', 'bc']
periods = ['1980-2010', '2010-2040',  '2035-2065']
lcolors = ['k', 'r']

# plt.clf()
# fig = plt.figure(2, figsize=(8,8))
# ax = fig.add_subplot(111, polar=True)
# # ax = fig.add_subplot(111, projection='polar')
# for ifp in fileids:
#     print statid
#     dd = get_file_pair(ifp, periods, statid)
#     add_traces(dd, ax, *lcolors)
# 
# format_polar(ax)
# plt.savefig('tdelta_rad.png')

# treatments = ['bc', 'bc', 'bc']
# periods = ['1980-2010', '2010-2040',  '2035-2065']
# lcolors = ['k', 'r']

# Inter-period need to sort by rank?
# plt.clf()
# fig = plt.figure(2, figsize=(8,8))
# ax = fig.add_subplot(121, polar=True)
# # ax = fig.add_subplot(111, projection='polar')
# treatments = ['bc', 'bc']
# periods = ['1980-2010', '2010-2040']
# lcolors = ['k']
# 
# for ifp in fileids:
#     print statid
#     dd = get_file_pair(ifp, periods, statid)
#     add_traces(dd, ax, *lcolors)
# format_polar(ax)
# 
# ax = fig.add_subplot(122, polar=True)
# # ax = fig.add_subplot(111, projection='polar')
# treatments = ['bc', 'bc']
# periods = ['2010-2040', '2035-2065']
# lcolors = ['r']
# 
# for ifp in fileids:
#     print statid
#     dd = get_file_pair(ifp, periods, statid)
#     add_traces(dd, ax, *lcolors)
# 
# format_polar(ax)
# 
# 
# plt.savefig('tdelta_rad2.png')

gcms='CCSM4,CNRM-CM5,CanESM2,HadGEM2-CC365,HadGEM2-ES365,IPSL-CM5A-MR,MIROC5,NorESM1-M,bcc-csm1-1-m'.split(',')
for gcm in gcms:
    fileids = ['DIABLO %s rcp45'%gcm]
    plt.clf()
    fig = plt.figure(2, figsize=(8,8))
    ax = fig.add_subplot(221, polar=True)
    # ax = fig.add_subplot(111, projection='polar')
    treatments = ['nobc', 'bc']
    periods = ['1980-2010', '1980-2010']
    lcolors = ['k']
    
     
    for ifp in fileids:
        print statid
        dd = hytime.get_file_pair(ifp, bdir, dbsrc, periods, statid, treatments)
        hytime.add_traces(dd, ax, *lcolors)
    hytime.format_polar(ax)
    rlim=2000.
    rmax = ax.set_rmax(rlim)
    plt.title(periods[0])
    
    ax = fig.add_subplot(222, polar=True)
    # ax = fig.add_subplot(111, projection='polar')
    treatments = ['nobc', 'bc']
    periods = ['2010-2040', '2010-2040']
    # periods = ['2070-2098', '2070-2098']
    lcolors = ['b']
     
    for ifp in fileids:
        print statid
        dd = hytime.get_file_pair(ifp, bdir, dbsrc, periods, statid, treatments)
        hytime.add_traces(dd, ax, *lcolors)
    hytime.format_polar(ax)
    rmax = ax.set_rmax(rlim)
    plt.title(periods[0])
    
     
    ax = fig.add_subplot(223, polar=True)
    # ax = fig.add_subplot(111, projection='polar')
    treatments = ['nobc', 'bc']
    periods = ['2035-2065', '2035-2065']
    # periods = ['2070-2098', '2070-2098']
    lcolors = ['c']
     
    for ifp in fileids:
        print statid
        dd = hytime.get_file_pair(ifp, bdir, dbsrc, periods, statid, treatments)
        hytime.add_traces(dd, ax, *lcolors)
    hytime.format_polar(ax)
    rmax = ax.set_rmax(rlim)
    plt.title(periods[0])
    
    
    
    ax = fig.add_subplot(224, polar=True)
    # ax = fig.add_subplot(111, projection='polar')
    treatments = ['nobc', 'bc']
    # periods = ['2035-2065', '2035-2065']
    periods = ['2070-2098', '2070-2098']
    lcolors = ['r']
     
    for ifp in fileids:
        print statid
        dd = hytime.get_file_pair(ifp, bdir, dbsrc, periods, statid, treatments)
        hytime.add_traces(dd, ax, *lcolors)
    hytime.format_polar(ax)
    rmax2 = ax.get_rmax()
    rmax = ax.set_rmax(rlim)
    plt.title(periods[0])
    
    plt.suptitle(fileids[0])
    plt.savefig(os.path.join(odir,'tdelta_rad5_%s.svg'%gcm)) 
    # plt.savefig('tdelta_rad4.svg')
    # plt.savefig('tdelta_rad3.png')

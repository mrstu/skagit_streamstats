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

# sys.path.append('/home/matt/data/streamflows')


def format_polar(ax):
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi)
    # ax.set_rgrids(**{'visible':True})
    # ax.grid(True)
    ax.yaxis.grid(color='k', linestyle='--', linewidth=1)
    ax.xaxis.grid(color='k', linestyle='--', linewidth=1)
    angles = np.arange(0,360,30)#*np.pi/180.
    ax.set_thetagrids(angles, labels='O,N,D,J,F,M,A,M,J,J,A,S'.split(',')) #, frac=None, fmt=None, **kwargs)
    # ax.yaxis.grid(linewidth=3)
    
    # .set_rgrids(radii, labels=None, angle=None, fmt=None, **kwargs)
    # .set_thetagrids(angles, labels=None, frac=None, fmt=None, **kwargs)
    # mlabs = np.arange(0,360,30)*np.pi/180.
    
    # for nlab, mlab in enumerate(mlabs):
    #     print str(nlab)
    #     ax.text(3000*np.cos(mlab), 3000.*np.sin(mlab), str(nlab))
    #     ax.annotate('a polar annotation',
    #                 xy=(thistheta, thisr),  # theta, radius
    #                 xytext=(0.05, 0.05),    # fraction, fraction
    #                 textcoords='figure fraction',
    #                 arrowprops=dict(facecolor='black', shrink=0.05),
    #                 horizontalalignment='left',
    #                 verticalalignment='bottom',
    #                 )    
    #     plt.text(3000*np.cos(mlab), 3000.*np.sin(mlab), str(nlab))


def leapscale_rad():
    if (df['year']%4 == 0 and df['year']%100 !=0 and df['month']<10) or \
        (df['year']%4 == 3 and df['year']%100 !=99 and df['month']>=10):
        df['yrad'] = 2. * np.pi * df['yd'] / 366.        
    else:
        df['yrad'] = 2. * np.pi * df['yd'] / 365.
#         dd[trt] = df        
#         if trt == 'bc':
#             dd[trt]['Q'] = dd[trt]['Q']*0.0283 

def add_traces(dd, ax, *args):
    dkeys = dd.keys()
    dkeys.sort()
    print dkeys
    for nk, dkey in enumerate(dkeys[1:]):
        for iv in dd[dkeys[0]].index:
        #     print iv
            yd,Q = dd[dkeys[0]].ix[iv,['yd','Q']]
            ydbc,Qbc = dd[dkey].ix[iv,['yd','Q']]   
            yrad = 2. * np.pi * yd / 366.
            yradbc = 2. * np.pi * ydbc / 366.
        
            # get angle between rays
            a = yrad; b = yradbc    
            av = np.array([np.cos(a),np.sin(a)])
            bv = np.array([np.cos(b),np.sin(b)])
            drad = np.arccos(np.cos(a)*np.cos(b)+np.sin(a)*np.sin(b)) #*180/np.pi
            crp = np.cross(av,bv)
            # could use cross product
            if crp < 0: # clockwise
                yradF=yrad-drad
        #         yrada = [yradbc, yrad]
        #         yQa = [Qbc, Q]
            else: # ccw
                yradF=yrad+drad
            yrada = np.linspace(yrad, yradF,20)
            yQa = np.linspace(Q, Qbc, 20)
        #     ax.plot(yrada,yQa,'b-',**{'alpha':0.5})
        #     ax.plot(yradF,Qbc,'o',**{'alpha':0.5, 'mec':'b', 'mfc':'None', 'ms':10, 'mew':2})
            if args:
                ax.plot(yrada,yQa,'-',**{'alpha':0.4,'color':args[nk],'lw':1.})
#                 lc = plt.getp(line, 'color')
                ax.plot(yrad,Q,'.',**{'mfc':args[nk], 'mec':'None', 'ms':3, 'mew':1})
#                 ax.plot(yradF,Qbc,'.',**{'mfc':args[nk], 'mec':'None', 'ms':5, 'mew':1})                
                ax.plot(yradF,Qbc,'s',**{'alpha':0.5, 'mfc':'None', 'mec':args[nk], 'ms':5, 'mew':.5})                                
#                 ax.plot(yradF,Qbc,'o',**{'alpha':0.4, 'mec':args[nk], 'mfc':'None', 'ms':10, 'mew':1})
            else:
                line,=ax.plot(yrada,yQa,'-',**{'alpha':0.8})
                lc = plt.getp(line, 'color')
                ax.plot(yradF,Qbc,'o',**{'alpha':0.4, 'mec':lc, 'mfc':'None', 'ms':10, 'mew':2})
            
    
#     plt.polar(yrada,yQa,'b-',**{'alpha':0.5})
#     plt.polar(yradF,Qbc,'bo',**{'alpha':0.5, 'mec':'b', 'mfc':None})

def get_file_pair(ifp, periods, statid):
#     for ifp in fileids:
    
    dd = {}
    idparts = ifp.split() 
    for ntrt, (trt, period) in enumerate(zip(treatments,periods)):
        fp = bdir+'/'+dbsrc[trt][0]+'.%s/%s*.%s'%(period, '*'.join(idparts), statid[0])
        print fp
        ifp = glob.glob(fp)
        print ifp
        df = pd.read_csv(ifp[0],
                   header=None, names=['Q','yd','year','month','day'],
                   index_col=[0], delim_whitespace=True)
        df['yrad'] = 2. * np.pi * df['yd'] / 366.        
        dd[ntrt] = df        
        if trt == 'bc':
            dd[ntrt]['Q'] = dd[ntrt]['Q']*0.0283 
    return dd            


# base directory
bdir = '/mnt/data/WDRG/skagit2015/streamflows'

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
        dd = get_file_pair(ifp, periods, statid)
        add_traces(dd, ax, *lcolors)
    format_polar(ax)
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
        dd = get_file_pair(ifp, periods, statid)
        add_traces(dd, ax, *lcolors)
    format_polar(ax)
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
        dd = get_file_pair(ifp, periods, statid)
        add_traces(dd, ax, *lcolors)
    format_polar(ax)
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
        dd = get_file_pair(ifp, periods, statid)
        add_traces(dd, ax, *lcolors)
     
    format_polar(ax)
    rmax2 = ax.get_rmax()
    rmax = ax.set_rmax(rlim)
    plt.title(periods[0])
    
    plt.suptitle(fileids[0])
    plt.savefig('tdelta_rad5_%s.svg'%gcm) 
    # plt.savefig('tdelta_rad4.svg')
    # plt.savefig('tdelta_rad3.png')

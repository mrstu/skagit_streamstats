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
statid = ['out_peak_flow_date out_quantiles out_strflw_flood_stats'.split()]

treatments = ['nobc', 'bc']
itrang = trang[0]

for ifp in fileids:
    
    dd = {'nobc':[], 'bc':[]}
    idparts = ifp.split() 
    for ntrt, trt in enumerate(treatments):
        print trt
        fp = bdir+'/'+dbsrc[trt][0]+'.%s/%s.%s*'%(itrang, '*'.join(idparts), statid[0])
        print fp
        ifp = glob.glob(fp)
        
        df = pd.read_csv(ifp[0],
                   header=None, names=['Q','yd','year','month','day'],
                   index_col=[0], delim_whitespace=True)

#         if (df['year']%4 == 0 and df['year']%100 !=0 and df['month']<10) or \
#             (df['year']%4 == 3 and df['year']%100 !=99 and df['month']>=10):
        df['yrad'] = 2. * np.pi * df['yd'] / 366.        
#         else:
#             df['yrad'] = 2. * np.pi * df['yd'] / 365.        
        
        if trt == 'bc':
            dd[trt] = df*0.0283 
        else:
            dd[trt] = df
            
# plt.figure(1)
# # plt.plot(dd['nobc']['yd'],dd['nobc']['Q'],'ko')
# dt=dd['nobc']['yd']-dd['bc']['yd']
# dQ=dd['nobc']['Q']-dd['bc']['Q']
# # plt.plot(dd['nobc']['yd'],dd['bc']['Q'],'b.')
# plt.plot(dd['nobc']['yd'],dd['nobc']['Q'],'ko')
# plt.plot([dd['nobc']['yd'],dd['bc']['yd']],[dd['nobc']['Q'],dd['bc']['Q']],'b-')
# plt.savefig('tdelta.png')

# plt.figure(2)
# # plt.plot(dd['nobc']['yd'],dd['bc']['Q'],'b.')
# plt.polar(dd['nobc']['yrad'],dd['nobc']['Q'],'ko',**{'alpha':0.5})
# plt.polar([dd['nobc']['yrad'],dd['bc']['yrad']],[dd['nobc']['Q'],dd['bc']['Q']],'b-',**{'alpha':0.5})
# plt.savefig('tdelta_rad.png')

plt.figure(2)
for iv in dd['nobc'].index:
    print iv
# # plt.plot(dd['nobc']['yd'],dd['bc']['Q'],'b.')
# plt.polar(dd['nobc']['yrad'],dd['nobc']['Q'],'ko',**{'alpha':0.5})
# plt.polar([dd['nobc']['yrad'],dd['bc']['yrad']],[dd['nobc']['Q'],dd['bc']['Q']],'b-',**{'alpha':0.5})

plt.savefig('tdelta_rad.png')        
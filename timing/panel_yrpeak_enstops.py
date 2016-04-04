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
from astropy.modeling.utils import comb

# sys.path.append('/home/matt/data/streamflows')

# base directory

mpl.rcParams['mathtext.default'] = 'regular'

def main(*args):

    bdir = '/mnt/data/WDRG/skagit2015/streamflows'
#     odir = 'figs.yrpeak'
#     odir = 'figs.yrpeak/stations'
    odir = 'figs.yrpeak/tdeltaEns'
    
    # map bias corrected to raw
    #    outputG_skagitHYDRO_lowflow.nobc_lff.rcp.flood.1980-2010/
    #    outputs_11Nov_1960_2099.bclff.rcp.flood.1980-2010/
    dbsrc = {'nobc':('outputG_skagitHYDRO_lowflow.nobc_lff.rcp.flood', 'm3s', ''),
          'bc':('outputs_11Nov_1960_2099.bclff.rcp.flood', 'cfs', 'outputs_11Nov_1960_2099.flood.bclff')}
    
    # fileids = ['DIABLO bcc-csm1-1-m rcp45']
    # SaukRiver nrSauk bcc-csm1-1-m.rcp45
    # stnname= 'DIABLO'
    
    stations = ['DIABLO']
    stations = ['WhiteChuck']
    stations = 'BACON BigCreek CascadeRiver DIABLO FinneyCreek GORGE Illabot JackmanCreek JordanCreek NorthForkSauk ROSS RedCabin SaukRiver_Darrington SaukRiver_abClearCreek_nrDarrington SaukRiver_nrSauk Sauk_abWhitechuck_nrDarrington SouthForkSauk THUNDERCreek WhiteChuck'.split()
#     stations = 'GORGE DIABLO ROSS RedCabin SaukRiver_nrSauk THUNDERCreek WhiteChuck'.split()    
    stations = 'DIABLO GORGE ROSS SaukRiver_nrSauk THUNDERCreek WhiteChuck'.split()    
#     stations = ['DIABLO']
    # stations = ['GORGE']
    # stations = ['WhiteChuck']
    
    statid = 'out_peak_flow_date out_quantiles out_strflw_flood_stats'.split(' ')
    
    # treatment = 'bc'
    # treatment = 'nobc'    
    treatment = args[1]
    periods = '1980-2010 2010-2040 2035-2065 2070-2098'.split()
    lcolors = ['k', 'b', 'c', 'r']
    fcolors = ['black', 'blue', 'cyan', 'red']
    
#     gcms='CCSM4,CNRM-CM5,CanESM2,HadGEM2-CC365,HadGEM2-ES365,IPSL-CM5A-MR,MIROC5,NorESM1-M,bcc-csm1-1-m'.split(',')
    if len(args) == 7:
        gcms = [args[6]]
        hemicount=2.*4*2.
    else:
        gcms = []
        for arg in args[6:]:
            gcms.append(arg)
        hemicount=2.*4*len(gcms)*2.    
            
#     gcms=['CCSM4']
#     hemicount=2.*4*2.
    
    # for gcm in gcms[:1]:
    #scen='rcp45'
    #scen='rcp85'
    scen = args[2]
    
    # rlim = 2000.
    donorm=False    
    if args[3] == 'scale':
        donorm=True
        rlimnorm=float(args[4]) #2.5
    elif args[3] == 'rlim':        
        rlim = float(args[4])
    else:
        rlim = -1
        
#     if rlimnorm == 1.0:
#         donorm=False
#     else:
#         donorm = True
#     # donorm = False
    
    # r0=1
    # rF=6
    # r0=1
    # rF=28
    # r0=23
    # rF=28
    # # r0=1
    # # rF=9
    # r0=10
    # rF=19
    # # r0=20
    # # rF=28
    # r0=1
    # rF=10
    # 
    # # This is a slice, but adding to be based on return stat (Q_10year).
    # inds=range(r0,rF)
    # hemicount=2.*len(inds)*len(gcms)*2. #20
    
    dorecint = 1
    
    recint = 'p2-y10'
    table_name = 'table-flood_%s.%s_%s_%s.csv'%(dbsrc[treatment][0], periods[0], scen, recint)
    
    if dbsrc[treatment][2]:
        table_loc = '/mnt/data/WDRG/skagit2015/streamflows/tables.%s/%s'%(dbsrc[treatment][2], table_name)
    else:
        table_loc = '/mnt/data/WDRG/skagit2015/streamflows/tables.%s/%s'%(dbsrc[treatment][0], table_name)
    
    # get_table(istn, periods[0])
    dft = pd.read_csv(table_loc, index_col=[0], delimiter=",")
    
    if treatment == 'bc':
        dft = dft * 0.0283 

    fig = plt.figure(1, figsize=(6,10))
#     fig = plt.figure(1)
    
    for nstn, istn in enumerate(stations):
        stnname = istn

        ax = fig.add_subplot('32%d'%(nstn+1), polar=True)        
                       
        comb = {}
        for nper, period in enumerate(periods):
            for seas in ['fall','winter','spring','summer']:
                comb['%sX_%d'%(seas,nper)] = []
                comb['%sY_%d'%(seas,nper)] = [] 
        print comb.keys()   
        
        try:
        
            # for gcm in gcms[:2]:
    #         for gcm in gcms[:1]:
            for gcm in gcms:
                fileids = ['%s %s %s'%(stnname, gcm,scen)]
                # ax = fig.add_subplot(111, projection='polar')
            #     treatments = ['nobc', 'bc']
            #     periods = ['1980-2010', '1980-2010']
            #     lcolors = ['k']
                 
                for ifp in fileids:
                    print gcm, statid
                    dd = hytime.get_periods(ifp, bdir, dbsrc[treatment][0], periods, statid, treatment)
            
                for nper, period in enumerate(periods):
                    print periods[nper]
                    
                    if dorecint:
                        print istn,gcm
                        print dft.loc[istn,gcm]
    #                     inds = dd[nper]['Q'][dd[nper]['Q']>=dft.loc[istn,gcm]] #.iloc[inds]['season']==seas]
    #                     inds = dd[nper]['Q'].where(dd[nper]['Q']>=dft.loc[istn,gcm]) #.iloc[inds]['season']==seas]                    
    #                     inds = dd[nper].where(dd[nper]['Q']>=dft.loc[istn,gcm]) #.iloc[inds]['season']==seas]
    #                     inds = dd[nper].where(dd[nper]['Q']>=dft.loc[istn,gcm]) #.iloc[inds]['season']==seas]
    #                     print inds
    #                     newinds = inds.notnull()
    #                     print newinds
                        inds = np.where(dd[nper]['Q'].values >= dft.loc[istn,gcm]) #.iloc[inds]['season']==seas]
                        print inds
    #                     newinds = inds.notnull()
    #                     print newinds
    
                        
            #         hytime.add_group(dd[nper], inds, ax, *[lcolors[nper]])
                    for seas in ['fall','winter','spring','summer']:
            #         for seas in ['fall','winter']:            
            #         for seas in ['summer','spring']:
                        sinds = dd[nper].iloc[inds][dd[nper].iloc[inds]['season']==seas]
                        print sinds
                        
                        if donorm:
                            x,y = hytime.polar2xy(sinds['yrad'], sinds['Q']/dft.loc[istn,gcm])
                            rlim = rlimnorm
                        else:
                            x,y = hytime.polar2xy(sinds['yrad'], sinds['Q']) # don't normalize
                            
                        print '%sX_%d'%(seas,nper)
            #             print type(x)
            #             print x
            
                        if len(x.tolist()) == 0:
                            pass
                        else:
                            print len(x.tolist())
                            if len(comb['%sX_%d'%(seas,nper)]) == 0:
                                comb['%sX_%d'%(seas,nper)] = x.tolist()
                                comb['%sY_%d'%(seas,nper)] = y.tolist()
                            else:
                                comb['%sX_%d'%(seas,nper)].extend(x.tolist())
                                comb['%sY_%d'%(seas,nper)].extend(y.tolist())
            #         print '%sX_%d'%('fall',nper), comb['%sX_%d'%('fall',nper)]
            # print comb['fallX_0']

            for nper, period in enumerate(periods):
                for seas in ['fall','winter','spring','summer']:            
                    xC = comb['%sX_%d'%(seas,nper)]
                    yC = comb['%sY_%d'%(seas,nper)]
            #         print 'meanvector'
                    print xC,yC
                    if len(xC) == 0:
                        pass
                    else:
                        X,Y = hytime.meanvector(xC,yC)
                #         print X,Y
                        itheta,irad= hytime.xy2polar(X,Y)
                        print itheta*180./np.pi, irad
                #         ax.plot([itheta,itheta], [0.,irad], color=lcolors[nper], linewidth=4)        
#                         print 'xC', xC, hemicount
#                         print gcms
                        width = np.pi/hemicount*len(xC)
                        bars = ax.bar(itheta-width/2., irad, width=width, bottom=0.0, alpha=0.75)
                        for bar in bars:
                            bar.set_facecolor('None')
                            bar.set_edgecolor(lcolors[nper])
                            bar.set_linewidth(2)
                            #bar.set_alpha(0.2)        
                            
             
            hytime.format_polar(ax)
            if donorm:
                rmax = ax.set_rmax(rlim)
            elif rlim > 0:            
#                 rlim = ax.get_rmax()
                rmax = ax.set_rmax(rlim)
            else:
                rlim = ax.get_rmax()
            ax.set_rlabel_position(135)                    
            hytime.add_season_sectors(ax,rlim)    
            rmax = ax.set_rmax(rlim)            
            #     plt.title(periods[0])    
            #     rmax2 = ax.get_rmax()
              
#             plt.title('%s, '%stnname+r'$Q_{10,hist} = %5.2f$'%dft.loc[istn].mean())
            plt.title('%s\n'%(stnname)+r'$Q_{10,hist} = %5.2f$ '%dft.loc[istn].mean()+r'$[m^{3}s^{-1}]$')            
#             plt.ylabel(r'$Q_{10,hist} = %5.2f$'%dft.loc[istn].mean())
#             ax.yaxis.labelpad = 20            
#             ax.set_rlabel_position(-45)


        except:
            raise
    pats = []
    for lc in lcolors:
        pats. append(mpl.patches.Rectangle((0, 0), 1, 1, fc=lc))
#     legend([p], lcolors)
    plt.figlegend(pats, periods, 'lower center', ncol=2) #ax.plot(itheta, irad, alpha=0.75, linewidth=1, color=colormap(cparts[igcm]))        

    plt.suptitle('Normalized Annual Peak Flow by Epoch ['+r'$Q_{peak}/Q_{10,hist}$'+'] for (%s, %s)'%(scen,treatment))            
    if dorecint:
        if args[5] == 'ensemble':
            oname = os.path.join(odir, 'tdeltaEns_r-%s_%s_%s_%s_%03.1F'%(recint, scen, args[5], treatment, rlim))
        else:
            oname = os.path.join(odir, 'tdeltaEns_r-%s_%s_%s_%s_%03.1F'%(recint, scen, args[6], treatment, rlim))
    else:            
        oname = os.path.join(odir, 'tdeltaEns_r-%s-%s_%s_%s'%(str(r0).zfill(2), str(rF).zfill(2), scen, treatment))
    print oname
    plt.savefig(oname+'.svg')
    plt.savefig(oname+'.png')            

if __name__=='__main__':
#     print sys.argv
    main(*sys.argv)        

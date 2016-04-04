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


def add_season_sectors(ax, rmax):
    '''Add seasonal slices'''
    theta = np.arange(0,4) * np.pi/2.
    radii = np.ones(4)*rmax
    width = np.pi / 2
    print theta
    print radii

    bars = ax.bar(theta, radii, width=width, bottom=0.0)
    bcolors=['b','k','g','r']
    # Use custom colors and opacity
    for bc, bar in zip(bcolors,bars):
        bar.set_facecolor(bc)
        bar.set_alpha(0.1)


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

def get_file_pair(ifp, bdir, dbsrc, periods, statid, treatments):
#     for ifp in fileids:
    
    dd = {}
    idparts = ifp.split() 
    for ntrt, (trt, period) in enumerate(zip(treatments,periods)):
        fp = bdir+'/'+dbsrc[trt][0]+'.%s/%s*.%s'%(period, '*'.join(idparts), statid[0])
        ifp = glob.glob(fp)

        df = pd.read_csv(ifp[0],
                   header=None, names=['Q','yd','year','month','day'],
                   index_col=[0], delim_whitespace=True)
        
        df['yrad'] = 2. * np.pi * df['yd'] / 366.        
        dd[ntrt] = df   
        if trt == 'bc':
            dd[ntrt]['Q'] = dd[ntrt]['Q']*0.0283 
    return dd            

def get_periods(ifp, bdir, indirprefix, periods, statid, trt, dosort=True):
    dd = {}
    idparts = ifp.split() 
    for nper, period in enumerate(periods):
        fp = bdir+'/'+indirprefix+'.%s/%s*.%s'%(period, '*'.join(idparts), statid[0])
        ifp = glob.glob(fp)
        print fp
        print ifp
        df = pd.read_csv(ifp[0],
                   header=None, names=['Q','yd','year','month','day'],
                   index_col=[0], delim_whitespace=True)
        if dosort:
            df.sort_values('Q', ascending=False, inplace=True)
        
        df['yrad'] = 2. * np.pi * df['yd'] / 366.
        df['season'] = ['none']*len(df.index)        
        df = frame_add_season(df)
        dd[nper] = df
        if trt == 'bc':
            dd[nper]['Q'] = dd[nper]['Q']*0.0283 
            
    return dd            

def add_group(df, inds, ax, *args):
#     print df.loc[inds,['yrad','Q']]    
#     yrad,Q = df.loc[inds,['yrad','Q']]
#     print df.iloc[inds].loc[:,['yd','Q']]
#     ax.plot(df.iloc[inds].loc[:,['yrad']],df.iloc[inds].loc[:,['Q']],'.',**{'mfc':args[0], 'mec':'None', 'ms':3, 'mew':1})
    print 'group', df.iloc[inds]
    ax.plot(df.iloc[inds].loc[:,['yrad']],df.iloc[inds].loc[:,['Q']],'s',**{'alpha':0.5, 'mfc':'None', 'mec':args[0], 'ms':5, 'mew':1})                                

def frame_add_season(df):
    mongrps=[('fall',[10,11,12]),('winter',[1,2,3]),('spring',[4,5,6]),('summer',[7,8,9])]
#     df['season'] = ['none']*len(df.index)
    for mongrp in mongrps:
        df['season'][df.month.isin(mongrp[1])] = mongrp[0]
    return df

def polar2xy(theta,radii):
    x=radii*np.cos(theta)
    y=radii*np.sin(theta)
    return x,y

def meanvector(x,y):    
    X=np.mean(x)
    Y=np.mean(y)
    return X,Y

def xy2polar(x,y):
    radii=np.sqrt(x**2+y**2)
#     theta = np.arccos(np.dot([1,0],[x/np.abs(x),y/np.abs(y)]))
#     theta = np.arccos(np.dot([x,y],[1,0])/(np.abs(x)*np.abs(y)))
    if y > 0.:
        if x > 0.:
            theta=np.arccos(x/radii)
        else:
#             theta=np.pi-np.arccos(x/radii)
            theta=np.arccos(x/radii)
    else:
        if x > 0.:
            theta=-np.arccos(x/radii)
        else:
            theta=2*np.pi-np.arccos(x/radii)
#         theta=np.arcsin(y/radii)
# #     theta=np.arctan(y/x)
    return theta,radii

def XYs2polars(X,Y):
#     Xl, Yl = X.to_list(), Y.to_list()
    Atheta, Aradii = [],[]
    for x,y in zip(X,Y):
        theta,radii = xy2polar(x,y)
        Atheta.append(theta)
        Aradii.append(radii)
    return Atheta, Aradii


# def get_season(df):
#     mongrps=[('fall',[10,11,12]),('winter',[1,2,3]),('spring',[4,5,6]),('summer',[7,8,9])]
#     dseas = {}
#     for mongrp in mongrps:
#         dseas[mongrp[0]] = df[df.month.isin(mongrp[1])]
#     return dseas


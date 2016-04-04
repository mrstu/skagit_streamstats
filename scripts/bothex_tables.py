
# coding: utf-8

# In[17]:

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

def records_from_startofname(dframe, name):
    irows=[]
    rownames=[]
    for n,ind in enumerate(dframe.index.values):
        if ind.startswith(name):
            irows.append(n)
            rownames.append(ind)
    return irows, rownames

def df2table(dframe,usites,ugcms,scen,pid):
    columns=ugcms
    index=usites
    dfn=pd.DataFrame(index=index, columns=columns)
    for gcm in ugcms:
        index0=[]
        for site in usites:
            index0.append(site+'__'+gcm+'__%s'%scen)
        selsite = dframe.ix[index0,pid]
        dfn[gcm]=selsite.values
    return dfn

def main(onameprefix, stattype, fsumtab, oloc):

    names=['dir', 'name', 'distnum', 'p1','p2','p3','p4','p5','p6','p7']
#     files=glob.glob('/home/matt/data/streamflows/sumtab_outputs_19Aug_1960_2099.4col.*.flood.*.txt')
    files=glob.glob(fsumtab)
    files.sort()
    print files

    try:
        os.makedirs(oloc)
    except OSError:
        pass


# def blah():    
    df = pd.read_csv(files[0],
                       header=None, names=names, 
                       index_col=[1], delim_whitespace=True)
#     df2 = pd.read_csv(files[1],
#                        header=None, names=names, 
#                        index_col=[1], delim_whitespace=True)
    
    catalog={}
    gcms={}
    pers={}
    for hind in df.index:
        parts = hind.split('__')
        catalog[parts[0]] = []
        gcms[parts[1]] = []
        pers[parts[2]] = []
    usites = catalog.keys()
    ugcms = gcms.keys()
    upers = pers.keys()    
    
    usites.sort()
    ugcms.sort()
    upers.sort()
#     '''Hack for skagit lowlands convention for historical period'''
#     ugcms.remove('vic')
#     upers.remove('hist')    
    
#     scens=[('historical',df), ('rcp45',df2), ('rcp85',df2)]
    if stattype == 'flood':
        labels='1 10 20 50 100 200 500 '.split() # HI YEARS
    elif stattype== 'low':
        labels='500 200 100 50 20 10 2'.split() # LOW YEARS
    # for scen in scens[:1]:
    #     for n in range(1,2):#*8):
    for scen in upers:
        for n in range(1,8):
            pid='p%d'%n
            
            otable='%s/table-%s_%s_%s_%s-y%s.csv'%(oloc, stattype, onameprefix, scen, pid, labels[n-1])
            print otable
    #         print '%s,%s,y%s'%(scen[0],pid,labels[n-1]), ' '.join(ugcms)
            dfn = df2table(df,usites,ugcms,scen,pid)
            dfn.to_csv(otable)
#     '''Hack for skagit lowlands convention for historical period'''
#     for scen in ['hist']:
#         for n in range(1,8):
#             pid='p%d'%n
#             
#             otable='%s/table-%s_%s_%s_%s-y%s.csv'%(oloc, stattype, onameprefix, scen, pid, labels[n-1])
#             print otable
#     #         print '%s,%s,y%s'%(scen[0],pid,labels[n-1]), ' '.join(ugcms)
#             dfn = df2table(df,usites,['vic'],scen,pid)
#             dfn.to_csv(otable)

    
if __name__ == '__main__':
    main(*sys.argv[1:5])
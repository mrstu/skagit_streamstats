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


# def main(onameprefix, stattype, fsumtab):
# def main(dirtables="/home/matt/data/streamflows/tables"):
def main(dirtables):
    timemap = [("hist", "1980-2010"),
                ("future1","2010-2040"),
                ("future2","2035-2065"),
                ("future3","2070-2098")]
#     timemap = [("hist", "hist"),
#                 ("future1","A1B")]    

    dirpctchg=dirtables+".pctchg"
    try:
        os.makedirs(dirpctchg)
    except OSError:
        pass
    
    names=['dir', 'name', 'distnum', 'p1','p2','p3','p4','p5','p6','p7']
#     files=glob.glob('/home/matt/data/streamflows/sumtab_outputs_19Aug_1960_2099.4col.*.flood.*.txt')
#     files=glob.glob(dirtables+"/*flood."+timemap[0][1]+"*_rcp45_p2-*.csv")
    files=glob.glob(dirtables+"/*"+timemap[0][1]+"*.csv")
    files.sort()
    print files

    for fn in files:
        df = pd.read_csv(fn)
        dfpct=pd.DataFrame(index=df.index,columns=df.columns)
        

        for itime in timemap[1:]:
            fnfut = fn.replace(timemap[0][1],itime[1])
            print fn, fnfut
    
            df2 = pd.read_csv(fnfut)
            iindex=df2.index
#             dfpct.reindex(index=iindex)            
            df2.reindex(index=[df2.index, 'max', 'mean', 'min'])
#             print df
#             print df2
            chgvals=(df2.ix[:,1:].values-df.ix[:,1:].values)/df.ix[:,1:].values * 100.
            chgshape=chgvals.shape
            '''Hack for skagit lowlands convention for historical period'''            
            if df.shape[1] == 2:
                dfpct=pd.DataFrame(index=iindex,columns=df2.columns)
            dfpct.iloc[:,0]=df.iloc[:,0]
#             print chgvals.shape, dfpct.shape
#             print dfpct     
#             print chgvals   
#             print df    
#             print 'dfshape1', df.shape[1]       
#             print iindex
#             print dfpct           
            dfpct.iloc[:,1:(chgshape[1]+1)] = chgvals
            print dfpct           
            chgmax=pd.Series(chgvals.max(axis=1), index=dfpct.index)
            chgmean=pd.Series(chgvals.mean(axis=1), index=dfpct.index)
            chgmin=pd.Series(chgvals.min(axis=1), index=dfpct.index)
            chgstd=pd.Series(chgvals.std(axis=1), index=dfpct.index)

            dfpct['mean'] = chgmean           
            dfpct['max'] = chgmax
            dfpct['min'] = chgmin  
            dfpct['std'] = chgstd
                      
#             print df.iloc[0,:]
#             print df2.iloc[0,:]
#             print dfpct.iloc[0,:]
            fnfutout=fnfut.replace(dirtables,dirpctchg)
            dfpct.to_csv(fnfutout,index=False, float_format='%.4f')
#             print dfpct.ix[:,[0,-4,-3,-2,-1]]
            
#     
#     catalog={}
#     gcms={}
#     pers={}
#     for hind in df.index:
#         parts = hind.split('__')
#         catalog[parts[0]] = []
#         gcms[parts[1]] = []
#         pers[parts[2]] = []
#     usites = catalog.keys()
#     ugcms = gcms.keys()
#     upers = pers.keys()    
#     
#     usites.sort()
#     ugcms.sort()
#     upers.sort()
#     
# #     scens=[('historical',df), ('rcp45',df2), ('rcp85',df2)]
#     if stattype == 'flood':
#         labels='1 10 20 50 100 200 500 '.split() # HI YEARS
#     elif stattype== 'low':
#         labels='500 200 100 50 20 10 2'.split() # LOW YEARS
#     # for scen in scens[:1]:
#     #     for n in range(1,2):#*8):

#     for scen in upers:
#         for n in range(1,8):
#             pid='p%d'%n
#             
#             otable='table-%s_%s_%s_%s-y%s.csv'%(stattype, onameprefix, scen, pid, labels[n-1])
#             print otable
#     #         print '%s,%s,y%s'%(scen[0],pid,labels[n-1]), ' '.join(ugcms)
#             dfn = df2table(df,usites,ugcms,scen,pid)
#             dfn.to_csv(otable)
    
if __name__ == '__main__':
#     main(*sys.argv[1:4])
    main(sys.argv[1])
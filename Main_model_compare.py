#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 13:11:24 2021
@author: jiching
"""
import math
import flac
import os,sys
import numpy as np
import pandas as pd
import gravity as fg
import matplotlib
#matplotlib.use('Agg')
from matplotlib import cm
import function_savedata as fs
import function_for_flac as f2
import matplotlib.pyplot as plt

#---------------------------------- DO WHAT -----------------------------------
trench_plot             = 0
dip_plot                = 0
plate_geometry          = 1
force_plot_LR           = 1
force_plot_RF           = 1
vel_plot                = 0
stack_topo_plot         = 0
# stack_gem_plot

#---------------------------------- SETTING -----------------------------------
path = '/home/jiching/geoflac/'
#path = '/scratch2/jiching/22winter/'
#path = '/scratch2/jiching/03model/'
#path = 'F:/model/'
savepath='/home/jiching/geoflac/data/'
figpath='/home/jiching/geoflac/figure/'
model_list=['chimex0601','chimex0602','chimex0603','chimex0604','chimex0605','chimex0606','chimex0607','chimex0608','chimex0609','chimex0610','chimex0611']
newcolors = ['#AE6378','#282130','#7E9680','#24788F','#849DAB','#EA5E51','#35838D','#4198B9','#414F67','#97795D','#6B0D47','#A80359','#52254F']
os.chdir(path+model)

fl = flac.Flac();end = fl.nrec
##------------------------------------ plot -----------------------------------
if trench_plot:
    print('--- start plotting the trench and topography with time ---')
    fig, (ax)= plt.subplots(1,1,figsize=(10,12))
    for kk,model in enumerate(model_list):
        name='trench_for_'+model
        df = pd.read_csv(savepath+name+'.csv')
        dis,time,topo=get_topo(start=1,end_frame=end)
        ax.plot(df.trench_x[df.trench_x>0],df.time[df.trench_x>0],lw=2,label=model,color=newcolors[kk])
    ax.set_xlim(0,dis[-1][-1])
    ax.set_ylim(0,df.time[-1])
    ax.set_title(str(model)+" Bathymetry Evolution",fontsize=24)
    ax.set_ylabel('Time (Myr)',fontsize=20)
    ax.set_xlabel('Distance (km)',fontsize=20)
    fig.savefig(figpath+'compare_trench_location_'+model_list[0]+'_'+model_list[-1]+'.png')
    print('=========== DONE =============')
if dip_plot:
    print('--- start plot dip with time ---')
    fig, (ax2)= plt.subplots(1,1,figsize=(10,7))
    for kk,model in enumerate(model_list):
        name = 'plate_dip_of_'+model
        depth1,depth2 = dip_setting(-5,-120)
        df = pd.read_csv(savepath+name+'.csv')
        ax2.plot(df.time[df.angle>0],df.angle[df.angle>0],,lw=2,label=model,color=newcolors[kk])
    ax2.set_xlim(0,df.time[-1])
    ax2.set_title('Angle Variation',fontsize=24)
    ax2.set_xlabel('Time (Myr)',fontsize=20)
    ax2.set_ylabel('Angel ($^\circ$) from '+str(-depth1)+' to '+str(-depth2)+' depth',fontsize=20)
    ax2.grid()
    fig.savefig('/home/jiching/geoflac/'+'figure/'+model+'_dip.jpg')
    print('=========== DONE =============')
if plate_geometry:
    print('--- start plot geometry ---')
    fig2, (ax2) = plt.subplots(1,1,figsize=(8,6))
    for kk,model in enumerate(model_list):
        xmean,ztop=np.loadtxt('/home/jiching/geoflac/data/'+str(model)+'_stack_slab.txt').T
        ax2.plot(xmean,ztop,c=newcolors[kk],label=model,lw=3)
    ax2.set_xlim(-10,500)
    ax2.set_title("slab comparation")
    ax2.set_ylabel("Depth (km)")
    ax2.set_xlabel("Distance relative to trench (km)",fontsize=16)
    ax2.legend(fontsize=16)
    fig2.savefig('/home/jiching/geoflac/figure'+'/'+'multi_slab_analysis_'+model_list[0]+'_'+model_list[-1]+'.png')
    print('=========== DONE =============')
if force_plot_LR:
    print('--- start plot left and right force with time ---')
    fig, (ax,ax2)= plt.subplots(2,1,figsize=(12,8))   
    for kk,model in enumerate(model_list):
        filepath = '/home/jiching/geoflac/'+model+'/forc.0'
        temp1=np.loadtxt(filepath)
        nloop,time,forc_l,forc_r,ringforce,vl,vr,lstime,limit_force = temp1.T
        ax.scatter(time,forc_l,s=4,label=model,color=newcolors[kk])
        ax2.scatter(time,forc_r,s=4,label=model,color=newcolors[kk])
    ax.set_xlim(0,time[-1])
    ax.set_title('oceanic side force',fontsize=16)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.grid()
    ax2.set_xlim(0,time[-1])
    ax2.set_title('continental side force',fontsize=16)
    ax2.tick_params(axis='x', labelsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    ax2.grid()
    fig.savefig(figpath+model+'_forc.png')
    print('=========== DONE =============')
if force_plot_RF:
    print('--- start plot ringforce with time ---')
    fig2, (ax3)= plt.subplots(1,1,figsize=(10,8))   
    for kk,model in enumerate(model_list):
        filepath = '/home/jiching/geoflac/'+model+'/forc.0'
        temp1=np.loadtxt(filepath)
        nloop,time,forc_l,forc_r,ringforce,vl,vr,lstime,limit_force = temp1.T
        ax3.scatter(time,ringforce,s=2,label=model,color=newcolors[kk])
    ax3.set_xlim(0,time[-1])
    ax3.tick_params(axis='x', labelsize=16)
    ax3.tick_params(axis='y', labelsize=16)
    ax3.grid()
    fig2.savefig(figpath+model+'_ringforc.png')
    print('=========== DONE =============')
if vel_plot:
    print('--- start plot velocity with time ---')
    fig3, (ax4)= plt.subplots(1,1,figsize=(10,8))
    for kk,model in enumerate(model_list):
        filepath = '/home/jiching/geoflac/'+model+'/forc.0'
        temp1=np.loadtxt(filepath)
        nloop,time,forc_l,forc_r,ringforce,vl,vr,lstime,limit_force = temp1.T
        ax4.plot(time,vl*31545741325,lw=2,label=model,color=newcolors[kk])
    ax4.set_xlim(0,time[-1])
    ax4.set_title('oceanic side velocity',fontsize=16)
    ax4.tick_params(axis='x', labelsize=16)
    ax4.tick_params(axis='y', labelsize=16)
    ax4.grid()
    ax4.set_xlabel('Time (Myr)',fontsize=16)
    ax4.set_ylabel('Velocity (mm/yr)',fontsize=16)
    fig3.savefig(figpath+model+'_vel.png')
    print('=========== DONE =============')
if stack_topo_plot:
    print('--- start plot topo with time ---')
    fig2, (ax2) = plt.subplots(1,1,figsize=(8,6))
    for kk,model in enumerate(model_list):
        name=model+'_stack_topography.txt'
        xmean,ztop=np.loadtxt(path+'data/'+name).T
        ax2.plot(xmean,ztop,lw=3,label=model,color=newcolors[kk])
    fig2.savefig(figpath+model+'_topo_analysis.png')
    print('=========== DONE =============')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:45:24 2022

@author: ji-chingchen
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
import function_for_flac as fd
import matplotlib.pyplot as plt
from numpy import unravel_index

model = str(sys.argv[1])
figpath='/home/jiching/geoflac/figure/'
path = '/home/jiching/geoflac/'+model+'/'
#path = '/Volumes/My Book/model/'+model+'/'
savepath = '/Users/ji-chingchen/Desktop/data/'
os.chdir(path)
fl = flac.Flac();end = fl.nrec
nex = fl.nx - 1;nez = fl.nz - 1

def nodes_to_elements(xmesh,zmesh):
    ele_x = (xmesh[:fl.nx-1,:fl.nz-1] + xmesh[1:,:fl.nz-1] + xmesh[1:,1:] + xmesh[:fl.nx-1,1:]) / 4.
    ele_z = (zmesh[:fl.nx-1,:fl.nz-1] + zmesh[1:,:fl.nz-1] + zmesh[1:,1:] + zmesh[:fl.nx-1,1:]) / 4.
    return ele_x, ele_z

depth = 0
def plot_phase_in_depth(depth=0):
    time=[];ph=[];xx=[]
    for step in range(end):
        x, z = fl.read_mesh(step+1)
        phase=fl.read_phase(step+1)
        ele_x, ele_z = nodes_to_elements(x,z)
        xt = ele_x[:,0]
        zt = ele_z[:,0]
        pp = np.zeros(xt.shape)
        t = np.zeros(zt.shape)
        t[:]=fl.time[step]
        for gg in range(len(ele_z)):
            pp[gg]=phase[gg,depth]
        time.append(t)
        ph.append(pp)
        xx.append(xt)
    return xx, time, ph

print('-----plotting single layer-----')
name = 'phase_for'+model
fig, (ax)= plt.subplots(1,1,figsize=(10,12))
colors = ["#CECCD0","#FF00FF","#8BFF8B","#7158FF","#FF966F",
      "#9F0042","#660000","#524B52","#D14309","#5AB245",
      "#004B00","#008B00","#455E45","#B89FCE","#C97BEA",
      "#525252","#FF0000","#00FF00","#FFFF00","#7158FF"]
phase15= matplotlib.colors.ListedColormap(colors)
#rainbow = cm.get_cmap('Set1',20)
#colors = rainbow(np.linspace(0, 1, 20))
#phase15= matplotlib.colors.ListedColormap(colors)
xt,t,pp= plot_phase_in_depth(depth=0)    
new_phase = np.zeros(pp.size)
for mm in range(len(pp)):
    for kk,qq in enumerate(pp):
        if qq == 14:
            new_phase[kk] = 1
        else:
            new_phase[kk] = 0
colors = ["#ffffff","#f0a224"]

phase15= matplotlib.colors.ListedColormap(colors)
colors1 = ["#ffffff","#1a1010"]
phase16= matplotlib.colors.ListedColormap(colors1)
fig, (ax)= plt.subplots(1,1,figsize=(7,9))
for step in range(end):
    x, z = fl.read_mesh(step+1)
    phase=fl.read_phase(step+1)
    ele_x, ele_z = nodes_to_elements(x,z)
    xt = ele_x[:,0]
    zt = ele_z[:,0]
    pp = np.zeros(xt.shape)
    qq = np.zeros(xt.shape)
    t = np.zeros(zt.shape)
    t[:] = fl.time[step]
    for gg in range(len(ele_z)):
        if phase[gg,depth]==14:
            pp[gg]=1
#        elif phase[gg,depth]==2 or phase[gg,depth]==4:
#            pp[gg]=2
#        elif phase[gg,depth]==3 or phase[gg,depth]==10:
#            pp[gg]=3
        else:
            pp[gg]=0        
        if ele_z[gg,0]-(np.average(ele_z[:,0]))>2.0:
           qq[gg] = 1
        else:
           qq[gg]=0 
    ax.scatter(xt,t,c=qq,cmap=phase16)
    ax.scatter(xt,t,c=pp,cmap=phase15,alpha = 0.2)

ax.set_ylabel("Time (Ma)")
ax.set_xlabel("Distance (km)")
ax.set_title(str(model)+" Phase")
ax.set_ylim(0,30)
ax.set_xlim(200,700)
bwith = 3
ax.spines['bottom'].set_linewidth(bwith)
ax.spines['top'].set_linewidth(bwith)
ax.spines['right'].set_linewidth(bwith)
ax.spines['left'].set_linewidth(bwith)
# cb_plot1 = ax.scatter([-1],[-1],s=0.1,c=[1],cmap=phase15,vmin=1, vmax=18)
# ax_cbin = fig.add_axes([0.27, 0.03, 0.23, 0.03])
# cb = fig.colorbar(cb_plot1,cax=ax_cbin,orientation='horizontal')
# ax_cbin.set_title('Phase')
fig.savefig(figpath+model+'_phase.png')
print('=========== DONE =============')

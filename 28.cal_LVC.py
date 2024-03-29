#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:17:25 2022

@author: ji-chingchen
"""
import sys,os
import math
import numpy as np
import flac
import flacmarker2vtk
import matplotlib
matplotlib.use('Agg')
import function_for_flac as fd
import matplotlib.pyplot as plt


path = '/home/jiching/geoflac/'
#path = '/scratch2/jiching/22winter/'
#path = '/scratch2/jiching/03model/'
path = '/scratch2/jiching/04model/'
#path ='/Volumes/My Book/model/03model/'
#path = '/Users/chingchen/Desktop/model/'
savepath='/scratch2/jiching/data/'
#savepath='/Users/chingchen/Desktop/data/'
figpath='/scratch2/jiching/figure/'
#figpath='/Users/chingchen/Desktop/figure/'

model = 'Nazca_a0634'
os.chdir(path+model)
fl = flac.Flac()
time=fl.time
end = fl.nrec
nex = fl.nx - 1
nez = fl.nz - 1
bwith=3

#time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
fig3,(ax3,ax4)=plt.subplots(2,1,figsize=(20,18))
fig,(aa)=plt.subplots(1,1,figsize=(10,6))
ax3.grid()
ax4.grid()
color=['#2F4F4F','#4682B4','#CD5C5C','#708090',
      '#AE6378','#282130','#7E9680','#24788F',
      '#849DAB','#EA5E51','#35838D','#4198B9',
      '#414F67','#97795D','#6B0D47','#A80359',
      '#52254F','r'] 
model_list=['ch1519','ch1522','ch1406','ch1512','ch1513','ch1510',
            'ch1520','ch1528','ch1529','ch1521','ch1530','ch1531',
            'ch1516','ch1517','ch1404','ch1523','ch1532','ch1533']
model_list=['ch1522','ch1512','ch1513','ch1510','ch1528','ch1529','ch1521',
            'ch1530','ch1531','ch1517','ch1404','ch1532','ch1519','ch1406',
            'ch1520','ch1516','ch1523','ch1533','ch1520']
model_list=['Nazca_a0634','Nazca_a0637','Nazca_a0640','Nazca_a0643',
            'Nazca_a0633','Nazca_a0636','Nazca_a0635',
            'Nazca_a0631','Nazca_a0630','Nazca_a0642','Nazca_a0641',
            'Nazca_a0644','Nazca_a0645']
def nodes_to_elements(xmesh,zmesh):
    ele_x = (xmesh[:fl.nx-1,:fl.nz-1] + xmesh[1:,:fl.nz-1] + xmesh[1:,1:] + xmesh[:fl.nx-1,1:]) / 4.
    ele_z = (zmesh[:fl.nx-1,:fl.nz-1] + zmesh[1:,:fl.nz-1] + zmesh[1:,1:] + zmesh[:fl.nx-1,1:]) / 4.
    return ele_x, ele_z
def oceanic_slab(frame):
    phase_oceanic = 3
    phase_ecolgite = 13
    phase_oceanic_1 = 17
    phase_ecolgite_1 = 18
    x, z = fl.read_mesh(frame)
    ele_x, ele_z = nodes_to_elements(x,z)
    phase = fl.read_phase(frame)
    trench_ind = int(trench_index[frame-1])
    crust_x = np.zeros(nex)
    crust_z = np.zeros(nex)
    for j in range(trench_ind,nex):
        ind_oceanic = (phase[j,:] == phase_oceanic) + (phase[j,:] == phase_ecolgite)+(phase[j,:] == phase_oceanic_1) + (phase[j,:] == phase_ecolgite_1)
        if True in ind_oceanic:
            kk = ele_z[j,ind_oceanic]
            xx = ele_x[j,ind_oceanic]
            if len(kk[kk<-15])==0:
                continue
            crust_x[j] = np.max(xx[kk<-15])
            crust_z[j] = np.max(kk[kk<-15])
    return crust_x,crust_z
def oceanic_slab2(frame,x,z,phase,trench_index):
    phase_oceanic = 3
    phase_ecolgite = 13
    phase_oceanic_1 = 17
    phase_ecolgite_1 = 18
    ele_x, ele_z = nodes_to_elements(x,z)
    trench_ind = int(trench_index[frame-1])
    crust_x = np.zeros(len(ele_x))
    crust_z = np.zeros(len(ele_x))
    for j in range(trench_ind,len(ele_x)):
        ind_oceanic = (phase[j,:] == phase_oceanic) + (phase[j,:] == phase_ecolgite)+(phase[j,:] == phase_oceanic_1) + (phase[j,:] == phase_ecolgite_1)
        if True in ind_oceanic:
            kk = ele_z[j,ind_oceanic]
            xx = ele_x[j,ind_oceanic]
            if len(kk[kk<-15])==0:
                continue
            crust_x[j] = np.max(xx[kk<-15])
            crust_z[j] = np.max(kk[kk<-15])       
    return crust_x,crust_z
def temp_elements(temp):
    ttt = (temp[:fl.nx-1,:fl.nz-1] + temp[1:,:fl.nz-1] + temp[1:,1:] + temp[:fl.nx-1,1:]) / 4.
    return ttt
def trench(start_vts=1,model_steps=end):
    trench_x=np.zeros(end)
    trench_z=np.zeros(end)
    trench_index=np.zeros(end)
    for i in range(start_vts,model_steps):
        x,z = fl.read_mesh(i)
        sx,sz=fd.get_topo(x,z)
        arc_ind,trench_ind=fd.find_trench_index(z)
        trench_index[i]=trench_ind
        trench_x[i]=sx[trench_ind]
        trench_z[i]=sz[trench_ind]
    return trench_index,trench_x,trench_z
# trench_index,trench_x,trench_z=trench()
#model_list = [model]
depth1 = 80
depth2 = 130
for www,model in enumerate(model_list):
    os.chdir(path+model)
    fl = flac.Flac()
    time=fl.time
    end = fl.nrec
    nex = fl.nx - 1
    nez = fl.nz - 1
    viswedge=np.zeros(end)
    areawedge=np.zeros(end)
    temwedge=np.zeros(end)
    channel = np.zeros(end)
    time, trench_index,trench_x,trench_z = np.loadtxt(savepath+'trench_for_'+model+'.txt').T
    for i in range(1,end+1):
        x, z = fl.read_mesh(i)
        phase = fl.read_phase(i)
        vis=fl.read_visc(i)
        area=fl.read_area(i)
        ele_x, ele_z = nodes_to_elements(x,z)
        # crust_x,crust_z = oceanic_slab(i)
        crust_x,crust_z = oceanic_slab2(i, x, z, phase, trench_index)
        temp = fl.read_temperature(i)
        ele_tem = temp_elements(temp)
        magma = fl.read_fmagma(i)
        wedge_area = np.zeros(nex-int(trench_index[i-1]))
        # fig2,aa=plt.subplots(1,1,figsize=(10,6))
        # aa.scatter(ele_x,ele_z,c=vis,s = 300)
        for ii in range(int(trench_index[i-1]),nex):
            if crust_z[ii]<-depth2:
                break
            if magma[ii,:].all() == 0:
                continue  
            up= (ele_z[ii,:]> crust_z[ii])*(ele_z[ii,:]<-depth1)*(vis[ii,:]<=22)*(magma[ii,:]>=1e-5)
            if True in up:
                wedge_area[ii-int(trench_index[i-1])]=np.mean(area[ii,up]/1e6)
                areawedge[i-1]+=sum(area[ii,up]/1e6)
                viswedge[i-1]+=np.mean(vis[ii,up])
                temwedge[i-1]+=np.mean(ele_tem[ii,up])
                channel[i-1]=(max(ele_z[ii,up])-min(ele_z[ii,up]))
                # aa.scatter(ele_x[ii,up],ele_z[ii,up],c='w',s=50)
        if len(wedge_area[wedge_area>0])==0:
            continue
        temwedge[i-1] = temwedge[i-1]/len(wedge_area[wedge_area>0])
    ccc = fd.moving_window_smooth(channel[channel>0],10)
    if www >3:
        ax3.plot(fl.time[channel>0], ccc,c = color[3],lw=3,label = model)
        aa.plot(fl.time[channel>0], ccc,c = color[3],lw=3,label = model)
        ax4.plot(fl.time[channel>0], temwedge[channel>0],c = color[3],lw=3,label = model)
    else:
        ax3.plot(fl.time[channel>0], ccc,c = color[2],lw=3,label = model)
        aa.plot(fl.time[channel>0], ccc,c = color[2],lw=3,label = model)
        ax4.plot(fl.time[channel>0], temwedge[channel>0],c = color[2],lw=3,label = model)
#ax3.legend(fontsize = 25)
    ax3.set_ylim(0,40)
for ax in [ax3,ax4,aa]:
    ax.set_xlim(0,20)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
fig3.savefig(figpath+model_list[0]+'_'+model_list[-1]+'_wedgechannel3_21.png')
fig.savefig(figpath+model_list[0]+'_'+model_list[-1]+'_wedgechannel.png')

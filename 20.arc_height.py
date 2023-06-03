#!/usr/bin/env python3
import math
import flac
import os,sys
import numpy as np
from matplotlib import cm
# import creat_database as cd
import matplotlib.pyplot as plt
# from Main_creat_database import oceanic_slab,nodes_to_elements
# model = str(sys.argv[1])
model = 'Ref_Cocos'
path = '/home/jiching/geoflac/'+model+'/'
#path = '/Volumes/My Book/model/'+model+'/'
path = '/Users/chingchen/Desktop/model/'
os.chdir(path+model)
fl = flac.Flac();end = fl.nrec
nex = fl.nx - 1;nez = fl.nz - 1
rainbow = cm.get_cmap('gray_r',end)
newcolors = rainbow(np.linspace(0, 1, end))
fig, (ax)= plt.subplots(1,1,figsize=(17,12))
#============================Time Series==========================
arc_thickness = np.zeros(end)
magma = np.zeros(end)
cc=0
arc_phase  = 14
#----------------------------Main code----------------------------
for i in range(1,end):
    phase=fl.read_phase(i)
    x,z=fl.read_mesh(i)
    ele_x, ele_z = flac.elem_coord(x, z)
    height = np.zeros(nex)
    for xx in range(0,nex):
        if phase[xx,0]==arc_phase:
            for zz in range(0,nez):
                if phase[xx,zz]!=arc_phase:
                    break
            height[xx]=z[xx,0]-z[xx,zz]
    ax.plot(ele_x[:,0],height,color=newcolors[i])
    arc_thickness[i]=np.average(height)
print(arc_thickness)
#----------------------------------------------------------------------------
# fig.savefig('/home/jiching/geoflac/'+'figure/'+model+'_arc_thickness.png')

cmap = plt.cm.get_cmap('gist_earth')
zmax, zmin =10, -10
trench_x = np.zeros(end)
trench_t = np.zeros(end)
arc_x = np.zeros(end)
fig, (ax) = plt.subplots(1,1,figsize=(10,12))

for i in range(end):
    x, z = fl.read_mesh(i+1)
    xmax = np.amax(x)
    xmin = np.amin(x)

    xt = x[:,0]
    zt = z[:,0]
    t = np.zeros(xt.shape)
    t[:] = i*0.2
    ax.scatter(xt,t,c=zt,cmap=cmap,vmin=zmin, vmax=zmax)
    trench_t[i] = t[0]
    trench_x[i] = xt[np.argmin(zt)]
    arc_x[i] = xt[np.argmax(zt)]
ind_within=(arc_x<900)*(trench_x>100)
#ax.plot(arc_x[ind_within],trench_t[ind_within],c='r',lw=4)
ax.plot(trench_x[ind_within],trench_t[ind_within],'k-',lw='4')
ax.set_xlim(400,800)
ax.set_ylim(0,t[0])
ax.set_title(str(model)+" Bathymetry Evolution")
ax.set_ylabel("Time (Ma)")
ax.set_xlabel("Distance (km)")
distance=arc_x-trench_x
#ax2.plot(distance[ind_within],trench_t[ind_within],c='b',lw=4)    
#ax2.set_ylim(0,t[0])
#ax2.set_xlabel('Distance between arc and trench (km)')

ax_cbin = fig.add_axes([0.67, 0.18, 0.23, 0.03])
cb_plot = ax.scatter([-1],[-1],s=0.1,c=[1],cmap=cmap,vmin=zmin, vmax=zmax)
cb = fig.colorbar(cb_plot,cax=ax_cbin,orientation='horizontal')
ax_cbin.set_title('Bathymetry (km)')
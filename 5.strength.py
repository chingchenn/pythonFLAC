#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 17:01:45 2021

@author: jiching
"""

import numpy as np
import function_for_flac as f2
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

# ----------------------------- initial setup ---------------------------------
'''
oceanic litho, SA                    =   1
normal continental litho, therm 3    =   2
depleted continental litho, therm 3  =   3
normal continental litho, therm 4    =   4
depleted continental litho, therm 4  =   5
strong lower crust  therm 3          =   6
s1518 colser trench geology          =   7
s1517 geology 			             =   8
oceanic litho, MEX                   =   9
'''

geo = 3
withregion = 0
max_depth = 60
# -------------------------------- geology zone ------------------------------- 
if geo == 1:
    layerz = (0, 1.5e3, 7.5e3, 10e3)   # 1st elem must be 0
    phase=[11,3,3,4]
    tem=1
elif geo==2:
    layerz = (0, 18e3, 26e3)
    phase=[2,6,4]
    tem=3
elif geo==3:
    layerz = (0, 18e3, 30e3, 40e3)
    phase=[2,14,8,4]
    tem=3
elif geo==4:
    layerz = (0, 18e3, 30e3)
    phase=[2,6,4]
    tem=3
elif geo==5:
    layerz = (0, 18e3, 30e3, 55e3)
    phase=[2,6,19,4]
    tem=3
elif geo==6:
    layerz = (0, 16e3, 26e3)
    phase=[2,1,4]
    tem=3
elif geo==7:
    layerz = (0, 15e3,40e3)
    phase=[2,4,4]
    tem=1
elif geo==8:
    layerz = (0, 25e3,35e3)
    phase=[2,14,4]
    tem=4
elif geo == 9:
    layerz = (0, 2e3, 7e3, 16e3)
    phase=[11,3,16,4]
    tem=2
#---------------------------- read phase from csv -----------------------------
pu=[]
for yy in range(20):
    pu.append(f2.phase_pro(yy))
#----------------------------- creat Dfc array --------------------------------
pp=[]
dfc=[0,10,12]
for qqq in phase:
    for nnn in dfc:    
        pp.append(pu[qqq][nnn])
Dfc=np.array(pp).reshape(len(phase),3)
#----------------------------- creat nAE array --------------------------------
pp=[]
nae=[3,4,5]
for qqq in phase:
    for nnn in nae:    
        pp.append(pu[qqq][nnn])
nAEs=np.array(pp).reshape(len(phase),3)
#---------------------- define strain rate & Temperature ----------------------
edot = 1e-14  # high strain rate
edot = 1e-15  # low strain rate
deepz = layerz[-1] * 20
z = np.linspace(0, deepz, num=1000)
if tem == 1:
    T = f2.half_space_cooling_T(z, 10, 1330, 40)
    print('geo='+str(geo))
elif tem==3:
    T = f2.continental_geothermal_T3(z,22,6,40)
    print('geo='+str(geo))
elif tem==4:
    T = f2.continental_geothermal_T4(z, 10,1330, 130)
    print('geo='+str(geo))
elif tem == 2:
    T = f2.half_space_cooling_T(z, 10, 1330, 15)
    print('geo='+str(geo))
#------------------------------------------------------------------------------
# equation soluiton of plastic stress and viscosity
frico_strength = f2.plastic_stress(z,layerz,Dfc)
visc = f2.visc_profile(z, T, edot, layerz, nAEs)
visco_strength = visc* edot *2 #Pa
#------------------------------------------------------------------------------
fig, ax = plt.subplots(1,1,figsize=(7,10))
applied_strength = np.amin((visco_strength,frico_strength),axis=0)
bwith = 5
ax.spines['bottom'].set_linewidth(bwith)
ax.spines['top'].set_linewidth(bwith)
ax.spines['right'].set_linewidth(bwith)
ax.spines['left'].set_linewidth(bwith)
# mm1,=ax.plot(visco_strength/1e6,z/1000,'--r',alpha=0.8,label = 'visco')
# mm2,=ax.plot(frico_strength/1e6,z/1000,'--b',alpha=0.8,label = 'plastic')
mm3,=ax.plot(applied_strength/1e6,z/1000,'k',label = 'final stress',lw=5)

ax.tick_params(axis='x', labelsize=26)
ax.tick_params(axis='y', labelsize=26)
# ax.set_title('Rock Strength',fontsize=30)
# ax.set_xlabel('Strength (MPa) / Temperature ($^\circ$C)',fontsize=20)
ax.set_xlabel('Strength (MPa)',fontsize=20)
ax.set_ylabel('Depth (km)',fontsize=26)
ax.set_ylim(max_depth,0)                                     
ax.set_xlim(0,1500)
ax.grid()
ax2 = ax.twinx()
temp = z/1000*0.6+T
# mm4,=ax2.plot(temp,z/1000,color='green',label='temperature',lw=5)
# mm=[mm1,mm2,mm3]#,mm4]
ax2.set_xlim(0,1000)
ax2.set_ylim(max_depth,0)
ax2.axes.yaxis.set_visible(False)
# ax.legend(mm, [curve.get_label() for curve in mm],fontsize=20,loc = 'lower left')
## ------------------------------  Elastic Plot  ------------------------------
if withregion:
    elastic =-z[applied_strength==frico_strength]/1000
    for rr in range(1,len(elastic)):
        if elastic[rr] > -100 and abs(elastic[rr-1]-elastic[rr]) <1 :
            ax.axhspan(elastic[rr-1],elastic[rr],facecolor='royalblue', alpha=0.45)
# ax.fill_between(applied_strength/1e6, -z/1000, facecolor='tab:cyan', interpolate=True,alpha=0.6)
fig.savefig('/Users/ji-chingchen/OneDrive - 國立台灣大學/年會/2022/POSTER/'+'strength_profile_ex'+'.pdf')

## --------------------------------  Intergal  --------------------------------
tol = 0
tt=np.zeros(len(z))
for ww in range(1,len(z)):
    tol += applied_strength[ww] *(z[ww]-z[ww-1])/1e9
    tt[ww] = applied_strength[ww]*(z[ww]-z[ww-1])/1e9
# print(tol)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 23/03/2025
@author: i-rok
"""
'''
To plot the OMA and OMB from netcdf file. the nc file is created from plot_gts_omb_oma.ncl
script
'''
import time
start=time.time()
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import glob

def RMSE(data,obs):
    dif=(data-obs)**2
    n=data.shape[0]
    rmse=np.sqrt(np.nanmean(dif))
    return rmse

color_list=['red','blue','orange']
files=glob.glob('/media/irok/hdd/data/wrfout/27052024/wind_profiler_exp/da_combined_thompson_gf_new_test/gts_omb_oma_profiler_*.nc')
fig, axs=plt.subplots(1,3,sharex=True, sharey=True,)
axs=axs.ravel()
################## Vertical profile of OMA and OMB
for i,file in enumerate(files):
	data=xr.open_mfdataset(file)
	fname=file.split('/')[-2]
	data=data.squeeze()
	# fig=plt.figure()
	# ax=plt.axes()
	axs[i].plot(data.VOMB.values,data.PRES.values/1000,color=color_list[1],alpha=0.7,label='OMB',ls='-')
	axs[i].plot(data.VOMA.values,data.PRES.values/1000,color=color_list[2],alpha=0.7,label='OMA',ls='--')
	axs[i].axvline(x=0,color='k',ls='--',lw=0.3)
	axs[i].set_title(data.attrs["ob_date"])
	axs[i].set_ylim(0,18)
	axs[i].set_xlim(-15,15)
axs[1].set_xlabel('V wind (m/s)')
axs[0].set_ylabel('Height (Km)')
axs[i].legend(labelspacing=0.3,handletextpad=0.5,fontsize=7,handlelength=2)

fig.savefig(f'/media/irok/hdd/python_files/python_plots/test/gts_omb_oma_{fname}_{data.attrs["ob_date"]}_vwnd.png',bbox_inches='tight', dpi=500,)


end = time.time()
print ("Time taken: ", (end-start), "s")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 17-04-2024 12:54:36
@author: irok
"""
'''
To plot 3hr accumulated rainfall for 24hr stamp for WRF out put
'''

import time
start=time.time()
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from cartopy.mpl.ticker import LongitudeFormatter
from cartopy.mpl.ticker import LatitudeFormatter
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from python_functions import getdata
import glob
from irok_wrf import wrf_datas
import cmaps

# plt.rcParams['font.family']='Arial'
# plt.rcParams['text.usetex']=True
# plt.rcParams['axes.spines.top']=False
# plt.rcParams['axes.spines.right']=False
plt.rcParams['axes.linewidth']=.2
# plt.rcParams['lines.linewidth']=.4
plt.rcParams['axes.labelsize']=4
# plt.rcParams['axes.titlesize']=10
# plt.rcParams['axes.labelpad']=.5
plt.rcParams['xtick.labelsize']=4
plt.rcParams['ytick.labelsize']=4
plt.rcParams['xtick.major.width']=plt.rcParams[
        'axes.linewidth']
plt.rcParams['ytick.major.width']=plt.rcParams[
        'axes.linewidth']
plt.rcParams['xtick.minor.width']=.2
plt.rcParams['ytick.minor.width']=.2
plt.rcParams['xtick.major.size']=2
plt.rcParams['ytick.major.size']=2
# plt.rcParams['xtick.minor.size']=2
# plt.rcParams['ytick.minor.size']=2
plt.rcParams['xtick.major.pad']=.2
plt.rcParams['ytick.major.pad']=.2

lat = 10.04205  
lon = 76.33216 
date='2024-05-28'
start_date='2024-05-28 03:00'
end_date='2024-05-28 06:00'
min_lon,max_lon=76,77.2
min_lat,max_lat=9.6,10.45
# min_lon,max_lon=74,78
# min_lat,max_lat=8,12
xticks=np.arange(min_lon,max_lon+1,0.25)
yticks=np.arange(min_lat,max_lat+1,0.25)
src_crs=ccrs.PlateCarree()
text_color='#000000'
shapefile_path=('/media/irok/hdd/python_files/shape_files/Kerala_District_Boundary/Kerala_District_Boundary_4326.shp')
shape_feature=ShapelyFeature(
        Reader(shapefile_path).geometries(),
        src_crs, edgecolor='black',
        facecolor='none', lw=.2)
shape_feature1=ShapelyFeature(
        Reader('/media/irok/hdd/python_files/shape_files/kerala_villages/village.shp').geometries(),
        src_crs, edgecolor='blue',
        facecolor='none', lw=.1)
fname='/media/irok/hdd/data/wrfout/27052024/wind_profiler_exp/no_da/thompson_gf/wrfout_d02_2024-05-27_18_00_00'
# fname='/media/irok/hdd/data/wrfout/27052024/mwr_exp/cyc_27th/27_18utc/wrfout_d03_2024-05-27_18_00_00'
fname='/media/irok/hdd/data/wrfout/27052024/wind_profiler_exp/da_combined_thompson_gf_new_test/2024052718/wrfout_d02_2024-05-27_18_00_00'

file=fname.split('/')[-3]
da=wrf_datas(fname=fname)
da.total_rain()
rr=da.rain_rate()

rain=rr.rain_rate.sel(longitude=slice(min_lon,max_lon),latitude=slice(min_lat,max_lat),Time=slice(start_date,end_date))
rain=rain.sum(dim='Time')

#### To plot as single plot

fig=plt.figure(figsize=(2.0, 2))
ax = plt.axes(projection=src_crs)
f=ax.pcolormesh(rain.longitude,rain.latitude,rain,vmin=0,vmax=141,cmap=cmaps.precip3_16lev,transform=src_crs,)
ax.scatter(lon,lat,s=0.5,marker='*',color='k')
# ax.set_title(f'3hr accumualtion from {start_date} to {end_date}',fontsize=6,pad=5)
# axs[i].add_feature(shape_feature1)
ax.add_feature(shape_feature)
ax.set_yticks(yticks, crs=ccrs.PlateCarree())
ax.set_xticks(xticks, crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.tick_params(axis='both',labelsize=3.5,pad=2,length=1,width=0.3,direction='in',)
ax.set_extent((min_lon, max_lon, min_lat, max_lat), src_crs)
# if i in [0,3,6,9]:
# 	axs[i].set_yticks(yticks, crs=src_crs)
# if i in [9,10,11]:
# 	axs[i].set_xticks(xticks, crs=src_crs)
c=fig.colorbar(f,ax=ax,shrink=0.65,aspect=60,pad=0.01)
c.set_label('Rainfall (mm/hr)',fontsize=5)
c.ax.tick_params(labelsize=6)
# fig.suptitle(f'Rainfall {file}',x=0.47,y=.85,fontsize=8)
# fig.subplots_adjust(wspace = 0.1,hspace = -0.6,right=.77)
fig.subplots_adjust(
        left=.01, right=1-.01,
        bottom=.10, top=1-.01)
fig.savefig(f"/media/irok/hdd/python_files/python_plots/test/accumulation_{file}_{date}_d2.png",bbox_inches='tight', dpi=500,)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 03/07/2024
@author: i-rok
"""
'''
Plot ACARR AWS data
'''
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import metpy
from irok_wrf import wrf_datas
import glob
import matplotlib.dates as mdates

start_date='2024-05-27 23:00'
end_date='2024-05-28 11:00'
lat = 10.04205  
lon = 76.33216   

############ ACARR AWS
fname='/media/irok/hdd/data/acarr_aws/2024/CUSAT_ACARR_AWS-Main_Campus_20240528Minute.csv'
df=pd.read_csv(fname,skiprows=3,index_col=0,parse_dates=True)
df.index=df.index-pd.Timedelta(hours=5,minutes=30) ### to convert UTC
df1=df.loc[start_date:end_date]
# rain=df1['Tot'].rolling('1h').sum()
rain=df1['Tot'].cumsum()
# rain=df1['Tot'].resample('1h').sum()
######
fig=plt.figure(figsize=(10,5))
ax=plt.axes()
ax.plot(rain,label='AWS ACARR',color='k')
#### IMD AWS
fname='/media/irok/hdd/data/imd_rainfall_data/aws_data/imd_aws_kerala_kalamassery_20240527-20240529.csv'
imd_df=pd.read_csv(fname,index_col=0,parse_dates=True)
imd_data=imd_df['2024-05-27 03:15:00':'2024-05-28 03:00:00']
# imd_rain1=imd_data['Cum. RF since 0300 UTC (mm)'].diff()
imd_rain1=imd_df['2024-05-27 03:15:00':'2024-05-28 03:00:00']['Cum. RF since 0300 UTC (mm)'].diff().fillna(imd_df['Cum. RF since 0300 UTC (mm)'])
imd_rain2=imd_df['2024-05-28 03:15:00':'2024-05-29 03:00:00']['Cum. RF since 0300 UTC (mm)'].diff().fillna(imd_df['Cum. RF since 0300 UTC (mm)'])
imd_rain=pd.concat([imd_rain1,imd_rain2])
imd_rain=imd_rain.loc[start_date:end_date]
ax.plot(imd_rain.cumsum(),ls='--',label='AWS IMD',color='k')

#### INSAT HEM
insat_data=xr.open_dataset('/media/irok/hdd/data/insat_rainfall/insat-3dr_rainfall_hem.nc')
insat_data=insat_data.sel(time=slice(start_date, end_date))
ind=(insat_data.Latitude==10.05) & (insat_data.Longitude==76.34)
insat_rf=insat_data.where(ind,drop=True)
rf=insat_rf.HEM.cumsum(dim='time')/2
ax.plot(rf.time,rf.squeeze(),ls='-',label='INSAT HEM',color='brown')
#####
labels={'no_da':'No_DA','cyc':' WPR_DA','da_combined_thompson_gf_new_test':'WPR_DA'}
labels_styles={'no_da':'-.','da_combined_thompson_gf_new_test':':'}
files=[
'/media/irok/hdd/data/wrfout/27052024/wind_profiler_exp/no_da/thompson_gf/wrfout_d03_2024-05-27_18_00_00',
'/media/irok/hdd/data/wrfout/27052024/wind_profiler_exp/da_combined_thompson_gf_new_test/2024052718/wrfout_d03_2024-05-27_18_00_00',
]
# files=glob.glob('/media/irok/hdd/data/wrfout/27052024/**/wrfout_d03_2024-05-27_18_00_00',recursive=True)
for fname in files:
	file=fname.split('/')[-3]
	da=wrf_datas(fname=fname)
	da.total_rain()
	rr=da.rain_rate()
	mod_rain=rr.rain_rate.sel(longitude=lon,latitude=lat,method='nearest')
	mod_rain=mod_rain.sel(Time=slice(start_date,end_date),)
	mod_rain=mod_rain.cumsum(dim='Time')

	ax.plot(mod_rain.Time,mod_rain,label=labels[file],ls=labels_styles[file])
ax.set_ylabel('Rainfall (mm)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H-%M'))
# ax.margins(y=0,x=0)
ax.set_ylim([0,220])
ax.set_xlabel('UTC Time (HH:MM)')
ax.spines[['right', 'top']].set_visible(False)
ax.legend(labelspacing=0.3,handletextpad=0.5,fontsize=8,handlelength=2)
fig.savefig(f'/media/irok/hdd/python_files/python_plots/test/cumulative_aws_imd_hem_model_28May202418_thompson_gf_paper_new.png',bbox_inches='tight', dpi=300,)
# fig=plt.figure()
# ax=plt.axes()
# ax1=ax.twinx()
# ax.plot(rain,label='Rainfall',color='red')
# ax1.plot(era_data.time,mse1,label='Q*Lv',)
# ax1.plot(era_data.time,mse2,label='Cp*T',)
# ax1.plot(era_data.time,mse3,label='g*z',)
# fig.legend()
# fig.savefig(f'/media/irok/hdd/python_files/python_plots/test/era5_mse_terms_rain_28may2024.png',bbox_inches='tight', dpi=500,)
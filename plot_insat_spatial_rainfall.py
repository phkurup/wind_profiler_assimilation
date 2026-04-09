"""
author: abhiramcsn
"""
from datetime import timedelta
from pathlib import Path

# import cmocean
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.ticker as mticker
# import matplotlib.dates as mdates
import xarray as xr
from cartopy import crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter
from cartopy.mpl.ticker import LatitudeFormatter
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
# from cartopy import feature
import cmaps

# plt.rcParams['font.family']='Arial'
# plt.rcParams['text.usetex']=True
# plt.rcParams['axes.spines.top']=False
# plt.rcParams['axes.spines.right']=False
plt.rcParams['axes.linewidth']=.2
# plt.rcParams['lines.linewidth']=.4
plt.rcParams['axes.labelsize']=5
# plt.rcParams['axes.titlesize']=10
# plt.rcParams['axes.labelpad']=.5
plt.rcParams['xtick.labelsize']=5
plt.rcParams['ytick.labelsize']=5
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
# plt.rcParams['legend.fontsize']=8

if __name__=='__main__':
    # lon_min, lon_max=74.6, 77.5
    # lat_min, lat_max=8, 13
    # Ernakulam
    lon_min, lon_max=76, 77.2
    lat_min, lat_max=9.6, 10.45
    # lon_min,lon_max=74,78
    # lat_min,lat_max=8,12
    xticks=np.arange(lon_min,lon_max, .25)
    yticks=np.arange(lat_min,lat_max, .25)
    satellite='insat-3dr'
    # satellite='insat-3ds'

    which='hem'
    # which='imc'

    out_netcdf=(
            f'/media/irok/hdd/data/insat_rainfall/'
            f'{satellite}_rainfall_{which}.nc')
    if satellite=='insat-3dr':
        data_dir=f'./data/{satellite}/{which}'
        data_file_prefix='3RIMG_'
        start_time='2024-05-28 03:14'
        end_time='2024-05-28 05:46'
        slicer={
                'time':slice(start_time, end_time),
                'GeoX':slice(1300, 1500),
                'GeoY':slice(1050, 1200),
                }
        if which=='hem':
            cbar_levels=np.arange(0, 40+.1, 2)
        elif which=='imc':
            cbar_levels=np.arange(0, 15+.1, 1)
    elif satellite=='insat-3ds':
        start_time='2024-05-28 03:30'
        end_time='2024-05-28 04:00'
        # start_time='2024-05-28 05:00'
        # end_time='2024-05-28 05:30'
        data_dir=f'./data/{satellite}/{which}'
        data_file_prefix='3SIMG_'
        slicer={
                'time':slice(start_time, end_time),
                'GeoX':slice(1200, 1300),
                'GeoY':slice(1050, 1200),
                }
        if which=='hem':
            cbar_levels=np.arange(0, 40+.1, 2)
        elif which=='imc':
            cbar_levels=np.arange(0, 15+.1, 1)

    shape_file=(
            '/media/irok/hdd/python_files/shape_files'
            '/Kerala_District_Boundary/'
            'Kerala_District_Boundary_4326.shp')
    shape_file_obj=ShapelyFeature(
            Reader(shape_file).geometries(),
            ccrs.PlateCarree(), edgecolor='#000000',
            facecolor='none', lw=.12,
            )
    acarr_aws=[[76.332,], [10.0426,]]
    imd_aws=[[76.3317,], [10.0557,]]

    print(f'{data_dir}/{data_file_prefix}*.h5')
    out_netcdf=Path(f'{out_netcdf}')
    if out_netcdf.is_file():
        print(f'Reading data from {out_netcdf}')
        rf=xr.open_dataarray(out_netcdf)
    else:
        print('Combined file not available.')
        rf=xr.open_mfdataset(
                f'{data_dir}/{data_file_prefix}*.h5',
                chunks={'time':2},
                )[which.upper()]
        rf.sel(time='2024-05-28').to_netcdf(out_netcdf)
        print(f'NetCDF file written to {out_netcdf}')
    rf=rf.sel(slicer)

    time_period=rf.indexes['time'][[0, -1]].to_pydatetime()
    time_period[1]+=timedelta(minutes=30)

    img_name=(
            f"/media/irok/hdd/python_files/python_plots/test/"
            f"{satellite}_rainfall_{which}_"
            "ernakulam_"
            f"{time_period[0].strftime('%Y%m%d%H%M')}-"
            f"{time_period[1].strftime('%Y%m%d%H%M')}"
            '_contour_3hr'
            )

    time_period=(
            f"{time_period[0].strftime('%Y-%m-%d %H:%M')} -"
            f" {time_period[1].strftime('%Y-%m-%d %H:%M')} "
            "UTC"
            )

    print(time_period)
    rf=(rf.sum(dim='time')/2.).compute()
    print(rf.max())
    print(rf.mean())
    # rf=xr.where(rf>1, rf, np.nan)
    lons=rf['Longitude'].to_numpy()
    lats=rf['Latitude'].to_numpy()

    fig=plt.figure(figsize=(2.0, 2))
    ax=fig.add_subplot(
            111, projection=ccrs.PlateCarree(),
            )

    # cmap=cmocean.cm.rain
    colour_obj=ax.pcolormesh(
            lons, lats, rf, cmap=cmaps.precip3_16lev,
            # vmin=cbar_levels[0], vmax=cbar_levels[-1],
            vmin=0, vmax=40, #85
            # extend='max',
            # levels=cbar_levels, 
            )
    l=ax.contour(
            lons, lats, rf, 
            # cmap=cmaps.precip3_16lev,
            # vmin=cbar_levels[0], vmax=cbar_levels[-1],
            vmin=0, vmax=40, #85
            linewidths=0.2,colors='red',alpha=0.7,
            # extend='max',
            # levels=cbar_levels, 
            )
    # ax.set_title('Rainfall (mm)', fontsize=8, pad=.1)
    ax.coastlines('10m', lw=.1)
    ax.add_feature(shape_file_obj)
    ax.set_extent(
            [lon_min, lon_max, lat_min, lat_max],
            crs=ccrs.PlateCarree(),
            )
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.tick_params(
            axis='both',labelsize=3.5,pad=2,length=1,
            width=0.3,direction='in',
            )
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.scatter(
            *acarr_aws, s=4, facecolors='k',
            linewidths=.1, edgecolors='r',
            marker='.', label='ACARR-AWS',
            )
    # ax.scatter(
    #         *imd_aws, s=2, facecolors='none',
    #         linewidths=.1, edgecolors='b',
    #         marker='.', label='IMD-AWS',
    #         )
    text_box_props={
            'boxstyle':'square', 'facecolor':'w',
            'edgecolor':'none', 'pad':.05, 'alpha':.8,
            'mutation_aspect':3,
            # 'linewidth':.1,
            }
    # ax.text(
    #         .01, .008, s=time_period, fontsize=4,
    #         bbox=text_box_props, va='bottom',
    #         ha='left', transform=ax.transAxes,
    #         )

    cbar=fig.colorbar(
            colour_obj, 
            # orientation='horizontal',
            shrink=0.65,aspect=60,pad=0.01,
            # fraction=.035,  
            # ticks=cbar_levels,
            # aspect=40, pad=.01,
            )
    cbar.set_label(
            'Rainfall (mm)', fontsize=6, labelpad=.1,
            )
    cbar.ax.tick_params(
            axis='y', which='major',)# rotation=90)
    fig.subplots_adjust(
            left=.01, right=1-.01,
            bottom=.10, top=1-.01)
    fig.savefig(img_name+'.png',bbox_inches='tight', dpi=500)
    print(img_name+'.png')

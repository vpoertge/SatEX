# -*- coding: iso-8859-1 -*-
import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob
import iris
from iris.util import unify_time_units
import numpy as np
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import matplotlib.cm as mpl_cm
import iris.plot as iplt
import cartopy.crs as ccrs
import copy
import datetime
import netCDF4
import cf_units


def plot_years(x,y):
    plt.close()
    fig=plt.figure()
    plt.plot(x,y)
    plt.grid()
    plt.title('Time series of global average '+indexname+' values (GHCNDEX)')
    plt.savefig(OUTPATH+indexname+'_time_series_GHCNDEX.png')

def plot_map(data, lons, lats):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([ -30., 65., 30, 65. ], crs=ccrs.PlateCarree())

    cont = ax.contourf(lons, lats, year,transform=ccrs.PlateCarree(),cmap='nipy_spectral')
    ax.coastlines()
    cb=fig.colorbar(cont, ax=ax, orientation='horizontal')
    cb.set_label(indexname+' Index Value')
    plt.title('Map of '+indexname+' values (GHCNDEX) '+ str(CHOOSE_YEAR))
    plt.savefig(OUTPATH+indexname+'_GHCNDEX_map_'+str(CHOOSE_YEAR)+'.png')

def line(x,t,m):
    '''Plot a line. '''
    return m*x+t




#***************************************
def MedianPairwiseSlopes(xdata,ydata,mdi,mult10 = False, sort = False, calc_with_mdi = False):
    '''
    Calculate the median of the pairwise slopes

    :param array xdata: x array
    :param array ydata: y array
    :param float mdi: missing data indicator
    :param bool mult10: multiply output trends by 10 (to get per decade)
    :param bool sort: sort the Xdata first
    :returns: float of slope
    '''
    import numpy as np
    # sort xdata
    if sort:
        sort_order = np.argsort(xdata)

        xdata = xdata[sort_order]
        ydata = ydata[sort_order]

    slopes=[]
    y_intercepts = []
    for i in range(len(xdata)):
        for j in range(i+1,len(xdata)):
            if calc_with_mdi == True:
                if mdi[j] == False and mdi[i] == False: #changed from: if ydata[j]!=mdi and ydata[i]!=mdi:
                    slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                    y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]
            elif calc_with_mdi == False:
                slopes += [(ydata[j]-ydata[i])/(xdata[j]-xdata[i])]
                y_intercepts += [(xdata[j]*ydata[i]-xdata[i]*ydata[j])/(xdata[j]-xdata[i])]

    mpw=np.median(np.array(slopes))
    y_intercept_point = np.median(np.array(y_intercepts))

    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()

    good_data=np.where(ydata == False)[0]

    n=len(ydata[good_data])

    dof=n*(n-1)/2
    w=np.sqrt(n*(n-1)*((2.*n)+5.)/18.)

    rank_upper=((dof+1.96*w)/2.)+1
    rank_lower=((dof-1.96*w)/2.)+1

    if rank_upper >= len(slopes): rank_upper=len(slopes)-1
    if rank_upper < 0: rank_upper=0
    if rank_lower < 0: rank_lower=0

    upper=slopes[int(rank_upper)]
    lower=slopes[int(rank_lower)]

    if mult10:
        return 10. * mpw, 10. * lower, 10. * upper, y_intercept_point      # MedianPairwiseSlopes
    else:
        return  mpw, lower, upper, y_intercept_point      # MedianPairwiseSlopes



OUTPATH = '/scratch/vportge/plots/GHCNDEX/'





##############
#load in data#
##############

indexname='TXx' #Decide which index should be used:
CHOOSE_YEAR=2015
filepath='/project/hadobs2/hadex3/ghcndex/GHCND_'+indexname+'_1951-2018_RegularGrid_global_2.5x2.5deg_LSmask.nc'
time_constraint = iris.Constraint(time=lambda c: 20160101 > c.point > 19910100)
longitude_constraint = iris.Constraint(longitude=lambda c: 0<=c.point<=60 or 360.>=c.point>=342)
latitude_constraint = iris.Constraint(latitude=lambda c: 22< c.point<60) 

data=iris.load(filepath, time_constraint) #Data has name of the months. 
data = data.extract(longitude_constraint)
data = data.extract(latitude_constraint)



data_values=data[0].data
LONS = data[0].coord('longitude').points
LATS = data[0].coord('latitude').points

years=np.arange(1991,2016)    
year=data[0].data[0,:,:]

##########################################
#compute the global average for some year#
##########################################
global_mean=data[0].collapsed('latitude', iris.analysis.MEAN)
global_mean=global_mean.collapsed('longitude', iris.analysis.MEAN)

######################################################
#Plot the data: Time Series and map of global average#
######################################################
plot_years(years, global_mean.data)
plot_map(data_values[CHOOSE_YEAR-1991, :, :], LONS, LATS)



#########################################
#Plot years 1991 - 2010 with trend line #
#########################################

time_coord = global_mean.coord('time')
times_datetime = []

for i in range(len(time_coord.points)):
    yyyy = datetime.datetime.strptime(str(int(time_coord.points[i]))[0]
    if global_mean.name() == 'NOV':
        mm == '11'
    times_datetime.append(datetime.datetime.strptime(str(int(time_coord.points[i])), '%Y%m%d'))

times_nums_units = netCDF4.date2num(times_datetime, units = 'days since 1970-01-01 00:00', calendar = 'standard')
time_unit = cf_units.Unit( 'days since 1970-01-01 00:00', calendar='standard')
new_timecoord = iris.coords.DimCoord(times_nums_units, standard_name = 'time', units = time_unit, var_name = "time") 
global_mean.remove_coord('time')
global_mean.add_dim_coord(new_timecoord,0)


plt.close()
YDATA = global_mean.data
XDATA = new_timecoord.points
MDI  = YDATA.mask

trendanalysis = MedianPairwiseSlopes(XDATA,YDATA,MDI,mult10 = False, sort = False, calc_with_mdi=True)

slope = trendanalysis[0]
slope_lower_uncrty = trendanalysis[1]
slope_upper_uncrty = trendanalysis[2]
#Y_INTERCEPTION = np.median(YDATA)-slope*np.median(XDATA)
Y_INTERCEPTION = trendanalysis[3]

trendcube = copy.deepcopy(global_mean)
trendcube.rename('Trend')
trendcube.data=line(XDATA, Y_INTERCEPTION, slope)
'''
trendcube_upper = copy.deepcopy(data_time_period)
trendcube_upper.rename('Upper Trend')
trendcube_upper.data=line(XDATA, Y_INTERCEPTION, slope_upper_uncrty)

trendcube_lower = copy.deepcopy(data_time_period)
trendcube_lower.rename('Upper Trend')
trendcube_lower.data=line(XDATA, Y_INTERCEPTION, slope_lower_uncrty)       
'''

plt.close()
fig=plt.figure(figsize = (10, 8))
iplt.plot(global_mean)
plt.grid()
plt.title(indexname + ' GHCNDEX', size=22)
#plt.ylabel(UNITS_DICT[INAME], size=20)
plt.xlabel('years', size=20)

iplt.plot(trendcube, label='trend: '+str(round(slope*365*10.,2))+' per decade')
#iplt.plot(trendcube_lower, label='lower trend: '+str(round(slope*365*10.,2))+' '+UNITS_DICT[INAME]+' per decade')
#iplt.plot(trendcube_upper, label='upper trend: '+str(round(slope*365*10.,2))+' '+UNITS_DICT[INAME]+' per decade')

plt.legend(fontsize = 16)
plt.tight_layout()
plt.tick_params(axis='both', which='major', labelsize=16)

#plt.xlim( 728294. - 5*365, 735599.)

plt.savefig(OUTPATH+indexname+'_GHCNDEX_with_trend.png')













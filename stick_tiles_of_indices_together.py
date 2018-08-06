import numpy as np
import iris
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import iris.quickplot as qplt
#import matplotlib.cm as mpl_cm
#import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import glob
#from iris.util import unify_time_units
import datetime
import numpy.ma as ma
import sys
#import requests
import netCDF4
import iris.plot as iplt
#from median_pairwise_slopes import MedianPairwiseSlopes
import copy
import iris.coord_categorisation

def plot_years(y, indexname):

    if TIMERANGE == 'ANN':
        title_time = 'annually'
    elif TIMERANGE == 'MON':
        title_time = 'monthly'
    elif TIMERANGE == 'DAY':
        title_time = 'daily'

    plt.close()
    fig=plt.figure()
    iplt.plot(y)
    plt.grid()
    plt.title(indexname+' ('+title_time+')', size=22)
    plt.ylabel(UNITS_DICT[INAME], size=20)
    plt.xlabel('years', size=20)
    plt.tick_params(axis='both', which='major', labelsize=16)

    #plt.show()
    #iplt.plot(trendcube)
    plt.savefig(OUTPATH+indexname+'_'+TIMERANGE+'_'+REGION+'.png')


def plot_figure(data, gridlons, gridlats, title):
    """Plot map of index for some day."""
    plt.close()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    lst_map = plt.pcolormesh(gridlons, gridlats, data, transform=ccrs.PlateCarree(), cmap = 'RdBu_r')
    cbar = plt.colorbar(lst_map, orientation='horizontal', extend='both')
    ax.set_extent((np.amin(gridlons)-2, np.amax(gridlons)+2, np.amin(gridlats)-2, np.amax(gridlats)+2), crs = ccrs.PlateCarree())

    political_bdrys = cfeat.NaturalEarthFeature(category='cultural',
                                                name='admin_0_countries',
                                                scale='50m')
    ax.add_feature(political_bdrys,
                edgecolor='b', facecolor='none', zorder=2)
    gl = ax.gridlines(draw_labels=True)
    plt.title(title, y=1.08, size=22)
    cbar.set_label(UNITS_DICT[INAME]+' per decade', size=20)
    #plt.tight_layout()
    #plt.show()

    plt.savefig(OUTPATH+INAME+'_map_of_trend_'+TIMERANGE+'_'+REGION+'.png')
    return

def line(x,t,m):
    return m*x+t


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

    mpw=np.ma.median(np.ma.array(slopes))
    y_intercept_point = np.ma.median(np.array(y_intercepts))

    # copied from median_pairwise.pro methodology (Mark McCarthy)
    slopes.sort()

    if calc_with_mdi == True:
        good_data = np.where(mdi == False)#good_data=np.where(ydata == False)[0]
        n=len(ydata[good_data])

    elif calc_with_mdi == False:
        n=len(ydata)

    try:

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

    except:
        if mult10:
            return 10. * mpw, 'test', 'test', y_intercept_point      # MedianPairwiseSlopes
        else:
            return  mpw, 'test', 'test', y_intercept_point      # MedianPairwiseSlopes




MIN_OR_MAX = 'max'
YEARS = np.arange(1991, 2016)
MONTHS = ["%.2d" % i for i in range(1,13)]
try:
    TILENUM = int(sys.argv[1]) #has format: '1'
except:
    TILENUM = 7

INDIR = '/scratch/vportge/indices/python_created_indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+str(TILENUM)+'/'

'''
UNITS_DICT = {'CSDI': 'days', 'DTR': u'\u00B0C', 'FD': 'days', 'ID': 'days', 'SU': 'days', 'TN10P': '%', 'tn90p': '%',
              'TNLT2': 'days', 'TNLTM2': 'days', 'TNLTM20': 'days', 'TNm': u'\u00B0C', 'TNn': u'\u00B0C', 'TNx': u'\u00B0C',
              'TR': 'days', 'TX10P': '%', 'TX90P': '%', 'TX95T': u'\u00B0C', 'TXGE30': 'days', 'TXGE35': 'days', 'TXGT50P': '%',
              'TXn': u'\u00B0C', 'TXx': u'\u00B0C', 'WSDI': 'days'}
'''

UNITS_DICT = {'CSDI': 'days', 'DTR': u'\u00B0C', 'FD': 'days', 'ID': 'days', 'SU': 'days', 'TN10p': '%', 'TN90p': '%',
              'TNm': u'\u00B0C', 'TNn': u'\u00B0C', 'TNx': u'\u00B0C', 
              'TR': 'days', 'TX10p': '%', 'TX90p': '%', 'TXn': u'\u00B0C', 'TXx': u'\u00B0C', 'WSDI': 'days' }


python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']


not_working = []
slopes = []
REGIONS = {'SPAIN': [-7.5, 37.5, 0.0, 42.5], 'GERMANY': [5.0, 47.5, 15.0, 52.5], 'MOROCCO': [-5.0, 30.0, 5.0, 35.0]}  #westerly longitude, southerly latitude, easterly longitude, northerly latitude


for INAME in python_indices:
    print(INAME)

    if INAME == 'WSDI' or INAME == 'CSDI' or INAME == 'HW': #those are annual indices.
        possible_times = ['ANN']
    elif INAME == 'TX95T':
        possible_times = ['DAY']

    else:
        possible_times = ['MON', 'ANN']

    for REGION in REGIONS:
        print(REGION)

        left_lon = float(REGIONS[REGION][0])
        right_lon = float(REGIONS[REGION][2])
        lower_lat = float(REGIONS[REGION][1])
        upper_lat = float(REGIONS[REGION][3])

        lat_constraint = iris.Constraint(latitude=lambda c: lower_lat <= c.point <= upper_lat)
        lon_constraint = iris.Constraint(longitude=lambda c: left_lon <= c.point <= right_lon)


        FPATH = glob.glob('/scratch/vportge/indices/python_created_indices/'+MIN_OR_MAX+'_LST_in_cold_window/*/'+INAME+'*.nc')
        OUTPATH = '/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'


        data = iris.load(FPATH)
        #concatenate data so that all tiles are sticked together!
        data = data.concatenate_cube()

        data = data.extract(lat_constraint)
        data = data.extract(lon_constraint)

        data.coord('latitude').guess_bounds()
        data.coord('longitude').guess_bounds()

        cube_name = data.name()
        if UNITS_DICT[INAME] != '%' and UNITS_DICT[INAME] != 'days':
            if INAME != 'DTR':
                data = data - 273.15
                data.rename(cube_name)

        ###############################################################################
        #Add a new time coordinate ('year') so that an annual average can be computed.#
        ###############################################################################
        iris.coord_categorisation.add_year(data, 'time', name='year')
        ann_data = data.aggregated_by('year', iris.analysis.MEAN)
        ann_data.rename(cube_name[:-3]+'ANN' )

        for TIMERANGE in possible_times:
            if TIMERANGE == 'ANN':
                TITLE_TIME = 'annually'
                analyse_data = ann_data

            elif TIMERANGE == 'MON':
                TITLE_TIME = 'monthly'
                analyse_data = data

            elif TIMERANGE == 'DAY':
                TITLE_TIME = 'daily'
                analyse_data = data

            #####################################################################################
            #Plot a time series of spatially averaged values weighted by the area of the gridbox#
            #First: Do spatial average, then: Compute the trend #
            #####################################################################################

            print('calculate weights')
            global_mean_areas = iris.analysis.cartography.area_weights(analyse_data)
            print('calculate spatial average')
            global_mean=analyse_data.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=global_mean_areas)


            YDATA = global_mean.data
            XDATA = global_mean.coord('time').points
            MDI  = YDATA.mask

            #Compute trend with MedianPairwisesSlopes
            trendanalysis = MedianPairwiseSlopes(XDATA,YDATA,MDI,mult10 = False, sort = False, calc_with_mdi=True)

            slope = trendanalysis[0]
            slope_lower_uncrty = trendanalysis[1]
            slope_upper_uncrty = trendanalysis[2]
            #Y_INTERCEPTION = np.median(YDATA)-slope*np.median(XDATA)
            Y_INTERCEPTION = trendanalysis[3]
            slopes.append(slope)

            trendcube = copy.deepcopy(global_mean)
            trendcube.rename('Trend')
            trendcube.data=line(XDATA, Y_INTERCEPTION, slope)
            '''
            trendcube_upper = copy.deepcopy(global_mean)
            trendcube_upper.rename('Upper Trend')
            trendcube_upper.data=line(XDATA, Y_INTERCEPTION, slope_upper_uncrty)

            trendcube_lower = copy.deepcopy(global_mean)
            trendcube_lower.rename('Upper Trend')
            trendcube_lower.data=line(XDATA, Y_INTERCEPTION, slope_lower_uncrty)       
            '''
            #Begin plot#

            plt.close()
            fig=plt.figure(figsize = (10, 8))
            iplt.plot(global_mean)
            plt.grid()
            plt.title(INAME+' CM SAF '+' ('+TITLE_TIME+')', size=22)
            plt.ylabel(UNITS_DICT[INAME], size=20)
            plt.xlabel('years', size=20)

            iplt.plot(trendcube, label='trend: '+str(round(slope*365*10.*24.,2))+' '+UNITS_DICT[INAME]+' per decade ' + REGION)
            #iplt.plot(trendcube_lower, label='lower trend: '+str(round(slope*365*10.,2))+' '+UNITS_DICT[INAME]+' per decade')
            #iplt.plot(trendcube_upper, label='upper trend: '+str(round(slope*365*10.,2))+' '+UNITS_DICT[INAME]+' per decade')

            plt.legend(fontsize = 16)
            plt.tight_layout()
            plt.tick_params(axis='both', which='major', labelsize=16)

            #plt.xlim( 728294. - 5*365, 735599.)
            plt.savefig(OUTPATH+INAME+'_with_trend_'+TIMERANGE+'_'+REGION+'.png')


            ####################################################
            #Plot map of calculated trends for every gridpoint #
            ####################################################
            if TIMERANGE == 'ANN':
                index_values = ann_data.data
                trends = np.zeros(index_values.shape[1:3]) # lat, lon
                XDATA_ANN = ann_data.coord('time').points #in hours!
                for lat in range(trends.shape[0]):
                    for lon in range(trends.shape[1]):
                        YDATA_GRIDPOINT = index_values[:, lat, lon]
                        trends[lat,lon] = MedianPairwiseSlopes(XDATA_ANN,YDATA_GRIDPOINT,10,mult10 = False, sort = False, calc_with_mdi = False)[0]*365*10.*24.

                GRIDLONS = ann_data.coord('longitude').points
                GRIDLATS = ann_data.coord('latitude').points

                trends = np.ma.masked_where(np.isnan(trends), trends)
                plot_figure(trends, GRIDLONS, GRIDLATS, 'Trend of '+ INAME+' CM SAF '+' ('+TITLE_TIME+')')

                    #except:
                        #not_working.append(INAME)
print(not_working)




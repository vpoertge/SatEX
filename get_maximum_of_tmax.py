import numpy as np
import iris
import matplotlib.pyplot as plt
import iris.quickplot as qplt
#import matplotlib.cm as mpl_cm
#import iris.plot as iplt
import cartopy.crs as ccrs
#import cartopy.feature as cfeature
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

def do_statistics_on_cube(cube, statistics, axis):
    ''' Calculate the max/min/mean of a cube over a defined axis.'''

    if statistics == 'max':
        stat = iris.analysis.max
    elif statistics == 'min':
        stat = iris.analysis.min
    if statistics == 'mean':
        stat = iris.analysis.mean
    return cube.collapsed(axis, stat)


def count_number_of_days_below_over_threshold():
    return 0


MIN_OR_MAX = 'max'


YEARS = np.arange(1991, 2016)
#INDIR = '/scratch/vportge/CM_SAF_LST_MIN_MAX/'
INDIR = '/scratch/vportge/CM_SAF_LST_MIN_MAX/'

MONTHS = ["%.2d" % i for i in range(1,13)]
'''
MONTHLY_AVERAGED = []
MONTHLY_AVERAGED_DATA = []

ANNUAL_AVERAGED = []
ANNUAL_AVERAGED_DATA = []

MONTHLY_AVERAGE = iris.cube.CubeList()
ANNUAL_AVERAGE = iris.cube.CubeList()
'''

TXx_MON_SPAT_AVG = iris.cube.CubeList()
TNx_MON_SPAT_AVG = iris.cube.CubeList()
TXn_MON_SPAT_AVG = iris.cube.CubeList()
TNn_MON_SPAT_AVG = iris.cube.CubeList()

TXx_MON = iris.cube.CubeList()
TNx_MON = iris.cube.CubeList()
TXn_MON = iris.cube.CubeList()
TNn_MON = iris.cube.CubeList()

try:
    TILENUM = int(sys.argv[1]) #has format: '1'
except:
    TILENUM = 0

tmax = '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/CORRECT_TILES/7/1991_2015_tmax_tile_7_max_LST_in_cold_window.nc'
tmin = '/scratch/vportge/concatenated_yearly_files/max_LST_in_cold_window/CORRECT_TILES/7/1991_2015_tmin_tile_7_max_LST_in_cold_window.nc'

OUTDIR = '/scratch/vportge/indices/python_created_indices/'+str(TILENUM)+'/'

#load in TX and TN and concatenate 

TX = iris.load(tmax)
TX = TX.concatenate_cube()
TN = iris.load(tmin)
TN = TN.concatenate_cube()

for i in range(len(YEARS)):
    print(YEARS[i])
    year_constraint = iris.Constraint(time=lambda c: c.point.year == int(YEARS[i]))
    #MONTHLY_MAX = np.ma.zeros((12, 856, 2171), fill_value = 1e+20) #25 years, 856 latitude, 2171 longitude

    #initialize different indice
    TXx_MONTHS = iris.cube.CubeList()
    TXn_MONTHS = iris.cube.CubeList()
    TNx_MONTHS = iris.cube.CubeList()
    TNn_MONTHS = iris.cube.CubeList()


    TN_YEAR = TN.extract(year_constraint)
    TX_YEAR = TX.extract(year_constraint)


    for MONTH in MONTHS:
        print(MONTH)
        #it's quicker not to use time_constraint but instead year_constraint and month_constraint. 
        #time_constraint = iris.Constraint(time=lambda c: c.point.year == int(YEARS[i]) and c.point.month == int(MONTH))
        month_constraint = iris.Constraint(time=lambda c: c.point.month == int(MONTH))

        #FPATH = glob.glob(INDIR+str(YEARS[i])+'/'+str(MONTH)+'/*.nc')

        TX_MONTH = TX_YEAR.extract(month_constraint)
        TN_MONTH = TN_YEAR.extract(month_constraint)


        #TX_MONTH = TX.extract(time_constraint)
        #TN_MONTH = TN.extract(time_constraint)

        TXx_MONTHS.append(TX_MONTH.collapsed('time', iris.analysis.MAX))
        TNx_MONTHS.append(TN_MONTH.collapsed('time', iris.analysis.MAX))
        TXn_MONTHS.append(TX_MONTH.collapsed('time', iris.analysis.MIN))
        TNn_MONTHS.append(TN_MONTH.collapsed('time', iris.analysis.MIN))


        '''
        #load in TX (maximum LST) and TN (minimum LST)
        TX = iris.load(FPATH, 'Maximum Land Surface Temperature in Warm Window (PMW)')
        TX = TX.concatenate_cube()

        TN = iris.load(FPATH, 'Minimum Land Surface Temperature in Cold Window (PMW)')
        TN = TN.concatenate_cube()
        '''

        #TXx_MONTHS.append(TX.collapsed('time', iris.analysis.MAX))

        #TX_data = TX.data
        #MONTHLY_MAX[int(MONTH)-1,:,:] = ma.max(TX_data, axis = 0)

    TXx_MONTHS = TXx_MONTHS.merge_cube()
    TNx_MONTHS = TNx_MONTHS.merge_cube()
    TXn_MONTHS = TXn_MONTHS.merge_cube()
    TNn_MONTHS = TNn_MONTHS.merge_cube()



    TXx_MON.append(TXx_MONTHS)
    TNx_MON.append(TNx_MONTHS)
    TXn_MON.append(TXn_MONTHS)
    TNn_MON.append(TNn_MONTHS)

    #Compute the averaged TXx over the whole region
    #TXx_MON_SPAT_AVG.append(TXx_MONTHS.collapsed(('longitude', 'latitude'), iris.analysis.MEAN))
    #TNx_MON_SPAT_AVG.append(TNx_MONTHS.collapsed(('longitude', 'latitude'), iris.analysis.MEAN))
    #TXn_MON_SPAT_AVG.append(TXn_MONTHS.collapsed(('longitude', 'latitude'), iris.analysis.MEAN))
    #TNn_MON_SPAT_AVG.append(TNn_MONTHS.collapsed(('longitude', 'latitude'), iris.analysis.MEAN))

    '''
    #Compute the averaged TXx over the whole region
    MEAN_MONTHLY_MAX = TXx_MONTHS.collapsed(('longitude', 'latitude'), iris.analysis.MEAN)
    #Average the monthly TXx (averaged over whole region) over the time to get an estimate of the Mean
    MEAN_ANNUALLY_MAX = MEAN_MONTHLY_MAX.collapsed('time', iris.analysis.MEAN)

    MONTHLY_AVERAGE.append(MEAN_MONTHLY_MAX)
    ANNUAL_AVERAGE.append(MEAN_ANNUALLY_MAX)
    '''


TXx_MON.rename('TXx MON')
TNx_MON.rename('TNx MON')
TXn_MON.rename('TXn MON')
TNn_MON.rename('TNn MON')


#Save indices to files
iris.save(TXx_MON, OUTDIR+'TXx_MON_'+str(TILENUM)+'.nc', zlib = True)
iris.save(TNx_MON, OUTDIR+'TNx_MON_'+str(TILENUM)+'.nc', zlib = True)
iris.save(TXn_MON, OUTDIR+'TXn_MON_'+str(TILENUM)+'.nc', zlib = True)
iris.save(TNn_MON, OUTDIR+'TNn_MON_'+str(TILENUM)+'.nc', zlib = True)






'''
MONTHLY_AVERAGE = MONTHLY_AVERAGE.concatenate_cube()
ANNUAL_AVERAGE = ANNUAL_AVERAGE.concatenate_cube()

qplt.plot(MONTHLY_AVERAGE)
plt.savefig('MONTHLY.png')

plt.close()
qplt.plot(ANNUAL_AVERAGE)
plt.savefig('ANNUALLY.png')
'''

'''
    MEAN_MONTHLY_MAX = ma.mean(MONTHLY_MAX, axis = (1,2))
    MONTHLY_AVERAGED.append(MEAN_MONTHLY_MAX)
    MONTHLY_AVERAGED_DATA.append(MEAN_MONTHLY_MAX.data)

    MEAN_ANNUAL_MAX = ma.mean(MEAN_MONTHLY_MAX)
    ANNUAL_AVERAGED.append(MEAN_ANNUAL_MAX)
    ANNUAL_AVERAGED_DATA.append(MEAN_ANNUAL_MAX.data)
    '''

'''
MONTHLY_AVERAGED_DATA = np.concatenate(MONTHLY_AVERAGED_DATA).ravel()
ANNUAL_AVERAGED_DATA = np.concatenate(ANNUAL_AVERAGED_DATA).ravel()



fig = plt.figure()
plt.plot(MONTHLY_AVERAGED_DATA)
plt.ylabel('K')
plt.savefig('test_monthly.png')

plt.close()
fig = plt.figure()
plt.plot(ANNUAL_AVERAGED_DATA)
plt.savefig('test_annual.png')

'''













"""
*********************************************************************
 dummy_python.py
*********************************************************************
 PYTHON script
 dummy_python.py
 alexander.loew@mpimet.mpg.de, February 2014
*********************************************************************
 This script is a dummy python script template for
 diagnostics implemented in python

 ensure to define a main() routine in your script as this is
 important for the calling routine interface

*********************************************************************
"""
import inspect
from esmval_lib import ESMValProject
from netCDF4 import Dataset
import numpy as np
import projects
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pylab as plt
import math
from matplotlib import cm

print(projects)

def main(project_info):
   
    E = ESMValProject(project_info)


    config_file = E.get_configfile()
    plotdir = E.get_plot_dir()
    verbosity = E.get_verbosity()
    plot_type = E.get_graphic_format()
    diag_script = E.get_diag_script_name()
    ifile_dict = E.get_raw_inputfile()
    workdir    = E.get_work_dir()

    #print(config_file)
    print(plotdir)
    print(workdir)
    #print(verbosity)
    #print(plot_type)
    #print(diag_script)
    #print(ifile_dict)
    #print(project_info)
      
    print('Hello, here is the dummy routine from the direct python interface!')

    # create instance of a wrapper that allows easy access to data
    #E = ESMValProject(project_info)

    # get filenames of preprocessed climatological mean files
    model_filenames = E.get_clim_model_filenames(variable='thetao', monthly=True)
    diagworkdir = os.path.join(workdir, 'arctic_ocean')
    if not os.path.exists(diagworkdir):
        os.makedirs(diagworkdir)
    
    for mmodel in model_filenames:
        print(mmodel)
        datafile = Dataset(model_filenames[mmodel])
        lon = datafile.variables['lon'][:]
        lat = datafile.variables['lat'][:]
        lev = datafile.variables['lev'][:]
        if lon.ndim == 2:
            lon2d, lat2d = lon, lat
        elif lon.ndim == 1:
            lon2d, lat2d = np.meshgrid(lon, lat)

        lev_limit = lev[lev<=1500].shape[0]+1

        indi, indj = np.where((lon2d>300)   & (lat2d>80))
        indi2, indj2 = np.where((lon2d<100) & (lat2d>80))
        indi3, indj3 = np.where((lon2d>100) & (lon2d<140) & (lat2d>66))

        indexesi = np.hstack((indi, indi2, indi3))
        indexesj = np.hstack((indj, indj2, indj3))

        series_lenght = datafile.variables['thetao'].shape[0]
        #print(lon[indexesi, indexesj])
        #print(lev)
        oce_kpp_euro = np.zeros((lev[0:lev_limit].shape[0], series_lenght))
        for mon in range(series_lenght):
            #print(mon)
            for ind, depth in enumerate(lev[0:lev_limit]):
                level_pp = datafile.variables['thetao'][mon, ind, :, :]
                oce_kpp_euro[ind,mon] = np.nanmean(level_pp[indexesi, indexesj])
        ofilename = os.path.join(diagworkdir, 'arctic_ocean_eurasian_basin_hof_temp_{}'.format(mmodel))
        np.save(ofilename, oce_kpp_euro)
        datafile.close()

        
        #print(lon)
        #print(lat)
    # plotting
    
    diagplotdir = os.path.join(plotdir, 'arctic_ocean')

    if not os.path.exists(diagplotdir):
        os.makedirs(diagplotdir)
    #data = [1,2,3,4,5,6,7,8,8,10,11,12]
    ncols = 2
    nplots = len(model_filenames)
    ncols = float(ncols)
    nrows = math.ceil(nplots/ncols)
    ncols = int(ncols)
    nrows = int(nrows)
    nplot = 1
    plt.figure(figsize=(8*ncols,2*nrows*ncols))
    for mmodel in model_filenames:
        print('Plotting')
        print(mmodel)

        ifilename = os.path.join(diagworkdir, 'arctic_ocean_eurasian_basin_hof_temp_{}.npy'.format(mmodel))
        hofdata = np.load(ifilename)

        datafile = Dataset(model_filenames[mmodel])
        lev = datafile.variables['lev'][:]
        lev_limit = lev[lev<=1500].shape[0]+1
        series_lenght = datafile.variables['thetao'].shape[0]

        months,depth = np.meshgrid(range(series_lenght), lev[0:lev_limit])
        plt.subplot(nrows,ncols,nplot)
        cmap = cm.Spectral_r
        plt.contourf(months, depth, hofdata-273.15, cmap=cmap, 
             levels=np.round(np.linspace(-2,2.3,41),1),
            extend='both')
        plt.yticks(size=15)
        #plt.xlabel("years", size=15)
        plt.ylabel('m', size=15, rotation='horizontal')
        plt.ylim(1500, 0)
        #plt.gca().invert_yaxis()

        cb = plt.colorbar(pad =0.01)
        cb.set_label('$^{\circ}$C', rotation='horizontal', size=15)
        # cb.set_ticks(size=15)
        cb.ax.tick_params(labelsize=15) 
        plt.title(mmodel, size=20)
        nplot=nplot+1
    plt.tight_layout()
    pltoutname = os.path.join(diagplotdir, 'arctic_ocean_eurasian_basin_hof.png')
    plt.savefig(pltoutname, dpi=100)


    print(model_filenames)

    print('Do something here!')
    print('ENDED SUCESSFULLY!!')
    print(dir(E))

    print('')


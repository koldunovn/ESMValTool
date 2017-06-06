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
print(projects)

def main(project_info):
   
    E = ESMValProject(project_info)


    config_file = E.get_configfile()
    plot_dir = E.get_plot_dir()
    verbosity = E.get_verbosity()
    plot_type = E.get_graphic_format()
    diag_script = E.get_diag_script_name()
    ifile_dict = E.get_raw_inputfile()
    #print(config_file)
    #print(plot_dir)
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
    for mmodel in model_filenames:
        print(mmodel)
        datafile = Dataset(model_filenames[mmodel])
        lon = datafile.variables['lon'][:]
        lat = datafile.variables['lat'][:]
        lev = datafile.variables['lev'][:]
        lon2d, lat2d = lon, lat
        
        indi, indj = np.where((lon2d>-60) & (lon2d<100) & (lat2d>80))
        indi2, indj2 = np.where((lon2d>100) & (lon2d<140) & (lat2d>66))

        indexesi = np.hstack((indi, indi2))
        indexesj = np.hstack((indj, indj2))

        #print(lon[indexesi, indexesj])
        print(lev)
        oce_kpp_euro = np.zeros((lev[0:28].shape[0], 24))
        for mon in range(24):
            print(mon)
            for ind, depth in enumerate(lev[0:28]):
                level_pp = datafile.variables['thetao'][mon, ind, :, :]
                oce_kpp_euro[ind,mon] = np.nanmean(level_pp[indexesi, indexesj])

        np.save('oce_with_brine_{}'.format(mmodel), oce_kpp_euro)
        datafile.close()

        
        #print(lon)
        #print(lat)


    print(model_filenames)

    print('Do something here!')
    print('ENDED SUCESSFULLY!!')
    #print(dir(E))

    print('')


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
from netCDF4 import num2date
from collections import OrderedDict
from cdo import Cdo
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
    #mask       = E.get_cf_lmaskfile()
    #print(currProject)
    #print(config_file)
    #print(plotdir)
    #print(workdir)
    #print(verbosity)
    #print(plot_type)
    #print(diag_script)
    #print('ifile\n')
    #print(ifile_dict)
    #print('project_info\n')
    #print(project_info['AUXILIARIES']['FX_files'].fx_files['sftlf_MPI-ESM-LR'].get_fullpath())
    #print(project_info[''])
    #print(mask)
      
    print('Hello, here is the dummy routine from the direct python interface!')
    fix_files = {}
    model_names = []
    for model in project_info['MODELS']:
        currProject = getattr(projects, model.split_entries()[0])()
        model_name = currProject.get_model_name(model)
        model_names.append(model_name)
        fix_files[model_name] = currProject.get_cf_lmaskfile(project_info,model)
    print(fix_files)
    model_names.sort()
    
    diagworkdir = os.path.join(workdir, 'TRR181_valerio')
    if not os.path.exists(diagworkdir):
        os.makedirs(diagworkdir)
    
    currVars = E.get_currVars()
    
    filenames = {}
    for vvar in currVars:
        filenames[vvar] = E.get_clim_model_filenames(variable=vvar, monthly=True)
    
    cdo = Cdo()
    print(model_names)
    for model_name in model_names:
        print(model_name+'\n')
        pr_file  = filenames['pr'][model_name]
        prsn_file = filenames['prsn'][model_name]
        ofile = diagworkdir+'/test.nc'
        cdo.add(input=[pr_file, prsn_file], output=ofile)
        
        print(filenames['pr'][model_name])
        
    #filenames = E.get_clim_model_filenames(variable='pr', monthly=True)
    #model_filenames = OrderedDict(model_filenames)
    #model_filenames = OrderedDict(sorted(model_filenames.items(), key=lambda t: t[0]))
    #print('model filenames\n')
    #print(model_filenames)
    
    
    # create instance of a wrapper that allows easy access to data
    #E = ESMValProject(project_info)

    # get filenames of preprocessed climatological mean files
    #model_filenames = E.get_clim_model_filenames(variable='thetao', monthly=True)
    #diagworkdir = os.path.join(workdir, 'arctic_ocean')

#    print(model_filenames)

    print('Do something here!')
    print('ENDED SUCESSFULLY!!')
    print(dir(E))

    print('')
    
    #return(project_info)
   


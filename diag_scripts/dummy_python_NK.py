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

import projects
print(projects)

def main(project_info):
   
    E = ESMValProject(project_info)


    config_file = E.get_configfile()
    plot_dir = E.get_plot_dir()
    verbosity = E.get_verbosity()
    plot_type = E.get_graphic_format()
    diag_script = E.get_diag_script_name()
    print(config_file)
    print(plot_dir)
    print(verbosity)
    print(plot_type)
    print(diag_script)

      
    print('Hello, here is the dummy routine from the direct python interface!')

    # create instance of a wrapper that allows easy access to data
    #E = ESMValProject(project_info)

    # get filenames of preprocessed climatological mean files
    model_filenames = E.get_clim_model_filenames(variable='ta', monthly=True)
    print(model_filenames)

    print('Do something here!')
    print('ENDED SUCESSFULLY!!')
    print('')


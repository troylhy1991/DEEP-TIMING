import os


# Step 2: create conda env for TIMING2-board

command = 'conda install --yes -c anaconda numpy'
os.system(command)

command = 'conda install --yes -c anaconda pyqt=4.10.4'
os.system(command)

command = 'conda install --yes -c anaconda scikit-learn=0.18.1'
os.system(command)

command = 'conda install --yes -c anaconda scikit-image=0.12.3'
os.system(command)

command = 'conda install --yes -c https://conda.anaconda.org/simpleitk SimpleITK'
os.system(command)

command = 'conda install --yes -c anaconda vtk=6.3.0'
os.system(command)

command = 'conda install --yes -c menpo opencv=2.4.11'
os.system(command)

command = 'conda install --yes -c conda-forge matplotlib=1.5.1'
os.system(command)

command = 'conda install --yes -c conda-forge pims'
os.system(command)

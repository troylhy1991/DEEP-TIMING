import os

# Step 1: install packages for TIMING2-pipeline

command = 'conda install --yes -c anaconda numpy'
os.system(command)

command = 'conda install --yes -c anaconda scikit-image'
os.system(command)

command = 'conda install --yes -c conda-forge tensorflow'
os.system(command)

command = 'conda install --yes -c conda-forge pims'
os.system(command)

command = 'conda install --yes -c conda-forge trackpy'
os.system(command)

command = 'conda install --yes -c anaconda jupyter'
os.system(command)

command = 'conda install --yes -c anaconda scikit-learn '
os.system(command)

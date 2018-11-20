import os

# Step 1: create conda env for DT-pipeline
command = 'conda create --yes --name DT-pipeline python=3.5'
os.system(command)



# Step 2: create conda env for DT-board
command = 'conda create --yes --name DT-board python=2.7'
os.system(command)


# Step 3: create the C:\\DT-temp folder (for windows)
command = 'mkdir C:\\DT-temp'
os.system(command)

# Step 3: create the ~/DT-temp folder (for windows)
command = 'mkdir ~/DT-temp'
os.system(command)

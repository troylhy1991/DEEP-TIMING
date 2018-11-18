import os
from multiprocessing import Pool

def DT_Initializer(DATASET_PATH, BLOCKS, CORES):
    
    os.system('mkdir ' + DATASET_PATH)
    
    os.system('mkdir ' + DATASET_PATH + '/features/')
    
    BLOCK_PATH_LIST = []
    
    for BID in BLOCKS:
        BLOCK_PATH_LIST.append(DATASET_PATH + BID + '/')
        
    pool = Pool(processes=CORES)
    
    pool.map(DT_Init_Block, BLOCK_PATH_LIST)
    
    pool.close()
    
    
def DT_Reset(DATASET_PATH):
    
    os.system('rm -rf ' + DATASET_PATH)
    
def DT_Init_Block(BLOCK_PATH):
    
    os.system('mkdir ' + BLOCK_PATH)
    
    # make images directory
    os.system('mkdir ' + BLOCK_PATH + 'images/')
    os.system('mkdir ' + BLOCK_PATH + 'images/crops_8bit_s/')
    os.system('mkdir ' + BLOCK_PATH + 'images/crops_16bit_s/')
    
    # make labels directory
    os.system('mkdir ' + BLOCK_PATH + 'labels/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/DET/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/DET/FRCNN-Fast/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/DET/FRCNN-Slow/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/DET/SSD/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/DET/GT/')
    
    os.system('mkdir ' + BLOCK_PATH + 'labels/TRACK/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/TRACK/EZ/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/TRACK/SIAMESE/')
    os.system('mkdir ' + BLOCK_PATH + 'labels/TRACK/GT/')
    
    # make meta directory
    os.system('mkdir ' + BLOCK_PATH + 'meta/')
    
    # make temp directory
    os.system('mkdir ' + BLOCK_PATH + 'temp/')
    os.system('mkdir ' + BLOCK_PATH + 'temp/preprocess/')
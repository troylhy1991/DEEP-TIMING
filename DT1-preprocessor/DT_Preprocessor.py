import os
from multiprocessing import Pool

def DT_UNMIX_BLOCK_Worker(Args):
    DT_HOME = Args[0]
    fname_in_domi = Args[1]
    fname_in_leak = Args[2]
    fname_out = Args[3]
    unmix_ratio = Args[4]
    
    command = DT_HOME + 'DT1-preprocessor/unmix ' + fname_in_domi + ' ' + fname_in_leak + ' ' + fname_out + ' ' + str(unmix_ratio)
    os.system(command)

def DT_UNMIX_BLOCK(DT_HOME, RAW_INPUT_PATH, OUTPUT_PATH, DATASET, BLOCK, FRAMES, UMX_Channel, CORES):
    
    Parameter_List = [] # append [DT_HOME, fname_in_domi, fname_in_leak, fname_out, unmix_ratio]
    for UMX in UMX_Channel:
        for t in range(1, FRAMES+1): 
            temp = []
            
            BID = 's' + BLOCK[2:4]
            fname_in_domi = RAW_INPUT_PATH + DATASET + '/' + DATASET + '_' + BID + 't' + str(t).zfill(2) + UMX[1] + '.tif'
            fname_in_leak = RAW_INPUT_PATH + DATASET + '/' + DATASET + '_' + BID + 't' + str(t).zfill(2) + UMX[0] + '.tif'
            fname_out = OUTPUT_PATH + DATASET + '/' + BLOCK + '/temp/preprocess/' + DATASET + '_' + BID + 't' + str(t).zfill(2) + UMX[0] + '.tif'
            unmix_ratio = UMX[2]
            
            temp.append(DT_HOME)
            temp.append(fname_in_domi)
            temp.append(fname_in_leak)
            temp.append(fname_out)
            temp.append(unmix_ratio)
            Parameter_List.append(temp)
            
    pool = Pool(processes =  CORES)
    pool.map(DT_UNMIX_BLOCK_Worker, Parameter_List)
    pool.close()
    
def DT_UNMIX(DT_HOME, RAW_INPUT_PATH, OUTPUT_PATH, DATASET, BLOCKS, FRAMES, UMX_Channel, CORES):
    for BLOCK in BLOCKS:
        print("UNMIXING " + BLOCK + " ......" )
        DT_UNMIX_BLOCK(DT_HOME, RAW_INPUT_PATH, OUTPUT_PATH, DATASET, BLOCK, FRAMES, UMX_Channel, CORES)

        
        
        
def DT_CLIP_ENHANCE_BLOCK_Worker(Args):        
    DT_HOME = Args[0]
    fname_in = Args[1]
    fname_out = Args[2]
    min_pixel_value = str(Args[3])
    max_pixel_value = str(Args[4])
    min_clip_value = str(Args[5])
    max_clip_value = str(Args[6])
    
    exe_name = DT_HOME + 'DT1-preprocessor/clip-rescale' 
    command = [exe_name, fname_in, fname_out, min_pixel_value, max_pixel_value, min_clip_value, max_clip_value]
    command = " ".join(command)
    os.system(command)
        
        
def DT_CLIP_ENHANCE_BLOCK(DEEP_TIMING_HOME, RAW_INPUT_PATH, OUTPUT_PATH, DATASET, BLOCK, FRAMES, ENHANCE_Channel, ENHANCE_Parameter,CORES):
    
    Parameter_List = []
    for ENHANCE in ENHANCE_Channel:
        for t in range(1, FRAMES+1):
            temp = []
            
            BID = 's' + BLOCK[1:4]
            fname_in = RAW_INPUT_PATH + DATASET + '/' + DATASET + '_' + BID + 't' + str(t).zfill(2) + ENHANCE + '.tif'
            fname_out = OUTPUT_PATH + DATASET + '/' + BLOCK + '/temp/preprocess/' + DATASET + '_' + BID + 't' + str(t).zfill(2) + ENHANCE + '.tif'
            if os.path.isfile(fname_out) == True:
                fname_in = fname_out
                
            temp.append(DEEP_TIMING_HOME)
            temp.append(fname_in)
            temp.append(fname_out)
            temp.append(ENHANCE_Parameter[0])
            temp.append(ENHANCE_Parameter[1])
            temp.append(ENHANCE_Parameter[2])
            temp.append(ENHANCE_Parameter[3])
            
            Parameter_List.append(temp)
            
    pool = Pool(processes =  CORES)
    pool.map(DT_CLIP_ENHANCE_BLOCK_Worker, Parameter_List)
    pool.close()
    
def DT_CLIP_ENHANCE(DEEP_TIMING_HOME, RAW_INPUT_PATH, OUTPUT_PATH, DATASET, BLOCKS, FRAMES, ENHANCE_Channel, ENHANCE_Parameter,CORES):
    for BLOCK in BLOCKS:
        print("CLIP ENHANCE " + BLOCK + " ......")
        DT_CLIP_ENHANCE_BLOCK(DEEP_TIMING_HOME,RAW_INPUT_PATH,OUTPUT_PATH,DATASET,BLOCK,FRAMES,ENHANCE_Channel,ENHANCE_Parameter,CORES)
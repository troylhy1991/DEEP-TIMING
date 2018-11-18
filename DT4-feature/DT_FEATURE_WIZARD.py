import os
from multiprocessing import Pool

import numpy as np


import skimage
from skimage import io
from skimage import color
from skimage import measure

from collections import Counter
Size = 6

def DT_FEATURE_EXTRACTOR(OUTPUT_PATH, DATASET, BLOCK, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, PARAMETER, CORES):
    '''
        For Nanowells in each block, create the cell Mask from bbox information.
        
    '''
    
    ### STEP 1: Load Nanowell Available in the BLOCK, make directory
    os.system('mkdir ' + os.path.join(OUTPUT_PATH, DATASET,'features','1_Well_Pool'))
    os.system('mkdir ' + os.path.join(OUTPUT_PATH, DATASET,'features','2_Cell_Pool'))
    
    
    ### STEP 2: Provide BLOCK and NANOWELL index, run NANO_FEATURE_EXTRACTOR()
    BLOCK_ET_LIST = get_BLOCK_ET_count(OUTPUT_PATH, DATASET, BLOCK, DETECTOR_TYPE)
    
    ARG_LIST = []
    for NANO_INFO in BLOCK_ET_LIST:
        NANOWELL = NANO_INFO[0]
        E_NUM = NANO_INFO[1]
        T_NUM = NANO_INFO[2]
        
        temp = [OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, E_NUM, T_NUM]
        ARG_LIST.append(temp)
        generate_cell_pool(temp)
        
    #p = Pool(processes = CORES)
    #p.map(generate_cell_pool, ARG_LIST)
    
    ### STEP 3: Generate the combined feature Table
    # generate_combined_feature_table()
    
    
    
    
def get_BLOCK_ET_count(OUTPUT_PATH, DATASET, BLOCK, DETECTOR_TYPE):
    '''
        returns the selected nanowell in one block
        [[ID1, E#, T#], [ID2, E#, T#], ...]
    '''
    
    BLOCK_ET_COUNT = [] 
    BLOCK_ET_FNAME = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/raw/selected_nanowells.txt'
    
    f = open(BLOCK_ET_FNAME)
    lines = f.readlines()
    f.close()
    
    for line in lines:
        temp = line.rstrip().split('\t')
        ID = int(temp[0])
        E_count = int(temp[1])
        T_count = int(temp[2])
        BLOCK_ET_COUNT.append([ID, E_count, T_count])
        
    return BLOCK_ET_COUNT
    
    
def generate_cell_pool(ARGS):
    OUTPUT_PATH = ARGS[0]
    DATASET = ARGS[1]
    BLOCK = ARGS[2]
    NANOWELL = ARGS[3]
    FRAMES = ARGS[4]
    DETECTOR_TYPE = ARGS[5]
    TRACKER_TYPE = ARGS[6]
    E_NUM = ARGS[7]
    T_NUM = ARGS[8]
    
    # step 1: load image sequences:
    img_frames_CH1, img_frames_CH2, img_frames_CH3 = create_img_frames(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, E_NUM, T_NUM)
    
    # step 2: get the # of E and T %%%This part adopt a lot of the original codes, so there are alias of variables declared here
    E_count = 0
    T_count = 0
    T = FRAMES

    if len(img_frames_CH1) == T:
        for i in range(0, T):
            temp1 = np.amax(img_frames_CH1[i])
            if temp1 > E_count:
                E_count = temp1

    if len(img_frames_CH2) == T:
        for i in range(0, T):
            temp2 = np.amax(img_frames_CH2[i])
            if temp2 > T_count:
                T_count = temp2    

    # step 3: calculate features for E and T candidates
    if E_count>0:
        E_count = int(E_count)
        E_feat = np.ones((E_count, 5, T), dtype=np.float)*(-1000)
        for t in range(0, T):
            # centroid_x, centroid_y, AR, Speed, Death
            regions = skimage.measure.regionprops(img_frames_CH1[t], intensity_image=img_frames_CH3[t])
            for region in regions:
                index = region.label-1
                (centroid_y, centroid_x) = region.centroid
                aspect_ratio = region.minor_axis_length/(region.major_axis_length+1)
                # death_marker = region.mean_intensity
                # death_marker = region.max_intensity
                
                E_feat[index][0][t] = centroid_x
                E_feat[index][1][t] = centroid_y
                E_feat[index][2][t] = aspect_ratio

                death_marker = np.mean(img_frames_CH3[t][int(centroid_y-3):int(centroid_y+3), int(centroid_x-3):int(centroid_x+3)])                
                E_feat[index][4][t] = death_marker
        for index in range(0, E_count):
            for t in range(0, T-1):
                if (E_feat[index][0][t] == -1000 and E_feat[index][1][t] == -1000) or (E_feat[index][0][t+1] == -1000 and E_feat[index][1][t+1] == -1000):
                    pass
                else:
                    temp1 = np.power(E_feat[index][0][t]-E_feat[index][0][t+1],2)
                    temp2 = np.power(E_feat[index][1][t]-E_feat[index][1][t+1],2)
                    E_feat[index][3][t] = np.sqrt(temp1 + temp2)


    if T_count>0:
        T_count = int(T_count)
        T_feat = np.ones((T_count, 6, T), dtype=np.float)*(-1000)
        for t in range(0, T):
            # centroid_x, centroid_y, AR, Speed, Death
            regions = skimage.measure.regionprops(img_frames_CH2[t], intensity_image=img_frames_CH3[t])
            if E_count > 0:
                mask = img_frames_CH1[t] > 0
            for region in regions:
                index = region.label-1
                (centroid_y, centroid_x) = region.centroid
                aspect_ratio = region.minor_axis_length/(region.major_axis_length+1)
                # death_marker = region.mean_intensity
                # death_marker = region.max_intensity
                T_feat[index][0][t] = centroid_x
                T_feat[index][1][t] = centroid_y
                T_feat[index][2][t] = aspect_ratio
                
                death_marker = np.mean(img_frames_CH3[t][int(centroid_y-3):int(centroid_y+3), int(centroid_x-3):int(centroid_x+3)])  
                T_feat[index][4][t] = death_marker
                if E_count > 0:
                    area = region.area
                    T_feat[index][5][t] = float(np.sum(img_frames_CH2[t][mask] == (index+1)))/float(area)


        for index in range(0, T_count):
            for t in range(0, T-1):
                if (T_feat[index][0][t] == -1000 and T_feat[index][1][t] == -1000) or (T_feat[index][0][t+1] == -1000 and T_feat[index][1][t+1] == -1000):
                    pass
                else:
                    temp1 = np.power(T_feat[index][0][t]-T_feat[index][0][t+1],2)
                    temp2 = np.power(T_feat[index][1][t]-T_feat[index][1][t+1],2)
                    T_feat[index][3][t] = np.sqrt(temp1 + temp2)

    # step 4: write the features to disk
    if E_count > 0:
        for i in range(0,E_count):
            fname_prefix = os.path.join(OUTPUT_PATH, DATASET,'features/2_Cell_Pool/')
            fname = BLOCK + 'No' + str(NANOWELL) + 'E' + str(i+1) + '.txt'
            fname = fname_prefix + fname
            write_cell_feature(fname, E_feat[i])

    if T_count > 0:
        for i in range(0, T_count):
            fname_prefix = os.path.join(OUTPUT_PATH, DATASET,'features/2_Cell_Pool/')
            fname = BLOCK + 'No' + str(NANOWELL) + 'T' + str(i+1) + '.txt'
            fname = fname_prefix + fname
            write_cell_feature(fname, T_feat[i])                
    

def create_img_frames(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, E_NUM, T_NUM):
    img_frames_CH1 = np.zeros((FRAMES, 281, 281), dtype=np.uint8)
    img_frames_CH2 = np.zeros((FRAMES, 281, 281), dtype=np.uint8)
    img_frames_CH3 = np.zeros((FRAMES, 281, 281), dtype=np.uint16)

    ### CH1
    if E_NUM > 0:
        #try:
        label_E_sequence = load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'E', E_NUM, DETECTOR_TYPE, TRACKER_TYPE)
        for t in range(FRAMES):
            for N in range(E_NUM):
                x = int(label_E_sequence[t][N][1])
                y = int(label_E_sequence[t][N][2])
                w = int(label_E_sequence[t][N][3])
                h = int(label_E_sequence[t][N][4])
                
                dw = int(0.08*w)
                dh = int(0.08*h)

                if w>4 and h>4:
                    img_frames_CH1[t][y+dh:y+h-dh, x+dw:x+w-dw] = N + 1
        #except:
            #print("CH1 ERROR")
            #pass


    ### CH2
    if T_NUM > 0:
        #try:
        label_T_sequence = load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'T', T_NUM, DETECTOR_TYPE, TRACKER_TYPE)
        for t in range(FRAMES):
            for N in range(T_NUM):
                x = int(label_T_sequence[t][N][1])
                y = int(label_T_sequence[t][N][2])
                w = int(label_T_sequence[t][N][3])
                h = int(label_T_sequence[t][N][4])

                dw = int(0.1*w)
                dh = int(0.1*h)
                
                if w>4 and h>4:
                    img_frames_CH2[t][y+dh:y+h-dh, x+dw:x+w-dw] = N + 1
        #except:
            #print("CH2 ERROR")
            #pass

    ### CH3
    if E_NUM > 0 or T_NUM > 0:
        try:
            for t in range(FRAMES):
                fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/images/crops_16bit_s/' + 'imgNo' + str(NANOWELL) + 'CH3/imgNo' + str(NANOWELL) + 'CH3_t' + str(t+1) + '.tif'
                img_frames_CH3[t] = io.imread(fname)
        except:
            print("CH3 ERROR")
            pass
        
    return img_frames_CH1, img_frames_CH2, img_frames_CH3
        


def load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, cell_type, cell_count, DETECTOR_TYPE, TRACKER_TYPE):

    # load label_E_sequence
    if cell_type == 'E':
        label_E_sequence = []
        E_num = cell_count
        for t in range(1, FRAMES + 1):
            if E_num > 0:
                label_E_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/TRACK/' + TRACKER_TYPE + '/' + DETECTOR_TYPE + '/imgNo' + str(NANOWELL) + '/label_E_t' + str(t).zfill(3) + '.txt'
                f = open(label_E_fname)
                lines = f.readlines()
                f.close()
                temp_E = []
                for line in lines:
                    line = line.rstrip().split('\t')
                    line = [float(kk) for kk in line]
                    temp_E.append(line)
                    label_E_sequence.append(temp_E)

        return label_E_sequence

    if cell_type == 'T':
        label_T_sequence = []
        T_num = cell_count
        for t in range(1, FRAMES + 1):
            if T_num > 0:
                label_T_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/TRACK/' + TRACKER_TYPE + '/' + DETECTOR_TYPE + '/imgNo' + str(NANOWELL) + '/label_T_t' + str(t).zfill(3) + '.txt'
                f = open(label_T_fname)
                lines = f.readlines()
                f.close()
                temp_T = []
                for line in lines:
                    line = line.rstrip().split('\t')
                    line = [float(kk) for kk in line]
                    temp_T.append(line)
                    label_T_sequence.append(temp_T)

        return label_T_sequence        

    

def No2RC(x, size):
    R = int((x-1)/size) + 1
    C = int(x - (R-1)*size)

    return [R,C]    
    

def generate_combined_feat_table(OUTPUT_PATH, DATASET, BLOCKS, FRAMES, DETECTOR_TYPE):
    # read in the cell count of all nanowells in the Block and generate the estimated Effector& Target cell count
    print("ASSEMBLE ALL THE FEATURES......")
    # step 1 create the file Table_Exp.txt
    Dataset_Output_Path = OUTPUT_PATH + DATASET + '/'
    
    T = FRAMES
    Table_Exp = []

    for BID in BLOCKS:
        # step 2 get the nanowell number and cell count
        BLOCK_ET_LIST = get_BLOCK_ET_count(OUTPUT_PATH, DATASET, BID, DETECTOR_TYPE)
        for NANO_INFO in BLOCK_ET_LIST:
            well_ID = NANO_INFO[0]
            E_count = NANO_INFO[1]
            T_count = NANO_INFO[2]
        
            print("BLOCK : " + BID + " NANOWELL: " + str(well_ID) )
            
            l0 = len(Table_Exp)

        # step 3 cell Pool update
            line_counter = 0
            flag_E = 0


            block = int(BID[1:4])
            [R,C] = No2RC(well_ID, 6)
            
            if int(E_count) == 0:
                flag_E = 1
                x=np.ones((5,T),dtype=np.int)*(-1000)
                x_temp = []
                for line in x:
                    line1 = [str(i) for i in line]
                    x_temp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(line1) + '\n')
            if int(E_count) == 1:
                flag_E = 1
                E_fname = Dataset_Output_Path + 'features/2_Cell_Pool/' +BID+'No'+str(well_ID)+'E1.txt'
                try:

                    f_E=open(E_fname,'r')
                    x = f_E.readlines()
                    f_E.close()
                    x_temp = []
                    for line in x:
                        x_temp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + line)
                except:
                    x=np.ones((5,T),dtype=np.int)*(-1000)
                    x_temp = []
                    for line in x:
                        line1 = [str(i) for i in line]
                        x_temp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(line1) + '\n')


            if flag_E == 1 and int(T_count) < 4:
            # if int(T_count) < 4:
                line_counter = line_counter + 6
                marker1 = np.ones((1,T),dtype=np.int)*(-1)
                marker1 = [str(i) for i in marker1[0]]
                x_temp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(marker1) + '\n')
                Table_Exp = Table_Exp + x_temp

                for T_num in range(1,int(T_count)+1):
                    T_fname = Dataset_Output_Path + 'features/2_Cell_Pool/' +BID+'No'+str(well_ID)+'T' + str(T_num) +'.txt'
                    flag_T = 0
                    try:
                        f_T=open(T_fname,'r')
                        y = f_T.readlines()
                        f_T.close()
                        y_temp = []
                        for line in y:
                            y_temp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + line)
                        flag_T = 1
                    except:
                        y=np.ones((6,T),dtype=np.int)*(-1000)
                        y_temp = []
                        for line in y:
                            line1 = [str(i) for i in line]
                            y_temp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(line1) + '\n')
                    if flag_T == 1:
                        line_counter = line_counter + 8
                        Table_Exp = Table_Exp + y_temp[0:5]
                        marker1 = np.ones((1,T),dtype=np.int)*(-1)
                        marker1 = [str(i) for i in marker1[0]]
                        Table_Exp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(marker1) + '\n')
                        Table_Exp = Table_Exp + y_temp[5:6]
                        marker2 = np.ones((1,T),dtype=np.int)*(-2)
                        marker2 = [str(i) for i in marker2[0]]
                        Table_Exp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(marker2) + '\n')

            line_remaining = 49 - line_counter
            for i in range(1, line_remaining):
                marker3 = np.ones((1,T),dtype=np.int)*(-1000)
                marker3 = [str(i) for i in marker3[0]]
                Table_Exp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(marker3) + '\n')

            marker4 = []
            for i in range(1,T+1):
                marker4.append(str(i))
            Table_Exp.append(str(block) + '\t' + str(R) + '\t' + str(C) + '\t' + '\t'.join(marker4) + '\n')

            l1 = len(Table_Exp)
            
            print("ADDING lines: " + str(l1-l0))
            
            
        # step 4 write the useful features to Table_Exp.txt
    fname = Dataset_Output_Path + 'features/Table_Exp.txt'
    f = open(fname, 'w')
    f.writelines(Table_Exp)
    f.close()


def write_cell_feature(fname, feature_array):

    float_formatter = lambda x: "%.2f" % x

    if 'E' in fname.split('/')[-1]:
        f = open(fname,'w')
        for i in range(0,5):
            line = [float_formatter(x) for x in feature_array[i]] # include the BID and No in the first two elements of feature
            line = '\t'.join(line) + '\n'
            f.writelines(line)
        f.close()

    if 'T' in fname.split('/')[-1]:
        f = open(fname,'w')
        for i in range(0,6):
            line = [float_formatter(x) for x in feature_array[i]]
            line = '\t'.join(line) + '\n'
            f.writelines(line)
        f.close()

    
    
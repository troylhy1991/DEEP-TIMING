import pims

import os
import numpy as np

import skimage
from skimage import io
from skimage import color
from skimage import measure

def write_cell_feature(fname, feature_array):
    
    float_formatter = lambda x: "%.2f" % x
    
    if 'E' in fname.split('\\')[-1]:
        f = open(fname,'w')
        for i in range(0,5):
            line = [float_formatter(x) for x in feature_array[i]] # include the BID and No in the first two elements of feature
            line = '\t'.join(line) + '\n'
            f.writelines(line)
        f.close()
        
    if 'T' in fname.split('\\')[-1]:
        f = open(fname,'w')
        for i in range(0,6):
            line = [float_formatter(x) for x in feature_array[i]]
            line = '\t'.join(line) + '\n'
            f.writelines(line)
        f.close()

        
def generate_cell_pool(labels_CH1, labels_CH2, Dataset_Output_Path, BID, Well_ID, T):
    # Given a Block ID and Nanowell ID, generate the cell feature files
    #print("......")
    
    # step 1: load the image sequences
    #img_fnames_CH1 = Dataset_Output_Path + BID + '\\label_img\\imgNo' + str(Well_ID) + 'CH1bg\\imgNo' + str(Well_ID) + 'CH1bg_t*.tif'
    #img_fnames_CH2 = Dataset_Output_Path + BID + '\\label_img\\imgNo' + str(Well_ID) + 'CH2bg\\imgNo' + str(Well_ID) + 'CH2bg_t*.tif'
    img_fnames_CH3 = Dataset_Output_Path + BID + '\\crops_8bit_s\\imgNo' + str(Well_ID) + 'CH3\\imgNo' + str(Well_ID) + 'CH3_t*.tif'
    try:
        img_frames_CH1 = labels_CH1
    except:
        img_frames_CH1 = []
    try:
        img_frames_CH2 = labels_CH2
    except:
        img_frames_CH2 = []
    try:
        img_frames_CH3 = pims.ImageSequence(img_fnames_CH3, process_func = None)
    except:
        img_frames_CH3 = []
    # step 2: get the # of E and T
    E_count = 0
    T_count = 0
    
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
        E_feat = np.ones((E_count, 5, T), dtype=np.float)*(-1000)
        for t in range(0, T):
            # centroid_x, centroid_y, AR, Speed, Death
            regions = skimage.measure.regionprops(img_frames_CH1[t], intensity_image=img_frames_CH3[t])
            for region in regions:
                index = region.label-1
                (centroid_y, centroid_x) = region.centroid
                aspect_ratio = region.minor_axis_length/(region.major_axis_length+1)
                death_marker = region.mean_intensity
                E_feat[index][0][t] = centroid_x
                E_feat[index][1][t] = centroid_y
                E_feat[index][2][t] = aspect_ratio
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
                death_marker = region.mean_intensity
                T_feat[index][0][t] = centroid_x
                T_feat[index][1][t] = centroid_y
                T_feat[index][2][t] = aspect_ratio
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
            fname_prefix = os.path.join(Dataset_Output_Path,'features\\2_Cell_Pool\\')
            fname = BID + 'No' + str(Well_ID) + 'E' + str(i+1) + '.txt'
            fname = fname_prefix + fname
            write_cell_feature(fname, E_feat[i])
        
    if T_count > 0:
        for i in range(0, T_count):
            fname_prefix = os.path.join(Dataset_Output_Path,'features\\2_Cell_Pool\\')
            fname = BID + 'No' + str(Well_ID) + 'T' + str(i+1) + '.txt'
            fname = fname_prefix + fname
            write_cell_feature(fname, T_feat[i])
            
            
from collections import Counter

Size = 6

def No2RC(x, size):
    R = int(x/size) + 1
    C = int(x - (R-1)*size)
    
    return [R,C]

def generate_combined_feat_table(Data_DIR, Dataset_Name, Dataset_Output, Blocks, T):
    # read in the cell count of all nanowells in the Block and generate the estimated Effector& Target cell count
    print("......")
    # step 1 create the file Table_Exp.txt
    Dataset_Output_Path = os.path.join(Data_DIR, Dataset_Name, Dataset_Output) + '/'
    cell_fnames = os.listdir(Dataset_Output_Path + 'features/2_Cell_Pool/')
    
    Table_Exp = []
    
    for BID in Blocks:
        # step 2 get the nanowell number and cell count
        temp_path = Dataset_Output_Path + BID +'/meta/cell_count/'
        nanowell_numbers = int(len(os.listdir(temp_path))/2)
        for well_ID in range(1, nanowell_numbers+1):
            cell_count_fname1 = Dataset_Output_Path+ BID + '/meta/cell_count/' +'imgNo'+ str(well_ID) + 'CH1bg.txt'
            cell_count_fname2 = Dataset_Output_Path+ BID + '/meta/cell_count/' +'imgNo'+ str(well_ID) + 'CH2bg.txt'
            E_count = 0 
            T_count = 0
            
            f1 = open(cell_count_fname1,'r')
            cell_count_list1 = f1.readlines()[0].rstrip('\n').split('\t')
            f1.close()
            
            f2 = open(cell_count_fname2,'r')
            cell_count_list2 = f2.readlines()[0].rstrip('\n').split('\t')
            f2.close()
            
            E_count_temp = Counter(cell_count_list1).most_common(1)
            E_count = E_count_temp[0][0]
            E_count_percent = float(E_count_temp[0][1])/float(T)
            
            T_count_temp = Counter(cell_count_list2).most_common(1)
            T_count = T_count_temp[0][0]
            T_count_percent = float(T_count_temp[0][1])/float(T)
            
            
            if (E_count_percent < 0.8 or T_count_percent < 0.8):
                continue;
            
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
                
    
        # step 4 write the useful features to Table_Exp.txt
    fname = Dataset_Output_Path + 'features/Table_Exp.txt'
    f = open(fname, 'w')
    f.writelines(Table_Exp)
    f.close()
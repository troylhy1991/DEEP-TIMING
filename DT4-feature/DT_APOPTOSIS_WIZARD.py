'''
THIS SCRIPT GENERATES THE APOPTOSIS CLASSIFICATION RESULTS USING PHASE CONTRAST CHANNEL
FUNCTION MODULES INCLUDING:
    (1) GET THE LIST OF NANOWELL ID [BLOCK, NANOWELL, CHANNEL]
    (2) EXTRACT CELL CROP PATCHES AND FORMAT THEM INTO A TENSOR
    (3) APOPTOSIS INFERENCE USING TRAINED CNN-LSTM MODEL
    (4) DECODE THE INFERENCE RESULTS AND WRITE TO FILES
'''
import os
from multiprocessing import Pool

import numpy as np
from skimage import io

from keras.models import model_from_yaml


def DT_APOPTOSIS_DETECTOR(OUTPUT_PATH, DATASET, BLOCKS, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, CORES):
    
    ALL_CROPS_E = []
    ALL_CROPS_T = []
    
    APOPTOSIS_FOLDER = OUTPUT_PATH + DATASET + '/features/3_Apoptosis/'
    os.system('mkdir ' + APOPTOSIS_FOLDER)
    
    for BLOCK in BLOCKS:
        
        print("Loading CROPS from " + BLOCK + " ...... ")
        
        ### STEP 1: GET NANOWELL LIST in the given BLOCK
        SELECTED_NANOWELL_LIST = get_valid_nanowells(OUTPUT_PATH, DATASET, BLOCK, FRAMES, DETECTOR_TYPE, TRACKER_TYPE)
        
        ### STEP 2: EXTRACT CELL CROPS (i) handle missing frames; (ii) separate E and T crops
        CELL_CROP_MOVIES_E, CELL_CROP_MOVIES_T = extract_cell_crops(OUTPUT_PATH, DATASET, SELECTED_NANOWELL_LIST, DETECTOR_TYPE, TRACKER_TYPE)
        
        ALL_CROPS_E.append(CELL_CROP_MOVIES_E)
        ALL_CROPS_T.append(CELL_CROP_MOVIES_T)
        
    ### STEP 3: RUN Cell Crop Inference and write results to folder /features/apoptosis/BxxxE1.txt (0 for live, 1 for dead)
    
    ### FOR the effectors
    MODEL_YAML_PATH = '/uhpc/roysam/hlu8/project/KDD/1_Apoptosis/Ablation/Alex-SB-LSTM-model-E-epoch50.yaml'
    MODEL_WEIGHTS_PATH = '/uhpc/roysam/hlu8/project/KDD/1_Apoptosis/Ablation/Alex-SB-LSTM-weights-E-epoch50.h5'
    apoptosis_inference(MODEL_YAML_PATH, MODEL_WEIGHTS_PATH, ALL_CROPS_E, OUTPUT_PATH, DATASET)
        
    ### FOR the targets
    MODEL_YAML_PATH = '/uhpc/roysam/hlu8/project/KDD/1_Apoptosis/Ablation/Alex-SB-LSTM-model-T-epoch50.yaml'
    MODEL_WEIGHTS_PATH = '/uhpc/roysam/hlu8/project/KDD/1_Apoptosis/Ablation/Alex-SB-LSTM-weights-T-epoch50.h5'
    apoptosis_inference(MODEL_YAML_PATH, MODEL_WEIGHTS_PATH, ALL_CROPS_T, OUTPUT_PATH, DATASET)    
    
    return ALL_CROPS_E, ALL_CROPS_T
    


def get_valid_nanowells(OUTPUT_PATH, DATASET, BLOCK, FRAMES, DETECTOR_TYPE, TRACKER_TYPE):
    '''
    Return the selected nanowell list in the given BLOCK
    [[BLOCK, NANOWELL, FRAMES, E#, T#], ...]
    '''
    selected_nanowell_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/raw/selected_nanowells.txt'
    f = open(selected_nanowell_fname)
    lines = f.readlines()
    f.close()
    
    selected_nanowells = []
    
    for line in lines:
        line = line.rstrip().split('\t')
        line = [int(i) for i in line]
        
        if line[1] > 0 or line[2] > 0:
            temp = [BLOCK, line[0], FRAMES, line[1], line[2]]
            selected_nanowells.append(temp)
    
    return selected_nanowells


def extract_cell_crops(OUTPUT_PATH, DATASET, SELECTED_NANOWELL_LIST, DETECTOR_TYPE, TRACKER_TYPE):
    '''
    Input Args:    
        SELECTED_NANOWELL_LIST = [[BLOCK, NANOWELL, FRAMES, E#, T#], ... , ]
        
    Output Args:
        cell_crop_movie contains two parts
        [[cell_crop_movie, movie_descriptor], ... ,]
            cell_crop_movie: tensor with shape [FRAMES, 51, 51, 1]
            movie_descriptor: [BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_ID]     
            
        Handle missing frame, pass a zero array [1, 51, 51, 1]
    '''
    CELL_CROP_MOVIES_E = []
    CELL_CROP_MOVIES_T = []
    
    for NANOWELL_INFO in SELECTED_NANOWELL_LIST:
        BLOCK = NANOWELL_INFO[0]
        NANOWELL = NANOWELL_INFO[1]
        FRAMES = NANOWELL_INFO[2]
        E_NUM = NANOWELL_INFO[3]
        T_NUM = NANOWELL_INFO[4]
        
        # load crops of Effectors
        if E_NUM > 0:
            label_E_sequence = load_bbox(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'E', E_NUM)
            E_CROPS_TEMP = get_crops(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'E', E_NUM, label_E_sequence)
            for CROP in E_CROPS_TEMP:
                CELL_CROP_MOVIES_E.append(CROP)
                
        # load crops of Targets
        if T_NUM > 0:
            label_T_sequence = load_bbox(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'T', T_NUM)
            T_CROPS_TEMP = get_crops(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'T', T_NUM, label_T_sequence)
            for CROP in T_CROPS_TEMP:
                CELL_CROP_MOVIES_T.append(CROP)                
       
    return CELL_CROP_MOVIES_E, CELL_CROP_MOVIES_T


def load_bbox(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, CELL_TYPE, CELL_NUM):
    '''
    label_sequence[t][cell_ID][feat_ID]  : [ID, x, y, w, h, Class, Score]
    '''
    
    # load label_E_sequence
    if CELL_TYPE == 'E':
        label_E_sequence = []
        E_num = CELL_NUM
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

    if CELL_TYPE == 'T':
        label_T_sequence = []
        T_num = CELL_NUM
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
    

    
def get_crops(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_NUM, label_sequence):
    '''
        load image frames
        parse label_sequence
        for each cell:
            append cell crop images
            generate cell tag
        formate the output
        
        [[cell_crop_movie, movie_descriptor], ... ,]
            cell_crop_movie: tensor with shape [FRAMES, 51, 51, 1]
            movie_descriptor: [BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_ID] 
    '''
    CROPS_TEMP = []
    
    #print(label_sequence)
    
    # STEP 1: Load all CH0 frames
    images_CH0 = get_frames(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES)
    
    # STEP 2: For each cell generate cell_crop_movie and movie_descriptor
    for CELL_ID in range(CELL_NUM):
        cell_crop_movie = np.zeros((FRAMES, 51, 51, 1))
        movie_descriptor = [BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_ID+1]
        for t in range(FRAMES):
            x0 = label_sequence[t][CELL_ID][1]
            y0 = label_sequence[t][CELL_ID][2]
            w = label_sequence[t][CELL_ID][3]
            h = label_sequence[t][CELL_ID][4]
            if w > 5 and h > 5:
                xc = int(x0 + w/2.0)
                yc = int(y0 + h/2.0)
                crop_img = images_CH0[t][yc-25:yc+26, xc-25:xc+26]
                cell_crop_movie[t] = np.reshape(crop_img, (51,51,1))
        temp = [cell_crop_movie, movie_descriptor]
        CROPS_TEMP.append(temp)
    
    return CROPS_TEMP

def get_frames(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES):
    
    output = np.zeros((FRAMES, 281, 281))
    
    for t in range(1, FRAMES+1):
        image_fname = os.path.join(OUTPUT_PATH, DATASET, BLOCK, 'images/crops_8bit_s/') + 'imgNo' + str(NANOWELL) + 'CH0/imgNo' + str(NANOWELL) + 'CH0_t' + str(t) + '.tif'
        
        image = io.imread(image_fname)
        output[t-1] = image
        
    return output



def write_apoptosis_record(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_ID, apoptosis_predict):
    
    fname = OUTPUT_PATH + DATASET + '/features/3_Apoptosis/' + BLOCK + 'No' + str(NANOWELL) + CELL_TYPE + str(CELL_ID) + '.txt'
    f = open(fname, 'w')
    apoptosis_predict = [str(i) for i in apoptosis_predict]
    lines  = '\t'.join(apoptosis_predict) + '\n'
    f.writelines(lines)
    f.close()
    

def apoptosis_inference(MODEL_YAML_PATH, MODEL_WEIGHTS_PATH, ALL_CROPS, OUTPUT_PATH, DATASET):
    '''
        Input: Cell_CROP_MOVIE [[cell_crop_movie, movie_descriptor], ...]
        Output: MOVIE_INFERENCE[[movie_inference_results, movie_descriptor], ... ]
                movie_inference_results: tensor of shape: [FRAMES, 1] 
        Notice: deal with variable length input sequence. if length < 72, padded with last frame; if length > 72, split the sequence
    '''
    
    ### STEP 1: load models
    yaml_file = open(MODEL_YAML_PATH, 'r')
    model_yaml = yaml_file.read()
    yaml_file.close()
    model = model_from_yaml(model_yaml)
    model.load_weights(MODEL_WEIGHTS_PATH)
    
    ### STEP 2: Run Inference
    for BLOCK_CROP in ALL_CROPS:
        ## STEP 2-1: Format Input Sequence
        ## STEP 2-2: Run Inference
        ## STEP 2-3: Format Output Prediction       
        ## STEP 2-4: Write Prediction to File      
        for CROP in BLOCK_CROP:
            movies = CROP[0]
            descriptor = CROP[1]

            # print descriptor

            FRAMES = descriptor[2]
            BLOCK = descriptor[0]
            NANOWELL = descriptor[1]
            CELL_TYPE = descriptor[3]
            CELL_ID = descriptor[4]

            if FRAMES < 72:
                input_frames = np.zeros(72, 51, 51, 1)
                for t in range(72):
                    if t < FRAMES:
                        input_frames[t] = movies[t]
                    else:
                        input_frames[t] = movies[FRAMES-1]

                input_frames = input_frames.reshape(1, 72, 51, 51, 1)        
                y = model.predict(input_frames, verbose=0)
                y = np.argmax(y, axis=2)
                y = list(y[0])

                write_apoptosis_record(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_ID, y)

            if FRAMES == 72:
                input_frames = movies
                input_frames = input_frames.reshape(1, 72, 51, 51, 1) 
                y = model.predict(input_frames, verbose=0)
                y = np.argmax(y, axis=2)
                y = list(y[0])

                write_apoptosis_record(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_ID, y)

            if FRAMES > 72:
                input_frames1 = movies[0:72]
                input_frames2 = movies[-72:72]
                input_frames1.reshape(1, 72, 51, 51, 1)
                input_frames2.reshape(1, 72, 51, 51, 1)
                input_frames1 = input_frames1.reshape(1, 72, 51, 51, 1) 
                input_frames2 = input_frames2.reshape(1, 72, 51, 51, 1) 
                y1 = model.predict(input_frames1, verbose=0)
                y2 = model.predict(input_frames2, verbose=0)
                y1 = np.argmax(y1, axis=2)
                y2 = np.argmax(y2, axis=2)

                y = []
                delta = FRAMES - 72
                for t in range(FRAMES):
                    if t < delta:
                        y.append(y1[t])
                    if t >= delta and t < 72:
                        y.append(y1[t])
                    if t >= 72:
                        y.append(y2[t-FRAMES])
                y = list(y)

                write_apoptosis_record(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_ID, y)
               





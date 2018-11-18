'''
This is the script for generating tracking results for a given movie sequence.
Inputs:
    Movie sequence I(t) and detection results labels
Outputs:
    New labels with index changed
'''
import os
import numpy as np
from itertools import permutations

from skimage import io
from skimage.transform import resize

from keras.models import model_from_yaml

from multiprocessing import Pool

def DT_SIAMESE_TRACKER(OUTPUT_PATH, DATASET, BLOCK, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, CORES):
    patch_a_s_E = []
    tag_a_s_E = []
    patch_b_s_E = []
    tag_b_s_E = []
    delimiter_info_s_E = []



    patch_a_s_T = []
    tag_a_s_T = []
    patch_b_s_T = []
    tag_b_s_T = []
    delimiter_info_s_T = []

    ### Make sure the tracker folder is created
    tracker_folder = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/TRACK/' + TRACKER_TYPE + '/' + DETECTOR_TYPE + '/'
    os.system('mkdir ' + tracker_folder)
    
    ### Step 0: Get the Selected Nanowells and E# & T# Information
    BLOCK_ET_COUNT = get_BLOCK_ET_count(OUTPUT_PATH, DATASET, BLOCK, DETECTOR_TYPE)
    
    
    ### Step 1: Load the Object Detection Results
    SELECTED_NANOWELL_COUNT = len(BLOCK_ET_COUNT)
    SELECTED_NANOWELL_ARGS = []
    
    for NANO in BLOCK_ET_COUNT:
        NANOWELL = NANO[0]
        E_count = NANO[1]
        T_count = NANO[2]
        
        ARGS = [OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, E_count, T_count]
        SELECTED_NANOWELL_ARGS.append(ARGS)
    
    # loading the BLOCK image and feature sequence in parallel
    if SELECTED_NANOWELL_COUNT > 0:
        p = Pool(processes = CORES)
        BLOCK_VOLUME = p.map(load_sequence, SELECTED_NANOWELL_ARGS)
    
    for Nanowell_ID in range(SELECTED_NANOWELL_COUNT):
        
        image_sequence = BLOCK_VOLUME[Nanowell_ID][0]
        label_E_sequence = BLOCK_VOLUME[Nanowell_ID][1]
        label_T_sequence = BLOCK_VOLUME[Nanowell_ID][2]
        NANOWELL = BLOCK_VOLUME[Nanowell_ID][3]
        E_num = BLOCK_VOLUME[Nanowell_ID][4]
        T_num = BLOCK_VOLUME[Nanowell_ID][5]


        if E_num == 1:
            write_tracks(label_E_sequence, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'E')
            

        if T_num == 1:
            write_tracks(label_T_sequence, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'T')

        if E_num > 1:
            patch_a, tag_a, patch_b, tag_b, delimiter_info = format_sequence(image_sequence, label_E_sequence, BLOCK, NANOWELL, FRAMES, E_num, 'E')
            patch_a_s_E.append(patch_a)
            tag_a_s_E.append(tag_a)
            patch_b_s_E.append(patch_b)
            tag_b_s_E.append(tag_b)
            delimiter_info_s_E.append(delimiter_info)



        if T_num > 1:
            patch_a, tag_a, patch_b, tag_b, delimiter_info = format_sequence(image_sequence, label_T_sequence, BLOCK, NANOWELL, FRAMES, T_num, 'T')
            patch_a_s_T.append(patch_a)
            tag_a_s_T.append(tag_a)
            patch_b_s_T.append(patch_b)
            tag_b_s_T.append(tag_b)
            delimiter_info_s_T.append(delimiter_info)

    ### Step 2: Run the SIAMESE Tracker        

    model_path = '/uhpc/roysam/hlu8/project/Cell-Tracking/NEO-Tracker/6_Training/'
    
    if len(patch_a_s_E) > 0:
        PAA_S_E = SIAMESE_Run(model_path, patch_a_s_E, tag_a_s_E, patch_b_s_E, tag_b_s_E, delimiter_info_s_E)
    else:
        PAA_S_E = []

    if len(patch_a_s_T) > 0:
        PAA_S_T = SIAMESE_Run(model_path, patch_a_s_T, tag_a_s_T, patch_b_s_T, tag_b_s_T, delimiter_info_s_T)
    else:
        PAA_S_T = []

    ### Step 3: Parse the PAA_S information and adjust the tracks

    for PAA_E in PAA_S_E:

        PAA = PAA_E[0]
        tag = PAA_E[1]
        
        BLOCK = tag[0]
        NANOWELL = tag[1]
        FRAMES = tag[2]
        N = tag[4]

        PAA = PAA.reshape(FRAMES-1, N, N)

        ASSO = []
        for i in range(FRAMES-1):
            PAA_i = PAA[i]
            ASSO.append(PAS(PAA_i))

        label_E_sequence = load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'E', N, DETECTOR_TYPE)

        label_sequence_new = get_tracks(label_E_sequence, ASSO, FRAMES)

        write_tracks(label_sequence_new, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'E')

    for PAA_T in PAA_S_T:

        PAA = PAA_T[0]
        tag = PAA_T[1]

        BLOCK = tag[0]
        NANOWELL = tag[1]
        FRAMES = tag[2]
        N = tag[4]

        PAA = PAA.reshape(FRAMES-1, N, N)

        ASSO = []
        for i in range(FRAMES-1):
            PAA_i = PAA[i]
            ASSO.append(PAS(PAA_i))

        label_T_sequence = load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'T', N, DETECTOR_TYPE)

        label_sequence_new = get_tracks(label_T_sequence, ASSO, FRAMES)

        write_tracks(label_sequence_new, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'T')
        
        

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
        

def load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, cell_type, cell_count, DETECTOR_TYPE):
    label_E_sequence = []
    label_T_sequence = []
    
    
    # load label_E_sequence
    if cell_type == 'E':
        E_num = cell_count
        for t in range(1, FRAMES + 1):
            if E_num > 0:
                label_E_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/clean/imgNo' + str(NANOWELL) + '/imgNo' + str(NANOWELL) + 'E_t' + str(t) + '.txt'
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
        T_num = cell_count
        for t in range(1, FRAMES + 1):
            if T_num > 0:
                label_T_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/clean/imgNo' + str(NANOWELL) + '/imgNo' + str(NANOWELL) + 'T_t' + str(t) + '.txt'
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
    

def load_sequence(ARGS):
    # Pass Parameters
    OUTPUT_PATH = ARGS[0]
    DATASET = ARGS[1]
    BLOCK = ARGS[2]
    NANOWELL = ARGS[3]
    FRAMES = ARGS[4]
    DETECTOR_TYPE = ARGS[5]
    E_num = ARGS[6]
    T_num = ARGS[7]
    
    image_sequence = np.zeros((FRAMES, 281, 281))
    label_E_sequence = []
    label_T_sequence = [] 
    
    for t in range(1, FRAMES + 1):
        # load image sequence
        img_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/images/crops_8bit_s/imgNo' + str(NANOWELL) + 'CH0/imgNo' + str(NANOWELL) + 'CH0_t' + str(t) + '.tif'
        img = io.imread(img_fname)
        image_sequence[t-1,:,:] = img

        # load label_E_sequence
        if E_num > 0:
            label_E_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/clean/imgNo' + str(NANOWELL) + '/imgNo' + str(NANOWELL) + 'E_t' + str(t) + '.txt'
            f = open(label_E_fname)
            lines = f.readlines()
            f.close()
            temp_E = []
            for line in lines:
                line = line.rstrip().split('\t')
                line = [float(kk) for kk in line]
                temp_E.append(line)
            label_E_sequence.append(temp_E)
        
        # load label_T_sequence
        if T_num > 0:
            label_T_fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/clean/imgNo' + str(NANOWELL) + '/imgNo' + str(NANOWELL) + 'T_t' + str(t) + '.txt'
            f = open(label_T_fname)
            lines = f.readlines()
            f.close()
            temp_T = []
            for line in lines:
                line = line.rstrip().split('\t')
                line = [float(kk) for kk in line]
                temp_T.append(line)
            label_T_sequence.append(temp_T)

    return image_sequence, label_E_sequence, label_T_sequence, NANOWELL, E_num, T_num





def format_sequence(image_sequence, label_E_sequence, BLOCK, NANOWELL, FRAMES, E_num, cell_type):

    # image_sequence, label_E_sequence, label_T_sequence, E_num, T_num = load_sequence(Sequence_DB_path, Seq_ID, frames)

    if E_num > 1:
        E_crops = np.zeros((FRAMES, E_num, 64, 64, 1))
        E_tags = np.zeros((FRAMES, E_num, 6, 1))
        for t in range(FRAMES):
            for label in label_E_sequence[t]:
                index = int(label[0])
                xa = int(label[1])
                ya = int(label[2])
                wa = int(label[3])
                ha = int(label[4])
                class_a = int(label[5])
                score_a = float(label[6])
                
                # in case some empty detection results
                try:
                    patch_a = image_sequence[t,ya:ya+ha,xa:xa+wa]
                    patch_a = resize(patch_a, (64,64))
                except:
                    patch_a = np.zeros((64,64))  
                E_crops[t, index-1, :,:,:] = np.reshape(patch_a, (64, 64, 1))

                vector_a = [xa, ya, wa, ha, class_a, score_a]
                vector_a = [float(kk) for kk in vector_a]
                vector_a = np.array(vector_a)
                E_tags[t, index-1, :, :] = np.reshape(vector_a, (6,1))

        offset = E_num*E_num

        patch_a = np.zeros((offset*(FRAMES-1), 64, 64, 1))
        patch_b = np.zeros((offset*(FRAMES-1), 64, 64, 1))
        tag_a = np.zeros((offset*(FRAMES-1),6,1))
        tag_b = np.zeros((offset*(FRAMES-1),6,1))


        for t in range(FRAMES-1):
            for i in range(E_num):
                for j in range(E_num):
                    patch_a[offset*t + E_num*i + j, :,:,:] = E_crops[t, i, :, :, :]
                    patch_b[offset*t + E_num*i + j, :,:,:] = E_crops[t, j, :, :, :]
                    tag_a[offset*t + E_num*i + j, :, : ] = E_tags[t, i, :, :]
                    tag_b[offset*t + E_num*i + j, :, : ] = E_tags[t, j, :, :]

        BID = BLOCK
        Nano_ID = NANOWELL
        cell_count = E_num
        delimiter_info = [BID, Nano_ID, FRAMES, cell_type, cell_count]

        # print("Sequence " + str(Seq_ID) + " format ready!")

        return patch_a, tag_a, patch_b, tag_b, delimiter_info
    
    
    
    
    
def SIAMESE_Run(model_path, patch_a_s, tag_a_s, patch_b_s, tag_b_s, delimiter_info_s):

    '''
        delimiter_info contains information about: [BID, Nano_ID, frames, cell_type, cell_count]
    '''

    cell_type = delimiter_info_s[0][3]

    PAA_S = []

    if cell_type == 'E':
        # Step 1: load the trained tracker model for Effector

        # load YAML and create model
        yaml_file = open(model_path + 'SIAMESE-E-model-epoch50.yaml', 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        loaded_model = model_from_yaml(loaded_model_yaml)
        # load weights into new model
        loaded_model.load_weights(model_path + "SIAMESE-E-model-weights-epoch50.h5")

        # Step 2: run the inference
        for patch_a, tag_a, patch_b, tag_b, delimiter_info in zip(patch_a_s, tag_a_s, patch_b_s, tag_b_s, delimiter_info_s):
            y = loaded_model.predict([patch_a, tag_a, patch_b, tag_b])
            temp = [y[:,1], delimiter_info]
            PAA_S.append(temp)

        # Step 3: delete model

        del loaded_model

    if cell_type == 'T':
        # Step 1: load the trained tracker model for Targets

        # load YAML and create model
        yaml_file = open(model_path + 'SIAMESE-T-model-epoch50.yaml', 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        loaded_model = model_from_yaml(loaded_model_yaml)
        # load weights into new model
        loaded_model.load_weights(model_path + "SIAMESE-T-model-weights-epoch50.h5")

        # Step 2: run the inference
        for patch_a, tag_a, patch_b, tag_b, delimiter_info in zip(patch_a_s, tag_a_s, patch_b_s, tag_b_s, delimiter_info_s):
            y = loaded_model.predict([patch_a, tag_a, patch_b, tag_b])
            temp = [y[:,1], delimiter_info]
            PAA_S.append(temp)

        # Step 3: delete model

        del loaded_model

    return PAA_S






def PAS(PAA):
    '''
    Generate the track mapping results based on Patch Association Array (PAA)
    Input:  PAA A1  A2  A3
            C1  p11 p12 p13
            C2  p21 p22 p23
            C3  p31 p32 p33
    Output:
        ASSO: [0,2,1]' which means 0-->0, 1-->2, 2-->1
    '''
    n = PAA.shape[0]
    temp = range(n)

    perms = list(permutations(temp))
    scores = []
    for perm in perms:
        score = 0
        for i in range(n):
            score += PAA[i, perm[i]]
        scores.append(score)

    index = np.argmax(scores)

    return np.array(perms[index])




def sort_index(s):
    '''
        Sort a list and return the index
        i.e. [0,2,1] --> [0,2,1]
    '''
    
    return sorted(range(len(s)), key=lambda k: s[k])

def ASSO_ABS(ASSO, init):
    
    ASSO_X = []
    
    ASSO_X.append(init)
    
    for link in ASSO:                 # links         [ ... ]
        latest_idx = ASSO_X[-1]       # updated index [ ... ]
        temp_order = sort_index(latest_idx)
        ASSO_X.append(list(np.array(link)[temp_order]))
    
    return ASSO_X

def get_tracks(label_sequence, ASSO, FRAMES):
    '''
    get_tracks will change the Cell ID and Position of the Cells in the label_sequence
                                    t1             t2           t72
                                c1   c2   c3
    label_sequence will be a [[[ ], [  ], [ ] ], [ ... ], ... ,[ ... ]]
    label_sequence[t1][c1][0:7]
    ASSO[t1] ---> Mapping from t1 to t1 + 1
    '''
    label_sequence_updated = list(label_sequence)
    
    N = len(ASSO[0])
    init = range(N)
    
    ASSO_X = ASSO_ABS(ASSO, init)
    
    for t in range(1, FRAMES):
        for i in range(N):
            try:
                temp = label_sequence[t][ASSO_X[t][i]]
                temp[0] = i + 1
                label_sequence_updated[t][i] = temp
            except:
                pass

    return label_sequence_updated


def write_label(fname, labels):
    w = len(labels)
    f = open(fname,'w')
    for i in range(w):
        temp = labels[i]
        if temp[0] != 0:
            temp = [str(i) for i in temp]
            line = '\t'.join(temp) + '\n'
            f.writelines(line)
    f.close()
    

def write_tracks(label_sequence, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, CELL_TYPE):
    tracker_folder = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/TRACK/'+ TRACKER_TYPE + '/' + DETECTOR_TYPE + '/imgNo' + str(NANOWELL) + '/'    
    try:
        os.system('mkdir ' + tracker_folder)
    except:
        pass
    
    if CELL_TYPE == 'E':
        prefix = 'label_E_t'
    if CELL_TYPE == 'T':
        prefix = 'label_T_t'
    
    for t in range(FRAMES):
        fname = tracker_folder + prefix + str(t+1).zfill(3) + '.txt'
        write_label(fname, label_sequence[t])
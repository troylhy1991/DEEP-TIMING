'''
EZ Tracker Implements a simple cell tracking algorithm as described here:
https://imagej.net/TrackMate_Algorithms#Spot_trackers
'''

from multiprocessing import Pool

from TIMING_BASIC_Tracker import *


def DT_EZ_TRACKER(OUTPUT_PATH, DATASET, BLOCK, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, CORES):
    ### Make sure the tracker folder is created
    tracker_folder = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/TRACK/' + TRACKER_TYPE + '/' + DETECTOR_TYPE + '/'
    os.system('mkdir ' + tracker_folder)
    
    ### Step 0: Get the Selected Nanowells and E# & T# Information
    BLOCK_ET_COUNT = get_BLOCK_ET_count(OUTPUT_PATH, DATASET, BLOCK, DETECTOR_TYPE)
    
    SELECTED_NANOWELL_COUNT = len(BLOCK_ET_COUNT)
    SELECTED_NANOWELL_ARGS = []
    
    for NANO in BLOCK_ET_COUNT:
        NANOWELL = NANO[0]
        E_count = NANO[1]
        T_count = NANO[2]
        
        ARGS = [OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, E_count, T_count]
        SELECTED_NANOWELL_ARGS.append(ARGS)
        #DT_EZ_NANOWELL_TRACKER(ARGS)
    
    # Do Cell Tracking in parallel
    if SELECTED_NANOWELL_COUNT > 0:
        p = Pool(processes = CORES)
        p.map(DT_EZ_NANOWELL_TRACKER, SELECTED_NANOWELL_ARGS)


def DT_EZ_NANOWELL_TRACKER(ARGS):
    
    # Pass the parameters
    OUTPUT_PATH = ARGS[0]
    DATASET = ARGS[1]
    BLOCK = ARGS[2]
    NANOWELL = ARGS[3]
    FRAMES = ARGS[4]
    DETECTOR_TYPE = ARGS[5]
    TRACKER_TYPE = ARGS[6]
    E_count = ARGS[7]
    T_count = ARGS[8]
    
    if E_count == 1:
        label_E_sequence = load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'E', E_count, DETECTOR_TYPE)
        write_tracks(label_E_sequence, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'E')
        
    if T_count == 1:
        label_T_sequence = load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, 'T', T_count, DETECTOR_TYPE)
        write_tracks(label_T_sequence, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, TRACKER_TYPE, 'T')        
        
    if E_count > 1:        
        E_TRACKER = Basic_Tracker(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, 'E', E_count)
        
        E_TRACKER.Run_Tracking()
        
        del E_TRACKER
        
    if T_count > 1:
        T_TRACKER = Basic_Tracker(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, 'T', T_count)
        
        T_TRACKER.Run_Tracking()
        
        del T_TRACKER
    

    
def load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, cell_type, cell_count, DETECTOR_TYPE):

        # load label_E_sequence
        if cell_type == 'E':
            label_E_sequence = []
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
            label_T_sequence = []
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
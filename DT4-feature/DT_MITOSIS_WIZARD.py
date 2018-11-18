'''
THIS MODULE WILL CHECK THE NUMBER OF EFFECTORS AND TARGETS AT FRAME 1,2,3 AND N-2, N-1, N
COMPARE E#(t0) AND E#(tN) OR T#(t0) AND T#(tN)
IF CELL COUNT IS LARGER IN THE END, THERE IS A POSSIBILITY OF CELL DIVISION 
THE IDS OF NANOWELLS CONTAINING POSSIBLE MITOSIS WILL BE KEPT IN features/mitosis.txt
'''

import numpy as np

def load_valid_nanowells(OUTPUT_PATH, DATASET, BLOCK, DETECTOR_TYPE):
    
    NANOWELLS = []
    
    fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/raw/selected_nanowells.txt'
    f = open(fname)
    lines = f.readlines()
    f.close()
    
    for line in lines:
        temp = line.rstrip().split('\t')
        temp = [int(i) for i in temp]
        NANOWELLS.append(temp)
    
    
    return NANOWELLS


def get_cell_count(fname, CELL_TYPE):
    
    if CELL_TYPE == 'E':
        CELL_TYPE_NUM = 1.0
    if CELL_TYPE == 'T':
        CELL_TYPE_NUM = 2.0
    
    f = open(fname)
    lines = f.readlines()
    f.close()
    
    counter = 0
    
    for line in lines:
        temp = line.rstrip().split('\t')
        temp = [float(i) for i in temp]
        if temp[6] > 0.80 and temp[5] == CELL_TYPE_NUM:
            counter += 1
            
    return counter
                


def get_final_number(array):
    x = np.array(array)
    counts = np.bincount(x)
    return np.argmax(counts)
    


def nanowell_mitosis_classifier(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, CELL_TYPE, CELL_COUNT):
    
    if CELL_COUNT == 0:
        return False
    
    CELL_COUNTER0 = []
    CELL_COUNTER1 = []
    
    # STEP-1: check the first three frames
    for t in range(1,4):
        fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/raw/imgNo' + str(NANOWELL) +  '/imgNo' + str(NANOWELL) + '_t' + str(t) + '.txt'
        CELL_COUNTER0.append(get_cell_count(fname, CELL_TYPE))
    
    # STEP-2: check the last three frames
    for t in range(FRAMES-2, FRAMES+1):
        fname = OUTPUT_PATH + DATASET + '/' + BLOCK + '/labels/DET/' + DETECTOR_TYPE + '/raw/imgNo' + str(NANOWELL) +  '/imgNo' + str(NANOWELL) + '_t' + str(t) + '.txt'
        CELL_COUNTER1.append(get_cell_count(fname, CELL_TYPE))    
    
    # STEP-3: compare the cell number, if increased generate TRUE output
    counter0 = get_final_number(CELL_COUNTER0)
    counter1 = get_final_number(CELL_COUNTER1)
    
    if counter0 == counter1:
        return False
    else:
        return True


def write_mitosis_list(fname, MITOSIS_LIST):
    
    f = open(fname, 'w')
    headline = 'BLOCK' + '\t' + 'NANOWELL' + '\t' + 'CELL_TYPE' + '\n'
    f.writelines(headline)
    for line in MITOSIS_LIST:
        line = [str(i) for i in line]
        line = '\t'.join(line) + '\n'
        f.writelines(line)
    f.close()


def DT_MITOSIS_INSPECTOR(OUTPUT_PATH, DATASET, BLOCKS, FRAMES, DETECTOR_TYPE, CELL_TYPE):
    
    MITOSIS_LIST = [] #contains [[BLOCK, NANOWELL, CELL_TYPE]]
    for BLOCK in BLOCKS:
        
        print "Processing " + BLOCK + " ......" 
        
        # STEP-1: Load nanowell list
        NANOWELLS = load_valid_nanowells(OUTPUT_PATH, DATASET, BLOCK, DETECTOR_TYPE)
        
        # STEP-2: nanowell mitosis event checking
        for NANOWELL in NANOWELLS:
            if CELL_TYPE == 'E':
                CELL_COUNT = NANOWELL[1]
            if CELL_TYPE == 'T':
                CELL_COUNT = NANOWELL[2]
            if nanowell_mitosis_classifier(OUTPUT_PATH, DATASET, BLOCK, NANOWELL[0], FRAMES, DETECTOR_TYPE, CELL_TYPE, CELL_COUNT):
                temp = [BLOCK, NANOWELL, CELL_TYPE]
                MITOSIS_LIST.append(temp)
    # STEP-3: save the mitosis nanowells
    fname = OUTPUT_PATH + DATASET + '/features/mitosis_' + CELL_TYPE + '.txt'
    write_mitosis_list(fname, MITOSIS_LIST)
                
        
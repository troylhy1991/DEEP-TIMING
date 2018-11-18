'''
This is the class definition of the basic cell tracker using Karlman filter and LAP
'''

import os
import numpy as np
from itertools import permutations


class Basic_Tracker:
    def __init__(self, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, DETECTOR_TYPE, CELL_TYPE, CELL_COUNT):
        self.OUTPUT_PATH = OUTPUT_PATH
        self.DATASET = DATASET
        self.BLOCK = BLOCK
        self.NANOWELL = NANOWELL
        self.FRAMES = FRAMES
        
        self.CELL_TYPE = CELL_TYPE
        self.CELL_COUNT = CELL_COUNT
        self.DETECTOR_TYPE = DETECTOR_TYPE
        self.TRACKER_TYPE = 'EZ'
        
        self.label_sequence = self.load_bbox_sequence(OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, CELL_TYPE, CELL_COUNT, DETECTOR_TYPE)
        self.output_label_sequence = np.array(self.label_sequence) # Needs to be updated right after each LAP process

        
    def Run_Tracking(self):
        ### Step 1: Run LAP for each time step
        for t in range(self.FRAMES-1):
            self.LAP(t)
        ### Step 2: Write all the tracks to the file 
        self.write_tracks()
        
        
        
    def get_detected_cell_current(self, t, N):
        x0 = self.output_label_sequence[t][N][1]
        y0 = self.output_label_sequence[t][N][2]
        w = self.output_label_sequence[t][N][3]
        h = self.output_label_sequence[t][N][4]
        
        xc = x0 + w/2.0
        yc = y0 + h/2.0
        
        if w<4 or h<4:
            zc = 0
        else:
            zc = 1
        
        return [xc, yc, zc]
    
    def get_detected_cell_next(self, t, N):
        x0 = self.label_sequence[t+1][N][1]
        y0 = self.label_sequence[t+1][N][2]
        w = self.label_sequence[t+1][N][3]
        h = self.label_sequence[t+1][N][4]
        
        xc = x0 + w/2.0
        yc = y0 + h/2.0
        
        if w<4 or h<4:
            zc = 0
        else:
            zc = 1
        
        return [xc, yc, zc]
        
    def get_current_state(self, t):
        state_0 = []
        for N in range(self.CELL_COUNT):
            temp = self.get_detected_cell_current(t, N)
            state_0.append(temp)
        
        return state_0
    
    def get_current_speed(self, t):
        speed_0 = []
        if t == 0:
            for N in range(self.CELL_COUNT):
                temp = [0,0]
                speed_0.append(temp)
            
        if t > 0:   ##### This could result problems
            for N in range(self.CELL_COUNT):
                temp1 = self.get_detected_cell_current(t,N)
                temp0 = self.get_detected_cell_current(t-1,N)
                if temp1[2] > 0 and temp0[2] > 0:
                    vx = temp1[0] - temp0[0]
                    vy = temp1[1] - temp0[1]
                else:
                    vx = 0
                    vy = 0
                speed_0.append([vx, vy])
            
        return speed_0       
                        
        
    def get_next_state(self, t):
        state_1 = []
        for N in range(self.CELL_COUNT):
            temp = self.get_detected_cell_next(t, N)
            state_1.append(temp)
        
        return state_1
    
        
    def predict_next_state(self, t):
        '''
        the simplest prediction of next state is to add the position with speed*decay(0.5)
        '''
        state_0 = self.get_current_state(t)
        speed_0 = self.get_current_speed(t)
        
        state_1_predict = np.array(state_0)
        
        for N in range(self.CELL_COUNT):
            state_1_predict[N][0] += speed_0[N][0]*0.5
            state_1_predict[N][1] += speed_0[N][1]*0.5
            
        return state_1_predict
            
             
    def LAP(self, t):
        '''
        STEP 1: Calculate the LINK COST MATRIX
        STEP 2: PARSE the MATRIX to get the MAPPING Relation
        STEP 3: Update output_label_sequence
        '''
        ### STEP 1: GET PAA
        PAA = np.zeros((self.CELL_COUNT, self.CELL_COUNT))
        
        state_1_predict = self.predict_next_state(t)
        state_1 = self.get_next_state(t)
        
        
        ### trace back and get effective record for each cell
        missing_cells = [1 for i in range(self.CELL_COUNT)]
        t0 = t
        
        for i in range(self.CELL_COUNT):
            if state_1_predict[i][2] > 0:
                missing_cells[i] = 0
        
        while sum(missing_cells) > 0 and t0 > 0:
            t0 = t0 - 1
            state_0_predict = self.predict_next_state(t0)
            
            for i in range(self.CELL_COUNT):
                if state_1_predict[i][2] == 0:
                    if state_0_predict[i][2] > 0:
                        missing_cells[i] =0
                        state_1_predict[i] = state_0_predict[i]
            
        
        ### calculate the cost MATRIX
        for i in range(self.CELL_COUNT):
            for j in range(self.CELL_COUNT):
                if state_1_predict[i][2]>0 and state_1[j][2]>0:
                    dx = state_1_predict[i][0] - state_1[j][0]
                    dy = state_1_predict[i][1] - state_1[j][1]
                    PAA[i][j] = -(dx*dx + dy*dy)
                else:
                    PAA[i][j] = -160000
        
        
        ### STEP 2: PARSE PAA to get ASSO
        ASSO = self.PAS(PAA)
        
        
        ### STEP 3: UPDATE output_label_sequence
        for i in range(self.CELL_COUNT):
            self.output_label_sequence[t+1][i] = self.label_sequence[t+1][ASSO[i]]
            self.output_label_sequence[t+1][i][0] = i+1
        


    def PAS(self, PAA):
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


    def write_label(self, fname, labels):
        w = len(labels)
        f = open(fname,'w')
        for i in range(w):
            temp = labels[i]
            if temp[0] != 0:
                temp = [str(i) for i in temp]
                line = '\t'.join(temp) + '\n'
                f.writelines(line)
        f.close()
    

    def write_tracks(self):
        
        tracker_folder = self.OUTPUT_PATH + self.DATASET + '/' + self.BLOCK + '/labels/TRACK/'+ self.TRACKER_TYPE + '/' + self.DETECTOR_TYPE + '/imgNo' + str(self.NANOWELL) + '/'    
        
        try:
            os.system('mkdir ' + tracker_folder)
        except:
            pass

        if self.CELL_TYPE == 'E':
            prefix = 'label_E_t'
        if self.CELL_TYPE == 'T':
            prefix = 'label_T_t'

        for t in range(self.FRAMES):
            fname = tracker_folder + prefix + str(t+1).zfill(3) + '.txt'
            self.write_label(fname, self.output_label_sequence[t])    
        
        
    
        
        
    def load_bbox_sequence(self, OUTPUT_PATH, DATASET, BLOCK, NANOWELL, FRAMES, cell_type, cell_count, DETECTOR_TYPE):

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
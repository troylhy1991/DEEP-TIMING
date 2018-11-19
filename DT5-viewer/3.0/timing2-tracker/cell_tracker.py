from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import os

import numpy as np
#import pandas as pd
#from pandas import DataFrame, Series  # for convenience

import pims
#import trackpy as tp

import skimage
from skimage import measure, io
import scipy
from scipy import spatial
from skimage.segmentation import join_segmentations

import itertools

class TIMING_Cell_Tracker:
    def __init__(self, frames, t):
        #self.frames = pims.ImageSequence(input_folder, process_func=None)
        self.frames = frames
        self.t = t
        self.track = []   #[[1,2,1,1,1,0,1,.....],[]]
        self.mapping = [] #[['1_1','2_3','3_2'], ..., ...]
        #self.output_folder = output_folder
        (w,h) = self.frames[0].shape
        self.frames_output = np.zeros(shape=(t,w,h), dtype=np.uint8)
        
        self.regions_0 = []
        self.regions_1 = []
        
    def get_distance_cost(self, t0, t1, n0, n1):
        #regions_0 = skimage.measure.regionprops(self.frames[t0], intensity_image=self.frames[t0])
        minr, minc, maxr, maxc = self.regions_0[n0-1].bbox
        centeroid_x_n0 = (minc+maxc)/2
        centeroid_y_n0 = (minr+maxr)/2

        #regions_1 = skimage.measure.regionprops(self.frames[t1], intensity_image=self.frames[t1])
        minr, minc, maxr, maxc = self.regions_1[n1-1].bbox
        centeroid_x_n1 = (minc+maxc)/2
        centeroid_y_n1 = (minr+maxr)/2

        distance = np.sqrt(np.power((centeroid_x_n0-centeroid_x_n1),2) + np.power((centeroid_y_n0-centeroid_y_n1),2))

        return distance


    def get_area_cost(self, t0, t1, n0, n1):
        #regions_0 = skimage.measure.regionprops(self.frames[t0], intensity_image=self.frames[t0])
        area_n0 = self.regions_0[n0-1].area

        #regions_1 = skimage.measure.regionprops(self.frames[t1], intensity_image=self.frames[t1])
        area_n1 = self.regions_1[n1-1].area

        delta_area = abs(area_n0-area_n1)
        return delta_area

    def get_set_distance_cost(self, t0, t1, n0, n1):

        # step1: calculate the overlapping area
        #regions_0 = skimage.measure.regionprops(self.frames[t0], intensity_image=self.frames[t0])
        area_n0 = self.regions_0[n0-1].area

        #regions_1 = skimage.measure.regionprops(self.frames[t1], intensity_image=self.frames[t1])
        area_n1 = self.regions_1[n1-1].area

        mask_t0_n0 = (self.frames[t0] == n0)
        mask_t1_n1 = (self.frames[t1] == n1)
        mask_join = np.logical_or(mask_t0_n0, mask_t1_n1)

        area_join = np.count_nonzero(mask_join)
        area_overlap = area_n1 + area_n0 - area_join

        (w,h) = mask_t0_n0.shape

        if area_overlap > 0:
            return 1 - float(area_overlap)/float(min(area_n0,area_n1))
        else:
            X_t0_n0 = []
            X_t1_n1 = []
            for i in range(0,w):
                for j in range(0,h):
                    if mask_t0_n0[i][j] == True:
                        X_t0_n0.append([i,j])
                    if mask_t1_n1[i][j] == True:
                        X_t1_n1.append([i,j])
            dist = scipy.spatial.distance.cdist(X_t0_n0, X_t1_n1)
            return (np.amin(dist))

        
    def get_death_cost(self, t0, t1, n0, n1):
        print(" ... ")    


    def get_edge_weight(self, t0, t1, n0, n1):
        dist_cost = self.get_distance_cost(t0,t1,n0,n1)
        set_dist_cost = self.get_set_distance_cost(t0,t1,n0,n1)
        area_cost = self.get_area_cost(t0,t1,n0,n1)

        return dist_cost + 10*area_cost + 100*set_dist_cost

    def get_candidate_mapping(self,n0,n1):
        candidate = []
        if n0 <= n1:
            s=""
            for idx in range(1, n1+1):
                s=s+str(idx)
            x = list(itertools.permutations(s,n0))
            for item in x:
                temp=[]
                for i in range(1,n0+1):
                    temp.append(str(i)+'_'+item[i-1])
                candidate.append(temp)
        if n0>n1:
            s=""
            for idx in range(1, n0+1):
                s=s+str(idx)
            x = list(itertools.permutations(s,n1))
            for item in x:
                temp=[]
                for i in range(1,n1+1):
                    temp.append(item[i-1]+'_'+str(i))
                candidate.append(temp)        

        return candidate


    def approx_intprog(self, t0, t1):
        #N0 = self.frames[t0].max()
        #N1 = self.frames[t1].max()
        self.regions_0 = skimage.measure.regionprops(self.frames[t0], intensity_image=self.frames[t0])
        N0 = len(self.regions_0)
        
        self.regions_1 = skimage.measure.regionprops(self.frames[t1], intensity_image=self.frames[t1])
        N1 = len(self.regions_1)
        
        if N0 == 0 or N1 == 0:
            return []
        
        # calculate features
        edges = {}
        for i in range(1,N0+1):
            for j in range(1,N1+1):
                edge = str(i)+'_'+str(j)
                edges[edge] = self.get_edge_weight(t0,t1,i,j)

        # enumerate combinatorics
        candidate = self.get_candidate_mapping(N0,N1)

        # find the min combination
        cost_candidate = []
        for mapping in candidate:
            cost_temp = 0
            for connection in mapping:
                cost_temp += edges[connection]
            cost_candidate.append(cost_temp)



        return candidate[np.argmin(cost_candidate)]



    def get_track(self):
        for i in range(0,self.t-1):
            self.mapping.append(self.approx_intprog(i,i+1))
            #print("Mapping ...")
            
        for i in range(0,self.t-1):
            if i == 0 :
                for link in self.mapping[0]:
                    temp = [int(link[0]), int(link[2])]
                    self.track.append(temp)
            else:
                for link in self.mapping[i]:
                    flag = 0
                    for track in self.track:
                        if int(link[0]) == track[i]:
                            track.append(int(link[2]))
                            flag = 1
                            break
                    if flag == 0:
                        temp = []
                        for k in range(i):
                            temp.append(0)
                        temp.append(int(link[0]))
                        temp.append(int(link[2]))
                        self.track.append(temp)
                for track in self.track:
                    while len(track) < (i + 2):
                        track.append(0) 

    def write_track_img(self):
        index = 1
        for track in self.track:
            counter = 0
            for item in track:
                if item > 0:
                    counter += 1
            if counter > 20:
                for t in range(0,self.t):
                    if track[t] > 0:
                        self.frames_output[t][self.frames[t] == track[t]] = index
                index += 1
        
        return self.frames_output
    
    def calculate_features():
        print(" ... ")
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:16:44 2021

@author: muthu
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:16:44 2021

@author: muthu
"""
# import required modules
import os
import numpy as np
import scipy as sci
from readTrodesExtractedDataFile3 import *
from sys import exit


import spikeinterface
import spikeinterface.extractors as se 
import spikeinterface.toolkit as st
import spikeinterface.sorters as ss
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw
import matplotlib.pylab as plt
#Trying to push to main
#Trying once more
%matplotlib notebook
#%%  
iron_path = "~/Documents/SpikeSorting/ironclust";    
ss.IronClustSorter.set_ironclust_path(os.path.expanduser(iron_path))
ss.IronClustSorter.ironclust_path
#%%
# Setting the number ofdatapoints depending on the length of each recording session
pre_length = 30000*60*60
maze_length = 30000*60*60
post_length = 30000*60*60*4

#%%
# assign directory
path_pre = '/home/samanta/Documents/SpikeSorting/pre'
#path_pre = r'/mnt/data/spikesorting/20201109/pre'

path_maze = r'/mnt/data/spikesorting/20201109/maze'
path_post = r'/mnt/data/spikesorting/20201109/post'

directory_list = [path_pre , path_maze , path_post]


LFP_timeseries_pre = np.array([]) # num_of_channels x LFP data from each channel
LFP_timeseries_maze = np.array([])
LFP_timeseries_post = np.array([])
# iterate over files in that  directory and exclude timestamps file. 
num_channels = 0 

for i in directory_list:
    for filename in os.scandir(i):
        
        if filename.is_file() and (str(filename).find('timestamps') == -1): 
            #num_channels += 1
            #get the LFP data
            LFP_data = readTrodesExtractedDataFile(filename.path)['data'].astype('float64')
            #Vertically stack the LFP timeseries array with LFP data
            #if num_channels == 1:
            if i.find('pre') != -1:    
                LFP_timeseries_pre = np.vstack((LFP_timeseries_pre , LFP_data)) if LFP_timeseries_pre.size else LFP_data
            elif i.find('maze') !=-1:
                LFP_timeseries_maze = np.vstack((LFP_timeseries_maze , LFP_data)) if LFP_timeseries_maze.size else LFP_data
            elif i.find('post') !=-1:
                LFP_timeseries_post = np.vstack((LFP_timeseries_post , LFP_data)) if LFP_timeseries_post.size else LFP_data


#sorter.py should be changed
#%%
num_channels = LFP_timeseries_pre.shape[0]
sampling_frequency = 30000  # in Hz

geom = np.zeros((num_channels, 2))
geom[:, 0] = range(num_channels)

#%%
pre_recording = se.NumpyRecordingExtractor(timeseries=LFP_timeseries_pre[: , 0:pre_length], geom=geom, sampling_frequency=sampling_frequency )
maze_recording = se.NumpyRecordingExtractor(timeseries=LFP_timeseries_maze[: , 0:maze_length], geom=geom, sampling_frequency=sampling_frequency)
post_recording = se.NumpyRecordingExtractor(timeseries=LFP_timeseries_post[: , 0:post_length], geom=geom, sampling_frequency=sampling_frequency)
#%%
recordings_list = [pre_recording , maze_recording, post_recording]


#Merges
multirecording = se.MultiRecordingTimeExtractor(recordings=recordings_list)


#%%
sorting_MS4 = ss.run_mountainsort4(multirecording , output_folder = '/mnt/data/spikesorting')
sorting_TDC = ss.run_tridesclous(multirecording)
sorting_IC = ss.run_ironclust(multirecording)
sorting_HS = ss.run_herdingspikes(multirecording)
sorting_SKC = ss.run_spykingcircus(multirecording)
sorting_KL = ss.run_klusta(multirecording)

sorters_run = [sorting_MS4, sorting_TDC , sorting_IC , sorting_HC , sorting_SKC , sorting_KL]
sorters_run_labels = ['MountainSort4' , 'Tridesclous' , 'IronClust' , 'HerdingSpikes' , 'SpykingCircus' , 'Klusta']
#%%


sortings = []

for epoch in multisorting.get_epoch_names():
    info = multisorting.get_epoch_info(epoch)
    sorting_single = se.SubSortingExtractor(multisorting, start_frame=info['start_frame'], end_frame=info['end_frame'])
    sortings.append(sorting_single)
















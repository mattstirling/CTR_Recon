'''
Created on Dec 2, 2016

@author: mstirling
'''
import glob
import time, ConfigParser

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in folder
in_folder = config.get('filename','parent_folder')

ctr_file_list = [i[len(in_folder + 'riskwatch/' ):] for i in glob.glob(in_folder + 'riskwatch/*.csv')]

for i in ctr_file_list:
    print i
'''
18-Aug-2015
mstirling

for 1 folder, iterate through all files and write records into 1 file

Timing:
Should take <10 seconds

**************************MANUAL STEP**************************
if there are files that break the code, and these files don't have any deal data, then we can remove them from the script
remove from the script by adding the filename to the list, list_filenames_to_skip

'''

#import libraries
import os, time, ConfigParser, glob2

#timing
t1 = time.time()

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in folder
parent_folder = config.get('filename','parent_folder')
yyyymmdd = config.get('filename','yyyymmdd')

#reuse same code for both var and algo riskwatch session
session = ['var','algo'][0]

if session == 'var':

    #in folder + out folder
    in_folder = parent_folder + 'calibration/deals'
    out_folder = parent_folder + 'all/'
    out_file = 'deals.csv'
    out_audit_file = 'deals_audit.csv'
    
elif session == 'algo':
    
    #in folder + out folder
    #parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/Algo Session/dynamic.20160721/'
    in_folder = parent_folder + 'input/UDS'
    out_folder = parent_folder + 'all/'
    out_file = 'deals.csv'
    out_audit_file = 'deals_audit.csv'
    
    list_filenames_to_skip = (['exclude/cpty_excludes.cfg'
                            'exclude/cpty_excludes_imm.cfg'
                            'exclude/credit_rating_exclude.cfg'
                            'exclude/trade_exclusion.csv'])

#make sure we have the folder
try:
    os.stat(out_folder[:-1])
except:
    os.mkdir(out_folder[:-1])

#output files
f_out = open(out_folder + out_file,'w')
f_audit_out = open(out_folder + out_audit_file,'w')

for f in glob2.glob(parent_folder + '**/deals.csv'):
    line_cnt_infile = 1
    this_filepath = f.replace('\\',"/")
    this_file = f[len(parent_folder):].replace('\\',"/")
    print this_file 
    f_in = open(this_filepath,'r')
    for line in f_in:
        f_out.write(line.strip() + '\n')
        f_audit_out.write(this_file + ',' + str(line_cnt_infile) + '\n')
        line_cnt_infile += 1
    f_in.close()
    
#close file          
f_out.close()

#done message
print 'done files from ' + str(in_folder) 
print 'wrote to ' + str(out_folder) + str(out_file)

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' sec'


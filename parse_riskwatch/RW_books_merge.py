'''
18-Aug-2015
mstirling

for 1 folder, iterate through all files and write records into 1 file

Timing:
Should take <10 seconds

'''

#import libraries
import os, time

#timing
t1 = time.time()

#reuse same code for both var and algo riskwatch session
session = ['var','algo'][0]

if session == 'var':

    #in folder + out folder
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.07.21/'
    in_folder_list = ['asia'
                      ,'corr'
                      ,'cva'
                      ,'dpdef'
                      ,'energy'
                      ,'ged'
                      ,'gef'
                      ,'invest_econ_capital'
                      ,'investment'
                      ,'metals'
                      ,'repo'
                      ,'southam'
                      ,'spread'
                      ]
    out_folder = parent_folder + 'all/'
    out_file = 'books.csv'
    
elif session == 'algo':
    
    #in folder + out folder
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/Algo Session/dynamic.20160721/'
    #in_folder = parent_folder + 'input/UDS'
    #out_folder = parent_folder + 'all/'
    #out_file = 'deals.csv'
    
#make sure we have the folder
try:
    os.stat(out_folder[:-1])
except:
    os.mkdir(out_folder[:-1])

#output files
f_out = open(out_folder + out_file,'w')

for in_folder in in_folder_list:
    
    this_folder_path = parent_folder + in_folder
    this_filename = 'books'
    
    #only grab files with the inclusion date
    #if included_date in filename:
    #CTR_filelist.extend(filename)
    #f.write(str(this_dir) + '/' + str(filename) + '\n') # python will convert \n to os.linesep
    this_filepath = this_folder_path + '/' + this_filename 
    line_cnt_infile = 1
    
    f_in = open(this_filepath,'r')
    for line in f_in:
        f_out.write(in_folder)
        f_out.write(',' + line.strip())
        f_out.write('\n')
        line_cnt_infile += 1
    f_in.close()

#close file          
f_out.close()

#done message
print 'done files from ' + str(in_folder) 
print 'wrote to ' + str(out_folder) + str(out_file)

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' sec'


'''
Created on Dec 23, 2016

@author: mstirling
'''

import glob2, mmap, re, os

#in
this_folder = 'C:\Users\mstirling\Desktop\Shared\RW\CTR Files/2017-02-28-PRD/riskwatch_x/'.replace('\\','/')

#out
out_folder = this_folder + 'err_records/'
#out_file = 'out_riskwatch_errors.txt'
#f_out = open(out_folder + out_file,'w')

#create the output folder
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

for f in glob2.glob(this_folder + '**/*.csv'):
    this_filepath = f.replace('\\',"/")
    this_file = f[len(this_folder):]
    print this_file 
    
    #open file, get header
    f_in = open(this_filepath,'r+')
    this_header = f_in.readline()
    
    #get errors
    data = mmap.mmap(f_in.fileno(), 0)
    
    #write header
    err_list = re.findall(r'\n.*Err_.*\n', data) 
    if len(err_list) > 0:
        f_out = open(out_folder + 'err_out_' + this_file,'w') 
        f_out.write('#' + this_file + '\n')
        f_out.write(this_header)
    
    #write errors
    for i in err_list:
        print i.strip()
        f_out.write(i.strip() + '\n')
    
    if len(err_list) > 0:
        f_out.close() 
    
print 'done'
print 'wrote to: ' + out_folder
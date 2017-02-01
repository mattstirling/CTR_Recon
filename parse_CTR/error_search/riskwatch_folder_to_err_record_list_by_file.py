'''
Created on Dec 23, 2016

@author: mstirling
'''

import glob2, mmap, re, os

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def write_riskwatch_errors(f_in_riskwatch,f_out_err):
    data = mmap.mmap(f_in_riskwatch.fileno(), 0)
    for i in re.findall(r'[PC],.*Err_.*\n', data):
        print i.strip()
        f_out.write(i)
    
#in
this_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/RW_ECR_Release_11/CTR_out_files/' 

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
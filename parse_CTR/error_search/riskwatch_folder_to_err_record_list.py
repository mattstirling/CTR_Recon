'''
Created on Dec 23, 2016

@author: mstirling
'''

import glob2, mmap, re

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
this_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/2016-12-30-PRD/riskwatch/' 

#out
out_folder = 'C:/Temp/python/out/'
out_file = 'out_riskwatch_errors.txt'
f_out = open(out_folder + out_file,'w')

for f in glob2.glob(this_folder + '**/*.csv'):
    this_file = f.replace('\\',"/")
    
    print this_file 
    
    #write filename, open file, write header
    f_out.write('#' + this_file + '\n')
    f_in = open(this_file,'r+')
    f_out.write('#' + f_in.readline())
    
    #write errors
    data = mmap.mmap(f_in.fileno(), 0)
    for i in re.findall(r'\n.*Err_.*\n', data):
        print i.strip()
        f_out.write(i.strip() + '\n')
    
print 'done'
print 'wrote to: ' + out_folder + out_file
'''
Created on Jun 9, 2016

@author: mstirling
'''
import time

def line_to_list(line):
    return line.split(',')

#file variables
in_folder = 'C:/Temp/python/in/'
in_file_list = ['deals.csv']
out_folder = 'C:/Temp/python/out/'
out_file = 'out_' + time.strftime("%Y%m%d") + '_all_headers.csv' 

f_out = open(out_folder + out_file,'w')
for in_file in in_file_list:
    with open(in_folder + in_file, 'r') as f_in:
        line_count = 0
        for line in f_in:
            line_count+=1
            b_include_line = 1
            if line[:5] ==',,,,,': b_include_line = 0
            if line[:5] ==',:pos': b_include_line = 0
            if line[:8] ==',Default': b_include_line = 0
            if line[:1] =='#': b_include_line = 0
            if b_include_line: 
                #case: NOT leading comma. we think this is a header
                if not line[:1] ==',':
                    line_split_to_list = line.strip().split(',')
                    this_header_type = line_split_to_list[0] 
                    for header in [header for header in line_split_to_list if not header == '']:
                        f_out.write(in_file)
                        f_out.write(',' + str(line_count))
                        f_out.write(',' + this_header_type)
                        f_out.write(',' + header)
                        f_out.write('\n')
                        
                #case: leading comma. we think this is a record
                #do nothing
                #if line[:1] ==',':
                    
                
f_out.close()

print 'done.'
for filename in in_file_list:
    print 'from ' + in_folder + filename

print 'to ' + out_folder + out_file
  

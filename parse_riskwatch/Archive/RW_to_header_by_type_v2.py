'''
Created on Jun 9, 2016

@author: mstirling
'''
import time, pandas as pd

def line_to_list(line):
    return line.split(',')

def preprocess_flename(name):
    replace_list = [[' ','_'],['*',''],['-',''],['/','']]
    new_name = name
    for item in replace_list:
        new_name = new_name.replace(item[0],item[1])
    return new_name

#time
t1 = time.time()

#file variables
in_folder = 'C:/Temp/python/in/'
in_file_list = ['deals.csv']
out_folder = 'C:/Temp/python/out/RW Files/ByProduct/'
out_file = 'out_' + time.strftime("%Y%m%d") + '_all_headers.csv' 

#set
set_header_type = set()

#list
list_header_type_filename_map = []

#get the header types in this file
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
                    line_split_to_list = line_to_list(line)
                    this_header_type = line_split_to_list[0] 
                    set_header_type.add(this_header_type)
        f_in.close()
        
#for each header type, get the unique list of headers and write to txt files
for header_type in sorted(set_header_type):
    set_headers = set()
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
                        line_split_to_list = line_to_list(line)
                        this_header_type = line_split_to_list[0]
                        if this_header_type == header_type: 
                            for header in [header for header in line_split_to_list if not header.strip() in ['',this_header_type]]:
                                set_headers.add(header)
        f_in.close()
        out_file_name = 'out_' + time.strftime("%Y%m%d") + '_headers_' + preprocess_flename(header_type) + '.txt'
        list_header_type_filename_map.append([header_type,out_file_name])
        
        with open(out_folder + out_file_name, 'w') as f_out:
            f_out.write(header_type)
            for header in sorted(set_headers):
                f_out.write('\n' + header)
            f_out.close()
                             
#write the header-filename to header-type mapping
out_file_name = 'out_' + time.strftime("%Y%m%d") + '_header_type_filename_mapping.csv'
with open(out_folder + out_file_name, 'w') as f_out:
    f_out.write('Header Type, Header Filename')
    for mapping in list_header_type_filename_map:
        f_out.write('\n' + mapping[0] + ',' + mapping[1])
    f_out.close()



















print 'done.'
for filename in in_file_list:
    print 'from ' + in_folder + filename

print 'to ' + out_folder + out_file
  
t2 = time.time()
print 'total run = ' + str(t2-t1) + ' ms'
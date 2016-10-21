'''
Created on Jun 9, 2016

@author: mstirling

update the process to point to 1 single folder as an input
deals will always be in deals.csv

Timing:
VAR Riskwatch Session took 14 minutes to run this for 21-Jul-2016 data

'''
import time, os

def line_to_list(line):
    return line.strip().split(',')

def preprocess_flename(name):
    replace_list = [[' ','_'],['*',''],['-',''],['/',''],[':','']]
    new_name = name
    for item in replace_list:
        new_name = new_name.replace(item[0],item[1])
    return new_name

#time
t1 = time.time()

#control variables
b_write_headers_to_xls = 1

#reuse same code for both var and algo riskwatch session
session = ['var','algo'][0]

if session == 'var':
    #main folder
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.10.19/'

elif session == 'algo':
    #main folder
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/Algo Session/dynamic.20160721/'

#previously we have many child folders in the VAR session. Now we create only 1 session for this data-profiling exercise
list_child_folder = ['all_OC_legacy']

#out folder
out_header_filename = 'out_type_list.txt'

for child_folder in list_child_folder: 
    #file variables
    in_folder = parent_folder + child_folder + '/'
    in_file_list = ['deals.csv']
    out_folder = in_folder + 'ByProduct/'
    
    #make sure we have the folder
    try:
        os.stat(out_folder[:-1])
    except:
        os.mkdir(out_folder[:-1])
    
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
                if line[:5].lower() == ',:pos': b_include_line = 0
                if line[:8].lower() == ',default': b_include_line = 0
                if line[:1] =='#': b_include_line = 0
                if b_include_line: 
                    #case: NOT leading comma. we think this is a header
                    if not line[:1] ==',':
                        line_split_to_list = line_to_list(line)
                        this_header_type = line_split_to_list[0] 
                        set_header_type.add(this_header_type)
                        #print str(this_header_type) + ', ' + str(line_count)
            f_in.close()
    
    #list all of the headers
    with open(out_folder + out_header_filename,'w') as f_header_out:
        for header_type in sorted(set_header_type):
            f_header_out.write(header_type + '\n')
            
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
                    if line[:5].lower() == ',:pos': b_include_line = 0
                    if line[:8].lower() == ',default': b_include_line = 0
                    if line[:1] =='#': b_include_line = 0
                    if b_include_line: 
                        #case: NOT leading comma. we think this is a header
                        if not line[:1] ==',':
                            line_split_to_list = line_to_list(line)
                            this_header_type = line_split_to_list[0]
                            if this_header_type == header_type: 
                                for header in [header for header in line_split_to_list if not str(header).strip() in ['',this_header_type]]:
                                    set_headers.add(header.strip())
            f_in.close()
            out_file_name = 'out_headers_' + preprocess_flename(header_type) + '.txt'
            list_header_type_filename_map.append([header_type,out_file_name])
            
            with open(out_folder + out_file_name, 'w') as f_out:
                f_out.write(header_type)
                for header in sorted(set_headers):
                    f_out.write('\n' + header)
                f_out.close()
                                 
    #write the header-filename to header-type mapping
    out_file_name = 'out_header_type_filename_mapping.csv'
    with open(out_folder + out_file_name, 'w') as f_out:
        f_out.write('Header Type, Header Filename')
        for mapping in list_header_type_filename_map:
            f_out.write('\n' + mapping[0] + ',' + mapping[1])
        f_out.close()


print 'done.'
for filename in in_file_list:
    print 'from ' + parent_folder

print 'to ' + out_folder
  
t2 = time.time()
print 'total run = ' + str(t2-t1) + ' s'
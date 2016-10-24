'''
Created on Jan 13, 2016

@author: mstirling

context: for some records, a vector of values populates within "one cell" and syntax is roughly:
 ,A,B,C,"D1,D2,D3,D4",E,etc....
 *"D1,D2,D3,D4" is the value in one cell

for v3 of this file, we transform ,A,B,C,"D1,D2,D3,D4",E, into ,A,B,C,D1|D2|D3|D4,E,
*we hope this won't cause further mistakes and confusion, but we can't be sure

*further context, we merge multi-row records into 1 record
 ,A,B,C,D1,E,etc....
 ,,,D2,,
 ,,,D3,,
 ,,,D4,,
 
 -->,A,B,C,D1|D2|D3|D4,E,

v5 goal is to only point to a single folder as input

**************************MANUAL STEP**************************
v5 Manual step added:
remove unwanted headers from "map_folder + map_file_name"
ie. parent folder + 'all/ByProduct/out_header_type_filename_mapping.csv'


***took 28 minutes to run on 8-Aug-2016 VAR session

'''
import time, os

def line_to_list(line):
#for v3 of this file, we transform ,A,B,C,"D1,D2,D3,D4",E, into ,A,B,C,D1|D2|D3|D4,E,
#*we hope this won't cause further mistakes and confusion, but we can't be sure 

    if not '"' in line:
        return line.strip().split(',')
    else:
        new_line = ''
        within_vector = False
        for i in line.strip():
            if i == '"':
                within_vector = not(within_vector)
                #don't add anything to the new line
                
            elif within_vector and i == ',':  
                new_line += '|'
            
            else:
                new_line += i
        
        return line_to_list(new_line)

def preprocess_flename(name):
    replace_list = [[' ','_'],['*',''],['-',''],['/','']]
    new_name = name
    for item in replace_list:
        new_name = new_name.replace(item[0],item[1])
    return new_name

#timing
t1 = time.time()

#reuse same code for both var and algo riskwatch session
session = ['var','algo'][0]

if session == 'var':
    #main folder
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.10.11/'

elif session == 'algo':
    #main folder
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/Algo Session/dynamic.20160721/'

list_child_folder = ['all']

for child_folder in list_child_folder: 
    
    #file variables
    in_folder = parent_folder + child_folder + '/'
    in_file_list = ['deals.csv']
    in_file_audit_list = ['deals_audit.csv']
    
    #out folder
    out_folder = in_folder + 'ByProduct/'
    
    #make sure we have the folder
    try:
        os.stat(out_folder[:-1])
    except:
        os.mkdir(out_folder[:-1])
    
    #mapping folder
    map_folder = out_folder
    map_file_name = 'out_header_type_filename_mapping.csv'
    
    #list
    list_header_type_filename_map = []
    
    #get header-type header-filename mappings
    with open(map_folder + map_file_name,'r') as f_in:
        #skip first line (which is a header)
        f_in.readline()
        for line in f_in:
            line_split = line.strip().split(',') 
            list_header_type_filename_map.append([line_split[0],line_split[1]])
    
    #for every header type, get the file of header
    for mapping in list_header_type_filename_map:
        
        this_header_type = mapping[0]
        this_header_filename = mapping[1]
        
        print child_folder + ' + ' + this_header_type
        
        #open file for output 
        this_out_filename = 'out_deals_'  + preprocess_flename(this_header_type) + '.csv'
        f_out = open(out_folder + this_out_filename,'w')
        
        #get the headers
        get_columns = []
        with open(map_folder + this_header_filename,'r') as f_in_headers:
            for line in f_in_headers:
                get_columns.append(line.strip())
    
        #initial variables
        get_columns_header_index = [0 for col in get_columns]
        record_line_split_to_list = []
        this_line_count = 0
        bHeaderTypeInScope = 0
        
        #write the header
        f_out.write('Filename,Row,' + str(','.join([col for col in get_columns])) + '\n')
        
        for i in xrange(len(in_file_list)):
            in_file = in_file_list[i]
            in_file_audit = in_file_audit_list[i]
            #this_out_file_name = in_file.replace('.csv.20160112', '_vect_removed.csv.20160112')
            #this_out_file = open(out_folder + this_out_file_name,'w')
            #print this_out_file_name
            
            #open files
            this_in_file = open(in_folder + in_file, 'r')
            this_in_file_audit = open(in_folder + in_file_audit, 'r') 
            
            #initialize line count
            #remove this in order to get the line count from the original file
            line_count = 0
            
            for line in this_in_file:
                #iterate line count
                line_count+=1
                
                #read from the auditfile
                audit_line = this_in_file_audit.readline()
                
                b_include_line = 1
                #if line[:5] ==',,,,,': b_include_line = 0
                if line[:5].lower() ==',:pos': b_include_line = 0
                if line[:8].lower() ==',default': b_include_line = 0
                if line[:1] =='#': b_include_line = 0
                
                if b_include_line: 
                    #f_out.write(line)
                    [audit_file_in, str_audit_line_count] = audit_line.strip().split(',')
                    
                    #case: NOT leading comma. we think this is a header
                    if not line[:1] ==',':
                        
                        #write previous record before moving onto the new header
                        if len(record_line_split_to_list)>0:
                            f_out.write(audit_file_in)
                            f_out.write(',' + str_audit_line_count)
                            max_len = len(record_line_split_to_list)
                            #write the optional columns
                            for idx in get_columns_header_index:
                                if idx==0 or idx>=max_len:
                                    f_out.write(',')
                                else:
                                    f_out.write(',' + record_line_split_to_list[idx])
                            
                            f_out.write('\n')
                            record_line_split_to_list = []
                        
                        #determine if this header_type is in scope
                        bHeaderTypeInScope = 0
                        get_columns_header_index = []
                        header_line_split_to_list = line_to_list(line)
                        if header_line_split_to_list[0] == this_header_type:
                            bHeaderTypeInScope = 1
                            
                            #get the "index in the header" of every column we're looking for 
                            for col in get_columns:
                                try:
                                    #print line_split_to_list.index(col)
                                    get_columns_header_index.append(int(header_line_split_to_list.index(col)))
                                except:
                                    #don't see this column in the header
                                    get_columns_header_index.append(0)
                    
                    #case: ONLY 1 leading comma. we think this is a record
                    if line[:1] ==',' and not line[:5] ==',,,,,':
                        
                        #only process if this record is associated with an "in-scope" header
                        if bHeaderTypeInScope == 1:
                            #write previous record before moving onto the new one
                            if len(record_line_split_to_list)>0:
                                f_out.write(audit_file_in)
                                f_out.write(',' + str(this_line_count))
                                max_len = len(record_line_split_to_list)
                                
                                #write the optional columns
                                for idx in get_columns_header_index:
                                    if idx==0 or idx >=max_len:
                                        f_out.write(',')
                                    else:
                                        f_out.write(',' + record_line_split_to_list[idx])
                                
                                f_out.write('\n')
                            
                            record_line_split_to_list = line_to_list(line)
                            this_line_count = str_audit_line_count
                    
                    #case: 5 leading commas. we think this is a vector
                    if line[:5] ==',,,,,':
                        
                        #only process if this vector if it is associated with an "in-scope" header
                        #only process if we have a parent record already. ie. drop solo vectors
                        if bHeaderTypeInScope == 1 and len(record_line_split_to_list)>0:
                            
                            vectorline_split_to_list = line_to_list(line)
                            max_len = len(vectorline_split_to_list)
                            
                            for idx in get_columns_header_index:
                                #idx==0 means the column is not in scope - do nothing
                                #blank value means there is no vector in this column - do nothing
                                if idx>0 and idx<max_len:
                                    if not vectorline_split_to_list[idx] == '':
                                        #append this value to the current line
                                        record_line_split_to_list[idx] += '|' + vectorline_split_to_list[idx]  
                        
                            
        #write the final record
        if len(record_line_split_to_list)>0:
            f_out.write(in_file)
            f_out.write(',' + str(this_line_count))
            max_len = len(record_line_split_to_list)
            
            #write the optional columns
            for idx in get_columns_header_index:
                if idx==0 or idx>=max_len:
                    f_out.write(',')
                else:
                    f_out.write(',' + record_line_split_to_list[idx])
        
        f_out.close()

print 'done.'
for filename in in_file_list:
    print 'from ' + in_folder + filename

print 'to ' + out_folder

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' ms'
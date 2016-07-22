'''
Created on Jan 13, 2016

@author: mstirling

context: for some records, a vector of values populates within "one column for on one line" and syntax is roughly:
 ,A,B,C,"D1,D2,D3,D4",E,etc....

for v3 of this file, we transform ,A,B,C,"D1,D2,D3,D4",E, into ,A,B,C,D1|D2|D3|D4,E,
*we hope this won't cause further mistakes and confusion, but we can't be sure 

*further context, we merge multi-row records into 1 record
 ,A,B,C,D1,E,etc....
 ,,,D2,,
 ,,,D3,,
 ,,,D4,,
 
 -->,A,B,C,D1|D2|D3|D4,E,

'''
import time

def line_to_list(line):
#for v3 of this file, we transform ,A,B,C,"D1,D2,D3,D4",E, into ,A,B,C,D1|D2|D3|D4,E,
#*we hope this won't cause further mistakes and confusion, but we can't be sure 

    if not '"' in line:
        return line.split(',')
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

#control variables
bWriteReport = 1
bUseHeaderMappingFile = 1
bGetHeadersFromFile = 1

#file variables
in_folder = 'C:/Temp/python/in/'
in_file_list = ['deals.csv']
in_filename_headers = 'RW files/in_columns.txt' 

#out folder
out_folder = 'C:/Temp/python/out/RW Files/ByProduct/'
#out_file_name = 'out_' + time.strftime("%Y%m%d") + '_summary.csv'
#f_out = open(out_folder + out_file_name,'w')

#mapping folder
map_folder = out_folder
#map_file_name = 'out_' + time.strftime("%Y%m%d") + '_header_type_filename_mapping.csv'
map_file_name = 'out_20160617_header_type_filename_mapping.csv'

#list
list_header_type_filename_map = []

if bUseHeaderMappingFile:
    #get header-type header-filename mappings
    with open(map_folder + map_file_name,'r') as f_in:
        f_in.readline()
        for line in f_in:
            line_split = line.strip().split(',') 
            list_header_type_filename_map.append([line_split[0],line_split[1]])

elif bGetHeadersFromFile:
    
    list_header_type_filename_map.append(['this 1 header',in_filename_headers])
    
else:
    get_columns = (['Type','*Theoretical Model','GL Account','GL Notional','Name',
                   'Issue Date','Maturity Date','ID','Currency','K2 Book','Placeholder',
                   'Product Category','Product Type','Foreign Exchange List','Strike Dates Schedule','Binary Pay'])

#for every header type, get the file of header
for mapping in list_header_type_filename_map:
    
    this_header_type = mapping[0]
    this_header_filename = mapping[1]
    
    #open file
    this_out_filename = 'out_' + time.strftime("%Y%m%d") + '_deals_'  + preprocess_flename(this_header_type) + '.csv'
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
    
    for in_file in in_file_list:
        #this_out_file_name = in_file.replace('.csv.20160112', '_vect_removed.csv.20160112')
        #this_out_file = open(out_folder + this_out_file_name,'w')
        #print this_out_file_name 
        with open(in_folder + in_file, 'r') as this_in_file:
            line_count = 0
            for line in this_in_file:
                line_count+=1
                b_include_line = 1
                #if line[:5] ==',,,,,': b_include_line = 0
                if line[:5] ==',:pos': b_include_line = 0
                if line[:8] ==',Default': b_include_line = 0
                if line[:1] =='#': b_include_line = 0
                
                if b_include_line: 
                    #f_out.write(line)
                    
                    #case: NOT leading comma. we think this is a header
                    if not line[:1] ==',':
                        
                        #write previous record before moving onto the new header
                        if len(record_line_split_to_list)>0:
                            f_out.write(in_file)
                            f_out.write(',' + str(this_line_count))
                            
                            #write the optional columns
                            for idx in get_columns_header_index:
                                if idx==0:
                                    f_out.write(',')
                                else:
                                    f_out.write(',' + record_line_split_to_list[idx])
                            
                            f_out.write('\n')
                            record_line_split_to_list = []
                        
                        #determine if this header_type is in scope
                        bHeaderTypeInScope = 0
                        get_columns_header_index = []
                        header_line_split_to_list = line.split(',')
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
                                f_out.write(in_file)
                                f_out.write(',' + str(this_line_count))
                                
                                #write the optional columns
                                for idx in get_columns_header_index:
                                    if idx==0:
                                        f_out.write(',')
                                    else:
                                        f_out.write(',' + record_line_split_to_list[idx])
                                
                                f_out.write('\n')
                            
                            record_line_split_to_list = line_to_list(line)
                            this_line_count = line_count
                    
                    #case: 5 leading commas. we think this is a vector
                    if line[:5] ==',,,,,':
                        
                        #only process if this vector if it is associated with an "in-scope" header
                        if bHeaderTypeInScope == 1:
                            
                            vectorline_split_to_list = line_to_list(line)
                            
                            for idx in get_columns_header_index:
                                #idx==0 means the column is not in scope - do nothing
                                #blank value means there is no vector in this column - do nothing
                                if idx>0:
                                    if not vectorline_split_to_list[idx] == '':
                                        #append this value to the current line
                                        record_line_split_to_list[idx] += '|' + vectorline_split_to_list[idx]  
                        
                        
    #write the final record
    if len(record_line_split_to_list)>0:
        f_out.write(in_file)
        f_out.write(',' + str(this_line_count))
        
        #write the optional columns
        for idx in get_columns_header_index:
            if idx==0:
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
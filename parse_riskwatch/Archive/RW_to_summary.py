'''
Created on Jan 13, 2016

@author: mstirling

context: for some records, a vector of values populates within "one column for on one line" and syntax is roughly:
 ,A,B,C,"D1,D2,D3,D4",E,etc....

for v3 of this file, we transform ,A,B,C,"D1,D2,D3,D4",E, into ,A,B,C,D1|D2|D3|D4,E,
*we hope this won't cause further mistakes and confusion, but we can't be sure 

*now we're getting even more crazy

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

#control variables
bWriteReport = 1
bGetHeadersFromFile = 1

#file variables
in_folder = 'C:/Temp/python/in/'
in_file_list = ['deals.csv']
in_filename_headers = 'RW files/in_columns.txt' 

#out folder
out_folder = 'C:/Temp/python/out/'
out_file_name = 'out_' + time.strftime("%Y%m%d") + '_summary.csv'
f_out = open(out_folder + out_file_name,'w')

if bGetHeadersFromFile:
    get_columns = []
    with open(in_folder + in_filename_headers,'r') as f_in_headers:
        for line in f_in_headers:
            get_columns.append(line.strip())
else:
   get_columns = (['Type','*Theoretical Model','GL Account','GL Notional','Name',
                   'Issue Date','Maturity Date','ID','Currency','K2 Book','Placeholder',
                   'Product Category','Product Type','Foreign Exchange List','Strike Dates Schedule','Binary Pay'])

get_columns_header_index = [0 for col in get_columns]

#write the header
f_out.write('Name,row_num,file_name,' + str(','.join([col for col in get_columns])) + '\n')
this_header_type = ''

for in_file in in_file_list:
    #this_out_file_name = in_file.replace('.csv.20160112', '_vect_removed.csv.20160112')
    #this_out_file = open(out_folder + this_out_file_name,'w')
    #print this_out_file_name 
    with open(in_folder + in_file, 'r') as this_in_file:
        line_count = 0
        for line in this_in_file:
            line_count+=1
            b_include_line = 1
            if line[:5] ==',,,,,': b_include_line = 0
            if line[:5] ==',:pos': b_include_line = 0
            if line[:8] ==',Default': b_include_line = 0
            if line[:1] =='#': b_include_line = 0
            if b_include_line: 
                #f_out.write(line)
                
                #case: NOT leading comma. we think this is a header
                if not line[:1] ==',':
                    #get the "index in the header" of every column we're looking for 
                    get_columns_header_index = []
                    line_split_to_list = line.split(',')
                    for col in get_columns:
                        try:
                            #print line_split_to_list.index(col)
                            get_columns_header_index.append(int(line_split_to_list.index(col)))
                        except:
                            #don't see this column in the header
                            get_columns_header_index.append(0)
                
                #case: leading comma. we think this is a record
                if line[:1] ==',':
                    line_split_to_list = line_to_list(line)
                    f_out.write(line_split_to_list[1])
                    f_out.write(',' + str(line_count))
                    f_out.write(',' + in_file)
                    
                    #write the optional columns
                    for idx in get_columns_header_index:
                        if idx==0:
                            f_out.write(',')
                        else:
                            f_out.write(',' + line_split_to_list[idx])
                    
                    f_out.write('\n')
                    
f_out.close()

print 'done.'
for filename in in_file_list:
    print 'from ' + in_folder + filename

print 'to ' + out_folder + out_file_name


'''
Created on Jun 9, 2016

@author: mstirling
'''
import time, pandas as pd

def line_to_list(line):
    return line.split(',')

#time
t1 = time.time()

#file variables
in_folder = 'C:/Temp/python/in/'
in_file_list = ['deals.csv']
out_folder = 'C:/Temp/python/out/'
out_file = 'out_' + time.strftime("%Y%m%d") + '_all_headers.csv' 

#dataframe
df = pd.DataFrame(columns=['type','header'])

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
                    for header in [header for header in line_split_to_list if not header in ['',this_header_type]]:
                        df.loc[len(df)] = [this_header_type,header] 
                        
                #case: leading comma. we think this is a record
                #do nothing
                #if line[:1] ==',':
                    
df.to_csv(out_file)

print 'done.'
for filename in in_file_list:
    print 'from ' + in_folder + filename

print 'to ' + out_folder + out_file
  
t2 = time.time()
print 'total run = ' + str(t2-t1)
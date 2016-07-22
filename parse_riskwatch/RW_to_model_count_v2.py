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

v5 goal is to only point to a single folder as input

'''
import time, pandas as pd, os

#control variables
bGetDataFromFiles = 0
bCreateGroupByReport = 1

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

if bGetDataFromFiles:
    
    #main folder
    #parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.06.14/'
    #list_child_folder = ['asia','basemetals','corr','energy','ged','gef','mocatta','repo','southam','spread']
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.06.14_try2/'
    list_child_folder = ['all']
    in_file_list = ['deals.csv']
    in_file_audit_list = ['deals_audit.csv']
        
    #out folder
    out_folder = parent_folder + 'report/'
    out_filename = 'out_' + time.strftime("%Y%m%d") + '_count_by_product.csv' 
    
    #make sure we have the folder
    try:
        os.stat(out_folder[:-1])
    except:
        os.mkdir(out_folder[:-1])
    
    #open the file
    f_out = open(out_folder + out_filename,'w')
    
    #get the headers
    get_columns = ['*Theoretical Model', 'Name']
        
    #write the header
    f_out.write('Session,Folder,Filename,Row Num,Header Type,*Theoretical Model,Name')
    
    #session
    this_session = 'VaR Riskwatch'
    
    for child_folder in list_child_folder: 
    
        #file variables
        in_folder = parent_folder + child_folder + '/'
        
        print child_folder
        
        #initial variables
        get_columns_header_index = [0 for col in get_columns]
        record_line_split_to_list = []
        this_line_count = 0
        
        for i in xrange(len(in_file_list)):
            in_file = in_file_list[i]
            in_file_audit = in_file_audit_list[i]
            
            #open files
            this_in_file = open(in_folder + in_file, 'r')
            this_in_file_audit = open(in_folder + in_file_audit, 'r') 
            
            #initialize line count
            #remove this in order to get the line count from the original file
            line_count = 0
            
            for line in this_in_file:
                line_count+=1
                
                 #read from the auditfile
                audit_line = this_in_file_audit.readline()
                
                b_include_line = 1
                if line[:5] ==',,,,,': b_include_line = 0
                if line[:5] ==',:pos': b_include_line = 0
                if line[:8] ==',Default': b_include_line = 0
                if line[:1] =='#': b_include_line = 0
                
                if b_include_line: 
                    #f_out.write(line)
                    
                    [audit_file_in, str_audit_line_count] = audit_line.strip().split(',')
                    
                    #case: NOT leading comma. we think this is a header
                    if not line[:1] ==',':
                        
                        get_columns_header_index = []
                        header_line_split_to_list = line_to_list(line)
                        this_header_type = header_line_split_to_list[0]
                            
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
                        
                        record_line_split_to_list = line_to_list(line)
                        max_len = len(record_line_split_to_list)
                        f_out.write('\n')
                        f_out.write('VAR')
                        f_out.write(',' + child_folder)
                        f_out.write(',' + audit_file_in)
                        f_out.write(',' + str_audit_line_count)
                        f_out.write(',' + this_header_type)
                        
                        #write the optional columns (in this file, Name and *Theoretical Model
                        for idx in get_columns_header_index:
                            if idx==0 or idx>=max_len:
                                f_out.write(',')
                            else:
                                try:
                                    f_out.write(',' + record_line_split_to_list[idx])
                                except: 
                                    print line
                                    print idx
                                    record_line_split_to_list[idx]
                                    f_out.write(',' + record_line_split_to_list[idx])

    print 'done.'
    for filename in in_file_list:
        print 'from ' + in_folder + filename
    
    print 'to ' + out_folder

if bCreateGroupByReport:
    
    parent_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.06.14_try2/'
    out_folder = parent_folder + 'report/'
    
    in_file='out_20160628_count_by_product.csv'
    out_file = 'report_count_by_product_by_system.csv'
    
    #load data
    df = pd.read_csv(out_folder+in_file)
    df_file_system_map = pd.read_csv(parent_folder + 'calibration/ctr_rules/file_system_map.csv')
    
    #left join source system
    df = pd.merge(df,df_file_system_map,how='left',on=['Filename'])
    
    df_group=df.groupby(['Header Type','*Theoretical Model','Source_System'])['Name'].agg(['count'])
    df_group.to_csv(out_folder + out_file)
    print df_group
    
    #df_pivot = df.pivot_table(df,index=['Header Type','*Theoretical Model'],columns=['Source_System'],aggfunc='count',fill_value=0)
    df_pivot = df_group.unstack('Source_System').fillna(0)
    df_pivot.to_csv(out_folder + out_file)
    print df_pivot
    
    
    
t2 = time.time()
print 'total run = ' + str(t2-t1) + ' ms'
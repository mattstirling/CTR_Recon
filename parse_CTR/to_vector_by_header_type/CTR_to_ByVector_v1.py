'''
Created on Jan 13, 2016

@author: mstirling

'''
import time, os, ConfigParser, glob

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


#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in folder
parent_folder = config.get('filename','parent_folder')

in_folder = 'riskwatch/'
out_folder_byvector = 'riskwatch_ctrfile_by_vector/'

#files in scope
header_type_in_scope = (['BNS Asset Asian'
                    ,'BNS Asset Option'
                    ,'BNS Bermuda Swaption'
                    ,'BNS CapFloor'
                    ,'BNS Currency Swap'
                    ,'BNS Default Swap'
                    ,'BNS Forex'
                    ,'BNS Fra'
                    ,'BNS Swap'
                    ,'BNS Swaption'
                    ,'BNS Total Return Equity Swap'
                    ])

#fields in scope
columns_in_scope = (['Cap Notional Principal'
                    ,'Dividend Cashflow'
                    ,'Expiry Dates Schedule'
                    ,'Fees'
                    ,'FI Fees'
                    ,'FI Notional'
                    ,'FI Principal Payment'
                    ,'Notional Adjustments'
                    ,'Pay Fees'
                    ,'Pay Principal Payment'
                    ,'Premium'
                    ,'Realized Dividends'
                    ,'Rec Fees'
                    ,'Rec Principal Payment'
                    ,'Redemption Premium'
                    ,'Spot Reset schedule'
                    ,'Stock Price Schedule'
                    ,'Strike Dates Schedule'
                    ,'Swap Notional'
                    ,'Swap Pay Notional'
                    ,'Swap Rec Notional'
                    ,'Swap Ref Notional'
                    ])

#out header cols
out_header_cols = 'id,rw_column,date,amt,curr'

#make sure we have the folder
try:
    os.stat(parent_folder + out_folder_byvector[:-1])
except:
    os.mkdir(parent_folder + out_folder_byvector[:-1])

ctr_path_list = glob.glob(parent_folder + in_folder + '*.csv')
ctr_file_list = [i[len(parent_folder + in_folder):] for i in ctr_path_list]

for this_file in ctr_file_list:
   
    print parent_folder + in_folder + this_file
    f_in = open(parent_folder + in_folder + this_file,'r')
    f_header = f_in.readline().strip().split(',')
    
    if f_header[0] in header_type_in_scope:
    
        this_index_id = f_header.index('ID')
        
        #open the file to write out to
        out_file_parent = 'out_vectors_' + this_file
            
        #get a list of fields in the header that are vectors
        vector_cols = []
        for i in range(len(f_header)):
            if f_header[i] in columns_in_scope:
                this_out_file = out_file_parent.replace('.csv','_' + f_header[i].replace(' ','_') + '.csv')
                this_f_out = open(parent_folder + out_folder_byvector + this_out_file,'w') 
                this_f_out.write(out_header_cols)
                vector_cols.append([f_header[i],i,this_f_out])
                
        
        for line in f_in:
            this_line = line_to_list(line)
            
            
            for [v_name, v_index, f_out] in vector_cols:
                
                this_id = this_line[this_index_id]
                this_vector_value = this_line[v_index]
            
                if len(this_vector_value)>0:
                    this_vector_value_list = this_vector_value.strip('(').strip(')').split('|')    
                    
                    for j in this_vector_value_list:
                        j_list = j.strip(' ').split(' ')
                        this_date = j_list[0]
                        
                        if len(j_list)>1: this_amt = j_list[1] 
                        else:this_amt='' 
                        
                        if len(j_list)>2: this_curr = j_list[2] 
                        else:this_curr=''
                        
                        record_to_insert = ([str(this_id)
                                            ,str(v_name)
                                            ,str(this_date)
                                            ,str(this_amt)
                                            ,str(this_curr)])
                        f_out.write('\n' + ','.join(record_to_insert))
            
        
        
    
print 'done'
    


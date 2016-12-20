'''
Created on Jan 13, 2016

@author: mstirling

'''
import time, os, ConfigParser

#open config file
config = ConfigParser.ConfigParser()
config.read('config.ini')

#in folder
in_folder = config.get('filename','parent_folder')

in_folder_byproduct = 'all/ByProduct/'
out_folder_byvector = 'all/ByVector/'

#files in scope
files_in_scope = (['out_deals_BNS_Asset_Asian.csv'
                    ,'out_deals_BNS_Asset_Option.csv'
                    ,'out_deals_BNS_Bermuda_Swaption.csv'
                    ,'out_deals_BNS_CapFloor.csv'
                    ,'out_deals_BNS_Currency_Swap.csv'
                    ,'out_deals_BNS_Default_Swap.csv'
                    ,'out_deals_BNS_Forex.csv'
                    ,'out_deals_BNS_Fra.csv'
                    ,'out_deals_BNS_Swap.csv'
                    ,'out_deals_BNS_Swaption.csv'
                    ,'out_deals_BNS_Total_Return_Equity_Swap.csv'
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
    os.stat(in_folder + out_folder_byvector[:-1])
except:
    os.mkdir(in_folder + out_folder_byvector[:-1])

for this_file in files_in_scope:
    
    f_in = open(in_folder + in_folder_byproduct + this_file,'r')
    f_header = f_in.readline().strip().split(',')
    this_index_id = f_header.index('ID')
    
    #open the file to write out to
    out_file_parent = this_file.replace('out_deals_','out_vectors_')
        
    #get a list of fields in the header that are vectors
    vector_cols = []
    for i in range(len(f_header)):
        if f_header[i] in columns_in_scope:
            this_out_file = out_file_parent.replace('.csv','_' + f_header[i].replace(' ','_') + '.csv')
            this_f_out = open(in_folder + out_folder_byvector + this_out_file,'w') 
            this_f_out.write(out_header_cols)
            vector_cols.append([f_header[i],i,this_f_out])
            
    
    for line in f_in:
        this_line = line.strip().split(',')
        
        
        for [v_name, v_index, f_out] in vector_cols:
            
            this_id = this_line[this_index_id]
            this_vector_value = this_line[v_index]
        
            if len(this_vector_value)>0:
                this_vector_value_list = this_vector_value.strip('(').strip(')').split('|')    
                
                for j in this_vector_value_list:
                    j_list = j.split(' ')
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
        
    #close the file    
    f_out.close()
   
        
    
print 'done'
    


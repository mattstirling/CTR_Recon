'''
Created on Jan 17, 2017

@author: mstirling
'''
import pandas as pd, os, time

#timing
t1 = time.time()

#in folder
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/RW_ECR_Release_10/CTR_input_files_used/K2/by_vector/'
in_file_list = ['out_Swap_C_Swap_v1_84_Pay_Fixings.csv','out_Swap_C_Swap_v1_84_Rec_Fixings.csv']

out_folder = in_folder + 'out_for_thomas_try2/'

#make sure we have the output folder
try: os.stat(out_folder[:-1])
except: os.mkdir(out_folder[:-1])

for in_file in in_file_list:
    
    out_file = in_file[:-4] + 'for_var_testing.txt'

    #output file
    f_out = open(out_folder + out_file,'w')
    
    #open vector file
    df = pd.read_csv(in_folder+in_file, header = None, usecols = [3,4,5,6], dtype={6: str})
    df.columns = ['id','vector_name','date','amt']
    
    #get all ids in this file
    id_list = df.id.unique()
    
    #for each id, order records by date desc and then merge into 1 str
    for this_id in id_list:
        this_id_df = df.loc[df.id.isin([this_id])]
        this_id_df.sort(['date'],ascending = False, inplace=True)
        rw_val = ', '.join(this_id_df.amt.tolist())
        f_out.write(this_id + '|' + rw_val + '\n')
        df = df[-df.id.isin([this_id])]
    f_out.close()
    
print 'done'

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' sec'

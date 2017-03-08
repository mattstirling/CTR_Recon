'''
Created on Feb 7, 2017

@author: mstirling
'''

import preprocess_ETL
import pandas as pd, numpy as np

in_folder = 'C:\Users\mstirling\Desktop\Shared\RW\CTR Files\RW_ECR_Release_12\CTR_output_file\out_K2_Asset_Option\mtm_compare\etd/'.replace('\\', '/')
in_file = 'K2_CSM_Equity_Option_ETD_D_20170131_2_RiskWatch.csv'
out_file = in_file.replace('.csv','_v2.csv')

#in_bench_folder = 'C:\Users\mstirling\Desktop\Shared\RW\CTR Files\RW_ECR_Release_12\CTR_output_file\out_K2_TRS/'.replace('\\', '/')
#in_bench_file = 'out_K2_TRS_VAR_preprocessed_file.csv'

df = pd.read_csv(in_folder + in_file)
#df_bench = pd.read_csv(in_bench_folder + in_bench_file) 


#Perform defaulting rules
#print df[(df.ID == ':K2.T92846')]['Underlying Instrument']
df.loc[df['Foreign Exchange List'] == 'CAD', 'Foreign Exchange List'] = 'CAD, USD'
df.loc[df['Foreign Exchange List'] == 'USD', 'Foreign Exchange List'] = 'CAD, USD'
#df['Asset Resets'] = [preprocess_ETL.number_list_divide_by_100(x) for x in df['Asset Resets']]
#df['Rec Rate'] = [preprocess_ETL.rec_rate_x100(x) for x in df['Rec Rate']]
#df['FI Spread'] = [preprocess_ETL.number_list_reverse(x) for x in df['FI Spread']]

#right-join the benchmark file to the ctr file
#rename benchmark column names
#df_bench.columns = [i + '_bench' for i in df_bench.columns]
#df_bench['Name'] = 'K2.' + df_bench['Name_bench']
#df_merge = pd.merge(df,df_bench, how='left',on='Name')

#add benchmark values to the file
#df_merge['Asset Reset Dates_bench'] = [preprocess_ETL.date_list_bar_to_comma_space(i) for i in df_merge['Asset Reset Dates_bench']]
#df['Asset Reset Dates'] = df_merge['Asset Reset Dates_bench'] 

#df_merge['FI Reset Dates_bench'] = [preprocess_ETL.date_list_bar_to_comma_space(i) for i in df_merge['FI Reset Dates_bench']]
#df['FI Reset Dates'] = df_merge['FI Reset Dates_bench'] 

#print len(df.index)
#drop any records in ctr that are not in benchmark (as the ETL is now causing errors)
#df = df[np.in1d(df['Name'],df_bench['Name'])]
#print len(df.index)
#print df[(df.ID == ':K2.T92846')]['Underlying Instrument']

df.to_csv(in_folder + out_file, index=False)

print 'done.'
print 'to ' + in_folder + out_file





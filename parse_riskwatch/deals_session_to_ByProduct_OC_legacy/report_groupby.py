'''
Created on Oct 20, 2016

@author: mstirling
'''
import pandas as pd,os

#in file
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.10.19/'
in_file = 'all_OC_legacy/ByProduct/out_deals_BNS_Forex.csv'

#out file
out_folder = in_folder
out_file = 'report_OC_legacy/out_deals_BNS_Forex_by_source_by_model.csv'

df = pd.read_csv(in_folder + in_file)
df_group = df.groupby(['Filename','*Theoretical Model']).size()

df_group.to_csv(out_folder + out_file)

print 'done.'
print 'wrote from: ' + in_folder + in_file
print 'wrote to: ' + out_folder + out_file
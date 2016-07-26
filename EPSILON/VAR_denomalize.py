'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd

#control variables
bWriteReport = 1

#in VAR files
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.07.21/'
in_file_TRS = 'all/ByProduct/out_20160722_deals_BNS_Total_Return_Equity_Swap.csv' 

#out folder
out_folder = in_folder + 'recon/'
out_file_FX_Deals = 'EPSILON_TRS.csv'

#open in_files
df_TRS = pd.read_csv(in_folder+in_file_TRS)
#print len(df_TRS.index)

#filter 
df_TRS = df_TRS[(df_TRS.Filename == '/Sybase_Epsilon_processed.csv')&(df_TRS.Name.str.contains("EpsilonTRS"))]
#print len(df_TRS.index)

#sort by Name
df_TRS.sort('Name', inplace = True)

#write out_files
df_TRS.to_csv(out_folder + out_file_FX_Deals,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder

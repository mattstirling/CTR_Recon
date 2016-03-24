'''
Created on Feb 23, 2016

@author: mstirling
'''
import pandas as pd

#control variables
bWriteReport = 1
sort_col = 'Name'

#file variables
in_folder = 'C:/Temp/python/in/RW files/OC/'
in_file_FX_Deals = 'FXOCDEALS_SE.CSV.20160218'
in_file_FX_Deals_PFE = 'FXOCDEALS_SE_PFE.CSV.20160218'

#out folder
out_folder = 'C:/Temp/python/out/RW Files/OC/'
out_file_FX_Deals = 'RW_denormalized_FXOCDEALS_SE.CSV.20160218'

#open in_files
df_FX_Deals = pd.read_csv(in_folder+in_file_FX_Deals)
df_FX_Deals_PFE = pd.read_csv(in_folder+in_file_FX_Deals_PFE)

#sort by Name
df_FX_Deals.sort(sort_col, inplace = True)

#write out_files
df_FX_Deals.to_csv(out_folder + out_file_FX_Deals,index=False)

print 'done.'
print 'from ' + in_folder
print 'to ' + out_folder

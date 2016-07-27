'''
Created on Jul 26, 2016

@author: mstirling
'''
import pandas as pd, os, time

#in folder
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.07.21/'
by_prod_folder = in_folder + 'all/ByProduct/'
out_folder = in_folder + 'report/'

out_file = 'out_nan_count_by_product.csv'

exclude_file_list = ['out_header_type_filename_mapping.csv']

list_df_nonnull = []

for filename in [f for f in os.listdir(by_prod_folder) if (f[-4:]=='.csv' and f not in exclude_file_list)]:
    print filename 
    df = pd.read_csv(by_prod_folder+filename)
    total_len = len(df.index)
    nonnull_count_series = df.count()
    list_filename = [filename for i in nonnull_count_series.index]
    list_total = [total_len for i in nonnull_count_series.index]
    df_nonnull = pd.DataFrame({'filename':list_filename,'column':nonnull_count_series.index,'nonnull':nonnull_count_series.tolist(), 'total': list_total},index = range(len(nonnull_count_series.index)))
    list_df_nonnull.append(df_nonnull)


df_out = pd.concat(list_df_nonnull, ignore_index=True)

df_out.to_csv(out_folder+out_file)

print 'done.'
print 'from: ' + by_prod_folder
print 'to: ' + out_folder

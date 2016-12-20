'''
Created on Dec 16, 2016

@author: mstirling
'''

import glob2

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#in
this_folder = 'C:/Users/mstirling/Desktop/Shared/RW/CTR Files/2016-12-15-UAT/RISKWATCH_ANVIL_20161215/' 

#out
out_folder = 'C:/Temp/python/out/'
out_file = 'out_count_by_file.csv'
f_out = open(out_folder + out_file,'w')
f_out.write('filename,file_len')

for f in glob2.glob(this_folder + '**/*.csv'):
    this_file = f.replace('\\',"/")
    this_file_len = file_len(this_file)
    print str(this_file) + ',' + str(this_file_len)
    f_out.write('\n' + str(this_file) + ',' + str(this_file_len))

print 'done'
print 'wrote to: ' + out_folder + out_file
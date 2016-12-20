'''
Created on Dec 16, 2016

@author: mstirling
'''
import collections
import hashlib

#in folder
in_folder = 'C:/Users/mstirling/Desktop/'
in_file = 'K2_CM_Swap_D_20161216_01.csv'
count = 0

dub_line_list = []
out_folder = in_folder
out_file = 'out_dupe_lines.txt'

f_out = open(out_folder + out_file,'w')
f_out.write('dupe lines')

d = collections.defaultdict(list)
with open(in_folder + in_file, 'r') as datafile:
    for line in datafile:
        count = count + 1 
        this_id = hashlib.sha256(line).digest()
        # Or id = line[:n]
        k = this_id[0:2]
        v = this_id[2:]
        if v in d[k]:
            print str(count) + ': ' + str(line).strip()
            dub_line_list.append(count)
            f_out.write('\n' + line.strip())
        else:
            d[k].append(v)


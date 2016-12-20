'''
Created on Dec 16, 2016

@author: mstirling
'''


this_trade_id = 'SS3006'

#in folder
in_folder = 'C:/Users/mstirling/Desktop/'
in_file = 'K2_CM_Swap_D_20161215_02.csv'

start_line = 560000
end_line = 561000

out_folder = 'C:/Temp/python/out/'
out_file = in_file[:-4] + '_' + str(start_line) + '_' + str(end_line) + '.txt' 
f_out = open(out_folder + out_file,'w')

f_in = open(in_folder + in_file,'r')

for i in xrange(end_line):
    if i < start_line:
        f_in.readline()
    else:
        f_out.write(f_in.readline())
    
print 'done.'
print 'written to: ' + out_folder + out_file
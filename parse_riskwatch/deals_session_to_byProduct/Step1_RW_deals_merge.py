'''
18-Aug-2015
mstirling

for 1 folder, iterate through all files and write records into 1 file

'''

#import libraries
import os, time

#timing
t1 = time.time()

#in folder + out folder
in_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.06.14_try2/calibration/deals'
out_folder = 'C:/Users/mstirling/Desktop/Shared/RW/VAR Session/market.16.06.14_try2/all/'
out_file = 'deals.csv'
out_audit_file = 'deals_audit.csv'

list_filenames_to_skip = (['__bns__derivProdData__riskWatch__Mocatta__baseMetals__RW__deals__day1__Counterparty_static.csv',
                           '__bns__derivProdData__riskWatch__Mocatta__baseMetals__RW__deals__day1__baseMetals_MTM.csv',
                           '__bns__var_rw__data__riskwatch__adpim__adp_isin_scusa.csv',
                           '__bns__var_rw__data__riskwatch__adpim__adp_isin_tor.csv',
                           '__bns__var_rw__data__riskwatch__adpim__adp_warrant_scusa.csv',
                           '__bns__var_rw__data__riskwatch__adpim__adp_warrant_tor.csv',
                           '__bns__var_rw__storage__position__inverlat__mdpraptipobase.csv.20160614.0',
                           '__bns__var_rw__storage__position__inverlat__tesoreria_md_tipobase.csv.20160614.0',
                           '__bns__var_rw__data__riskwatch__costa_rica__exceptions_costa_rica.csv'])


#get the files we are interested in
f_out = open(out_folder + out_file,'w')
f_audit_out = open(out_folder + out_audit_file,'w')

for (dirpath, dirnames, filenames) in os.walk(in_folder):
    this_dirpath = dirpath.replace('\\','/')
    this_dir = dirpath[len(in_folder):].replace('\\','/')
    
    for filename in [f for f in filenames if f not in list_filenames_to_skip]:
        #only grab files with the inclusion date
        #if included_date in filename:
        #CTR_filelist.extend(filename)
        #f.write(str(this_dir) + '/' + str(filename) + '\n') # python will convert \n to os.linesep
        this_dirfile = this_dir + '/' + filename 
        this_dirfilepath = this_dirpath + '/' + filename
        line_cnt_infile = 1
        print this_dirfile
        
        f_in = open(this_dirfilepath,'r')
        for line in f_in:
            f_out.write(line.strip() + '\n')
            f_audit_out.write(this_dirfile + ',' + str(line_cnt_infile) + '\n')
            line_cnt_infile += 1
        f_in.close()

#close file          
f_out.close()

#done message
print 'done files from ' + str(in_folder) 
print 'wrote to ' + str(out_folder) + str(out_file)

t2 = time.time()
print 'total run = ' + str(t2-t1) + ' ms'


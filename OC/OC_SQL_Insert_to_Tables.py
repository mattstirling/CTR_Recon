'''
Created on Feb 26, 2016

@author: mstirling
'''
import sqlite3

def path_to_file(path):
    return str(path)[path.rfind('/'):]

def preprocess_header(name):
    replace_list = [[' ','_'],['*',''],['-',''],['/','']]
    new_name = name
    for item in replace_list:
        new_name = new_name.replace(item[0],item[1])
    return new_name

#list files to upload
db_path = 'C:/Users/mstirling/Desktop/Shared/CTR_Recon/SQL/CTR_Recon_2.db'
in_list_file = 'C:/Users/mstirling/Desktop/Shared/CTR_Recon/OC 2016-01-18/SQL Files/Filename_SQLTable_Map.csv' 

#common headers are in every SQL table
common_headers = ['Source Name','File Date','File Name']
this_source = 'OC'
this_filedate = '2016-01-18'

#get the pathnames of the files
#skip the header, line format is "path, SQL_tablename"
in_list_pathnames = []
f_in = open(in_list_file,'r')
next(f_in)
for line in f_in:
    items = line.strip().split(',')
    in_list_pathnames.append([items[0],items[1]])
f_in.close()

#if database is not created, this line will create the database
conn=sqlite3.connect(db_path)
c = conn.cursor()

for file_table in in_list_pathnames:
    this_path = file_table[0]
    this_table_name = file_table[1]
    
    #get headers from the this filepath
    f_in = open(this_path,'r')
    this_file_header_list_len = len(f_in.readline().strip().split(','))
    common_header_list_len = len(common_headers)
    
    record_list = []
    
    for line in f_in:
        this_record = [this_source,this_filedate,path_to_file(this_path)]
        this_record.extend(line.strip().split(','))
        record_list.append(this_record)
    
    print this_table_name
    SQL = 'insert into ' + this_table_name + ' values (' + ','.join(['?' for i in xrange(this_file_header_list_len + common_header_list_len)]) + ')'
    c.executemany(SQL, record_list)
    conn.commit()

print 'done'
print 'files from: ' +  in_list_file
print 'to database table: ' + db_path            

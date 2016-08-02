'''
Created on Feb 24, 2016

@author: mstirling
'''
import sqlite3

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
    
    #begin with header common to all tables
    this_header_list = list(common_headers)
    
    #get headers from the this filepath
    f_in = open(this_path,'r')
    this_file_header_list = f_in.readline().strip().split(',')
    this_header_list.extend(this_file_header_list)
    this_header_list = [preprocess_header(header) for header in this_header_list]
    print (this_table_name, this_header_list)
    
    #write the sql Create statement
    SQL = 'create table ' + this_table_name + ' (' + ' text, '.join(this_header_list) + ' text)'
    
    #execute the SQL
    c.execute(SQL)

print 'done.'
print 'files from: ' +  in_list_file
print 'to database table: ' + db_path
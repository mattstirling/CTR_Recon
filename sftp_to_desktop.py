'''
Created on Feb 29, 2016

@author: mstirling
'''
import pysftp, os, time

t1 = time.time()

#folder data
pass_folder = 'C:/Temp/python/in/Ref Data/'
pass_filename = 'rw_unix.txt'

#get password for server
f = open(pass_folder + pass_filename,'r')
this_host = f.readline().strip()
this_username = f.readline().strip()
this_pass = f.readline().strip()
f.close()

print this_host
print this_username
print this_pass

#server folders
out_folder = 'C:/Users/mstirling/Desktop/Shared/RW/'

#server data
server_path_list = ['/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/riskwatch/']
public_local_map_list = [['/home/mstirl','home']]

#filter data
filter_filedate = '20160224'
filter_systemname = 'ANVIL'


#
# main program
#

#connect to the server
sftp = pysftp.Connection(this_host, username=this_username, password=this_pass)

for this_map in public_local_map_list:
    
    this_public = this_map[0]
    this_local = this_map[1]
    
    #make the folder if it's not already there
    try:
        os.stat(out_folder + this_local)
    except:
        os.mkdir(out_folder + this_local)    
    
    sftp.get_r(this_public,out_folder + this_local, preserve_mtime = True)


    print 'done. from ' + this_public + ' to ' + out_folder + this_local
    
 
t2 = time.time()
print 'total run = ' + str(t2-t1) + ' ms'

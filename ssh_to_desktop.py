'''
Created on Feb 29, 2016

@author: mstirling
'''
import paramiko, os, time

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

#server folders
out_folder = 'C:/Users/mstirling/Desktop/Shared/RW/'

#server data
server_path_list = ['/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/riskwatch/']
public_local_map_list = [['/home/mstirl','home']]

#
# main program
#

#get filenames from ctr unix server
paramiko.util.log_to_file('ssh.log') #turns on logging for access the unix file using ssh/smtp

#connect to the server
ssh = paramiko.SSHClient() 
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(this_host, username=this_username, password=this_pass)
stdin, stdout, stderr = ssh.exec_command('ls -l')
sftp = ssh.open_sftp()

for this_map in public_local_map_list:
    
    this_public = this_map[0]
    this_local = this_map[1]
    
    #make the folder if it's not already there
    try:
        os.stat(out_folder + this_local)
    except:
        os.mkdir(out_folder + this_local)    
    
    #get the files we are interested in
    serverfile_list = sftp.listdir(path=this_public)
    for server_file in serverfile_list:
        sftp.get(this_public + str(server_file), out_folder + this_local + '/' + str(server_file))
        
    sftp.get_r(this_public,out_folder + this_local, preserve_mtime = True)


    print 'done. from ' + this_public + ' to ' + out_folder + this_local


t2 = time.time()
print 'total run = ' + str(t2-t1) + ' ms'
                
'''
Created on Feb 29, 2016

@author: mstirling
'''
import paramiko

#folder data
in_folder = 'C:/Temp/python/in/'
pass_file = 'ctr_unix_prd.txt'
out_download_folder = 'C:/Temp/python/in/CTR files/ANVIL/'

#server data
server_path_list = ['/opt/ctr/ctr/ctrapp/ctr/ctrarchive/outfiles/riskwatch/']

#filter data
filter_filedate = '20160224'
filter_systemname = 'ANVIL'

#get password for server
f = open(in_folder + pass_file,'r')
ctr_host = f.readline().strip()
ctr_username = f.readline().strip()
ctr_pass = f.readline().strip()
f.close()

#
# main program
#

#get filenames from ctr unix server
paramiko.util.log_to_file('ssh.log') #turns on logging for access the unix file using ssh/smtp

#connect to the server
ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ctr_host, username=ctr_username, password=ctr_pass)
stdin, stdout, stderr = ssh.exec_command('ls -l')
sftp = ssh.open_sftp()

#for each folder on the server
for server_path in server_path_list:
    
    #get the files we are interested in
    serverfile_list = sftp.listdir(path=server_path)
    for server_file in serverfile_list:
        
        #filter for 1 date
        #apply any other filters
        if filter_filedate in server_file and filter_systemname in server_file:
            
            print 'saving ' + str(server_file)
            sftp.get(server_path + str(server_file), out_download_folder + str(server_file))
            
print 'got server files from ' + server_path

print 'done'  
                
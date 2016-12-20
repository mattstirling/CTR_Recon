'''
Created on Nov 15, 2016

@author: mstirling
'''

in_folder = 'C:/Temp/python/in/'
in_file = 'portfolio_list.txt'

str_temp = ''

for line in open(in_folder + in_file, 'r'):
    for letter in line.strip():
        if not letter in str_temp:
            str_temp = str_temp + letter 
            print letter

print str_temp

    

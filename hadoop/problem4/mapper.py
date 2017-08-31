#!/usr/bin/python

# Format of each line is:
# date\ttime\tstore name\titem description\tcost\tmethod of payment
#
# We want elements 2 (store name) and 4 (cost)
# We need to write them out to standard output, separated by a tab

import sys 
import re 
for line in sys.stdin :
	data=line.strip().split(" ");
	if len(data)==10: 
		ip_address,identity,username,datetime ,timezone,method,path,proto,status,size =data ;
		clean_path=re.sub(r"^http://www.the-associates.co.uk", '',path);
		print "{0}\t{1}".format(clean_path,1) ;

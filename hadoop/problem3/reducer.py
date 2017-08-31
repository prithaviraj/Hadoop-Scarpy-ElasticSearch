#!/usr/bin/python
import sys ;
current_ip =None ;
requested_count=0 ;
for line in sys.stdin: 
	data=line.strip().split();
	if len(data)!=2 :
		continue ;
	new_ip , count =data ;
	if current_ip and current_ip != new_ip :
		if(current_ip=="10.99.99.186") :						
			print "{0}\t{1}".format(current_ip , requested_count);
		requested_count = 0;
	current_ip = new_ip ;
	requested_count+=1;
	
if current_ip !=None :
	print "{0}\t{1}".format(current_ip , requested_count);

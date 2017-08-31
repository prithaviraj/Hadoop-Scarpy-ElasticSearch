#!/usr/bin/python
import sys ;
current_path =None ;
requested_count=0 ;
for line in sys.stdin: 
	data=line.strip().split();
	if len(data)!=2 :
		continue ;
	new_path , count =data ;
	if current_path and current_path != new_path :
		if(current_path=="/assets/js/the-associates.js") :						
			print "{0}\t{1}".format(current_path , requested_count);
		requested_count = 0;
	current_path = new_path ;
	requested_count+=1;
	
if current_path !=None :
	print "{0}\t{1}".format(current_path , requested_count);

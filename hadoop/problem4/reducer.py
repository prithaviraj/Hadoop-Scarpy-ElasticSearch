#!/usr/bin/python
import sys ;
current_path =None ;
request_count=0 ;
maxpath = None ;
maxcount = 0 ;
for line in sys.stdin: 
	data=line.strip().split("\t");
	if len(data)!=2 :
		continue ;
	new_path , count =data ;
	if current_path and current_path != new_path :
		if(request_count>maxcount) :						
			maxcount=request_count ;
			maxpath = current_path ;
			print "{0}\t{1}".format(maxpath , maxcount);
			#print "here 1";
		#print "here 2";
		request_count = 0;
		current_path = new_path ;
	#print "here 3 "	
	current_path = new_path ;
	request_count+=1;

if current_path!=None :
	if(request_count>maxcount) :						
			maxcount=request_count ;
			maxpath = current_path ;
	
print "{0}\t{1}".format(maxpath , maxcount);

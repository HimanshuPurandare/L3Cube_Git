'''
* This is a 'SIMPLE VERSION CONTROL' program.

* MongoDB is used at the back-end. The data is stored in 
  Database:'svc', Collection:'my_collection'.
  
* Program implements two methods
	1) commit            : Saves the new version  
	2) display_version   : Retrieves current/older versions
	
* Softwares required
    1) Python  (v2.7.8)
    2) MongoDB (v2.6.3)
  
'''
from pymongo import MongoClient
import sys

'''The function saves the new version in the database'''
def commit(file_name , my_collection):
	print "commit"
	obj = my_collection.find_one({"fileid": file_name})
	print obj
	if str(obj) == 'None':
		print "Creating first version"
		
		f = open(file_name,'r+')
		i = 1
		line_list = {}
		ver_line_list = []
		for line in f:
			line_list[line] = i
			ver_line_list.append(i)
			i = i+1		
		
		f.close()

		ver_list = { "0" : ver_line_list }
		
		doc = { "fileid" : file_name ,
				"lines" : line_list ,
				"version" : ver_list }
				
		my_collection.insert_one(doc)		
	else:
		print "Previous versions are available"
		lines_in_all_versions = obj['lines']
		
		lines_in_all_versions_keys = lines_in_all_versions.keys()
		
		line_list_curr_ver = []
		
		f = open(file_name,'r+')
		
		for line in f:
			if line in lines_in_all_versions_keys:
				line_list_curr_ver.append(lines_in_all_versions[line])
			else:
				temp = len(lines_in_all_versions.keys()) + 1
				lines_in_all_versions[line] = temp 
				line_list_curr_ver.append(lines_in_all_versions[line])
		
		version_length = len(obj['version'].keys())
		print version_length
	
		ver_dict = obj['version']
		ver_dict[str(version_length)] = line_list_curr_ver
		
		obj1 = { "fileid" : file_name ,
				"lines" :  lines_in_all_versions,
				"version" : ver_dict }
				
		my_collection.update({"fileid" : file_name},{"$set": obj1})
		
		print "Done!!"

'''The function retrieves the current/older versions from the database'''
def display_version(file_name , version_num , my_collection):
	print "The version is displayed"
	obj = my_collection.find_one({"fileid": file_name})
	print obj
	
	ver_dict = obj['version']
	all_line_dict = obj['lines']
	ver_line_list = ver_dict[str(version_num)]
	
	my_dict2 = {y:x for x,y in all_line_dict.iteritems()}
	
	print "\n\n\n"
	print str(version_num)+"th Version of ",file_name
	
	for i in ver_line_list:
		print my_dict2[i]
	

if __name__ == '__main__':
	argv_list=sys.argv
	
	'''Connect to the database'''
	client=MongoClient('localhost',27017)
	
	'''Get the currently present databases'''
	db_list=client.database_names()
	
	'''Check whether'svc' database is present'''
	if 'svc' not in db_list:
		svc=client.get_database('svc')
	else:
		svc=client['svc']
		
	'''Get the currently present collections'''
	collection_list=svc.collection_names()
	
	'''Check whether'my_collection' collection is present'''
	if 'my_collection' not in collection_list:
		my_collection=svc.get_collection('my_collection')
	else:
		my_collection=svc['my_collection']	
		
	'''Get command line arguments'''
	print argv_list
	
	if len(argv_list)==1:
		print "Command line arguments are not provided"
	elif len(argv_list) == 2:
		commit(argv_list[1],my_collection)
	elif len(argv_list) == 3:
		display_version(argv_list[1],argv_list[2],my_collection)
	else:
		print "Too many arguments"
		
		

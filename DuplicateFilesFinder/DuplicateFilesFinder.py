"""
This program finds the duplicate files in the given directory.
1.Run the program using terminal command:
				$python programname.py
2.Then a window will open.
3.Select the directory on which you want to apply check by pressing 'Open' button(at top-left corner).
4.Then press 'Apply' button(at top-right corner) to apply the duplicate file check on that directory.If you want to apply
	the check on whole drive or pen-drive you can select it like: /media/username/pendrive_or_partition_name
5.You will see the list of all duplicate files listed as:


				Hash value1
				1) file1
				2) file2
				Hash value2
				1) file1
				2) file2
				3) file3

Here 2 files are having same hash value i.e. they are duplicate.And other 3 files are duplicates of each other with hash_value2.

6.Select all the files which you want to delete and press the 'Delete' button.

*The program uses md5 message digest algorithm.It searchs all files recursively in the given path and applys this algorithm to all files and all
files with same hash value are considered as duplicates of each other and shown in list.

**The program calculates hash value of file chunk by chunk so that program doesen't fail even for large files
	 having size greater than RAM size.(10-20GB) 

"""
import sys
import os
import hashlib
import time
from PyQt4 import QtGui,QtCore
from PyQt4.Qt import *



def check_duplicates(dup_list):

#	---------------Declaring lists 1.f_pointers and 2.hash_list which will hold file pointers and hash objects of all files in dup_list

	f_pointers=[]
	hash_list=[]

#	---------------The lists f_pointers and hash_list are initialised here

	for f in dup_list: 
		h=hashlib.md5()
		fp=open(f,'r')
		fp.close()
		f_pointers.append(fp)
		hash_list.append(h)
		

#	print f_pointers,hash_list
#	---------------This flag variable is used to decide the end of while loop		

	flag=1
	f_size=os.path.getsize(dup_list[0])
	
#	--------------- The chunk_size is decided according the size of file,to increase overall efficiecy of program.

	if f_size>10**9:
		chunk_size=1073741824
	elif f_size>10**6:
		chunk_size=1048576
	else:
		chunk_size=10240


	while flag and len(f_pointers):

		for ptr in range(len(f_pointers)):

#	---------------data read from file and respective hash value is updated

			fp=open(f_pointers[ptr].name,f_pointers[ptr].mode)
			fp.seek(0,2)
			if fp.tell()>(flag-1)*chunk_size:
				fp.seek((flag-1)*chunk_size)
				d=fp.read(chunk_size)
				hash_list[ptr].update(d)
				
				
			else:
				d=''
			
			fp.close()
	
#			print "Now the flag is:",flag #Flag will be updated as file wil be travrsed
#	---------------If this is end of last file in list then while loop is broken
			
			if not d :
#				print "Now flag=0"
				flag=0
				break
		
		if flag:
			flag+=1
#			print flag*chunk_size


#	---------------Comment out to check hexdigest values of objects in hash_list		
#		for h in hash_list:
#			print h.hexdigest()



		hash_map={}
		
#	Forming the hash_map dictionary of elements of hash_list 
#	This helps to remove the files of which no further checking is required

		for h in hash_list:
			hex_of_h=h.hexdigest()
			if hex_of_h in hash_map.keys():
				hash_map[hex_of_h].append(h)
			else:
				same_digest_list=[h]
				hash_map[hex_of_h]=same_digest_list
		
		
#	---------------Comment out to check the formed hash_map				
#		print hash_map
				
		for i in hash_map.keys():
			if len(hash_map[i])==1:
				f_index=hash_list.index(hash_map[i][0])
				del hash_map[i]
				del f_pointers[f_index]
				del hash_list[f_index]
		

#	---------------The hash_map is dictionary which contains 				
	
	hash_map={}			
	
	for i in range(len(hash_list)):
		if hash_list[i].hexdigest() in hash_map.keys():
			hash_map[hash_list[i].hexdigest()].append(f_pointers[i].name)
		else:
			f_path_list=[]
			f_path_list.append(f_pointers[i].name)
			hash_map[hash_list[i].hexdigest()]=f_path_list
			
#	---------------The dictionary of hash values as key and list of all files having that hash value as value of that resp key		
	
	return hash_map
		
	





###				-------------------------------------This function accepts the root path and --------------------------------------------------
def accept_path(dir_path):
	
#	t1 is start time of program	
	t1=time.time()
	
#	all files dictionary is returned which is the final list of duplicate files
	all_files={}
	
	dup_count=0
	copies_count=0
	return_list={}

	#/media/niranjan/NIRANJAN/MyPhotos&Videos/MyVideos/Movies/Bollywood Movies/BollywoodMovies/Untitled Folder
	for current_path,dir_list,file_list in os.walk(dir_path):

	#	---------------Making all file dictionary file_list----->>>>Future Change:Print/Show the current checking dirs also

		for f in file_list:
			f_path=os.path.join(current_path,f)
			f_size=os.path.getsize(f_path)
			if f_size in all_files.keys():
				all_files[f_size].append(f_path)
			else:
				same_size_list=[]
				same_size_list.append(f_path)
				all_files[f_size]=same_size_list


#	---------------	Applying check_duplicate function on list of files of same size	

	for same_list in all_files.values():
#		print same_list
		if len(same_list)>1:
			dups=check_duplicates(same_list)		
			for i in dups.keys():		
				return_list[i]=dups[i]
	
			
			
	t2=time.time()
	
#	---------------	printing of time required for finding duplicate files in the given directory/path
#	print t2-t1           

	return return_list




class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()

#	--------------- The function is executed after pressing the 'Open' button
    def myopen(self):
		folder = QtGui.QFileDialog.getExistingDirectory(None, "Select folder")
		self.textbox.setText(""+folder)

#	--------------- This function is executed after pressing the 'Delete button'

    def mydelete(self):
		abc = []
		abc = self.list.selectedItems()
				
		for a in abc:
			a = str(a.text()).split(") ")[1]
			os.remove(a)

		directory = self.textbox.text()
		d=accept_path(str(directory))
		
		x = d.keys()
		y = d.values()
		
		self.list.clear()
		for a in x:
			temp = d[a]
			my_item = QListWidgetItem(a)
			my_item.setFlags(QtCore.Qt.NoItemFlags)	
			self.list.addItem(my_item)
			i = 1
			for b in temp:
				my_item1 = QListWidgetItem(str(i)+") "+str(b))	
				self.list.addItem(my_item1)
				i = i+1
			
			
#	--------------- This function is executed when apply button is pressed ;and this function passes directory chosen by user
 
    def myapply(self):
		directory = self.textbox.text()
		d=accept_path(str(directory))
		
		self.list.clear()

		x = d.keys()
		y = d.values()
		
		for a in x:
			temp = d[a]
			my_item = QListWidgetItem(a)
			my_item.setFlags(QtCore.Qt.NoItemFlags)	
			self.list.addItem(my_item)
			i = 1
			for b in temp:
				my_item1 = QListWidgetItem(str(i)+") "+str(b))	
				self.list.addItem(my_item1)
				i = i+1
		
    def initUI(self):      

		self.main_frame = QWidget()
				       
		self.btn = QPushButton('Open', self)
		self.btn.setToolTip('Click to select folder')
		self.btn.resize(self.btn.sizeHint())	
		self.btn.move(10,13)		
		self.btn.clicked.connect(self.myopen)

		screen = QtGui.QDesktopWidget().screenGeometry()
		 	
		self.textbox = QtGui.QLineEdit(self)
		self.textbox.resize(screen.width()-300,35)
		self.textbox.move(100,10)

		self.btn1 = QPushButton('Apply', self)
		self.btn1.setToolTip('Click to find duplicate files')
		self.btn1.resize(self.btn.sizeHint())	
		self.btn1.move(screen.width()-200,13)		
		self.btn1.clicked.connect(self.myapply)

		self.list = QListWidget(self)
		self.list.move(10 , 50)
		self.list.resize((screen.width())-100, ((screen.height())/10)*8)
		self.list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		
		self.btn2 = QPushButton('Delete', self)
		self.btn2.setToolTip('Click to delete files')
		self.btn2.resize(self.btn.sizeHint())	
		self.btn2.move((screen.width())-300,((screen.height())/10)*8 + 75)		
		self.btn2.clicked.connect(self.mydelete)

		self.showMaximized()		
		self.setWindowTitle('Duplicate file finder')
		self.show()
                                    
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
	main()



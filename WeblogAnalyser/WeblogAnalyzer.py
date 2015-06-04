"""
* PyQt is used for making GUI
* All the fields of packets are displayed in table
* These packets can be filtered out
	Filtering is done on the basis of IP and request method.
	syntax is:
		IP==82.28.27.27
		METHOD==GET   or   METHOD==POST
		
* Colour coding scheme is used for displaying packets
	For ex: RED :- Status code is 4xx or 5xx
* After clicking on each packet, All the information about packet is displayed 
* There is toolbar and Menubar. Various options are present there.
* After pressing graph menu, graph is displayed.
	Graph is plotted Number of bytes in MB/Number of days in may
* Library Matplotlib is used for plotting graph
"""
import sys, os, random ,re
from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure



class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
		if not index.isValid():
			return None
		elif role == Qt.BackgroundRole:
			if int(self.mylist[index.row()][3]) > 399:
				return QBrush(Qt.red)
			elif int(self.mylist[index.row()][3]) > 299 and int(self.mylist[index.row()][3]) <399:
				return QBrush(Qt.cyan)

		elif role == Qt.DisplayRole:
			return self.mylist[index.row()][index.column()]
		elif role == Qt.TextAlignmentRole:
			return Qt.AlignCenter
		return None
        
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None



class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Web Log Analysis')

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        #self.on_draw()

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        
        path = unicode(QFileDialog.getSaveFileName(self, 
                        'Save file', '', 
                        file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)
    
    def on_about(self):
        msg = """ 
					* All the fields of packets are displayed in table
					* These packets can be filtered out
						Filtering is done on the basis of IP and request method.
						syntax is:
							IP==82.28.27.27
							METHOD==GET   or   METHOD==POST
		
					* Colour coding scheme is used for displaying packets
						For ex: RED :- Status code is 4xx or 5xx
					* After clicking on each packet, All the information about packet is displayed 
					* There is toolbar and Menubar. Various options are present there.
					* After pressing graph menu, graph is displayed.
						Graph is plotted Number of bytes in MB/Number of days in may
        """
        QMessageBox.about(self, "About the demo", msg.strip())
    
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        QMessageBox.information(self, "Click!", msg)
    
    def on_draw(self):

		if(len(self.data)!=0):
			print self.data[0][3]
			print self.data[0][9]
			d = {}
			print len(self.data) 
			i = 0
			for a in self.data:
				st = a[3]
				got_date = st[:2]
				if str(a[9]) == '-':
					print "Do nothing"
				else:
					got_date = int(got_date)  
					s = d.keys()
					if got_date in s:
						print got_date," : ",d[got_date]
						d[got_date] = int(d[got_date]) + int(a[9])
					else:
						d[got_date] = int(a[9])
		    			print d[got_date]
		    	
		    
		   
			print d
			x = d.keys()
			y = d.values()
			for i in range(0,len(y)):
				y[i] = float(y[i])/ 1000000.0
			print x
			print y
		    # clear the axes and redraw the plot anew
		    #
			self.axes.clear()        
			self.axes.grid(True)
		    
			self.axes.set_xlabel('Date of month')
			self.axes.set_ylabel('Size of data sent in MB')                
		    
			self.axes.bar(
		        left=x, 
		        height=y, 
		        width=20.00 / 100.0, 
		        align='center', 
		        alpha=0.44,
		        picker=10)
		    
			self.canvas.draw()


    def myapply(self):
		expression = self.textbox.displayText()
		print "Expression in filter is "+expression
		if expression == "":
			tablemodel = MyTableModel(self, self.tabledata, self.header)
			self.tableview.setModel(tablemodel)
			self.tableview.resizeColumnsToContents()   	 	
			hh = self.tableview.horizontalHeader()
			hh.setStretchLastSection(True)				
		elif expression[:4] == "IP==":
			IP_addr = expression[4:]
			temp = []
			for a in self.tabledata:
			
				if a[0] == IP_addr:
					temp.append(a)
					
			if len(temp) == 0:
				QMessageBox.about(self, "Ooopps", "IP enterred is either wrong or there isn't entry for this IP.")		
			else:		
				tablemodel = MyTableModel(self, temp, self.header)
				self.tableview.setModel(tablemodel) 
				self.tableview.resizeColumnsToContents()   	 	
				hh = self.tableview.horizontalHeader()
				hh.setStretchLastSection(True)
		elif expression[:8] == "METHOD==":
			method = expression[8:]
			temp = []
			for a in self.tabledata:
				if a[2] == method:
					temp.append(a)
					
			if len(temp) == 0:
				QMessageBox.about(self, "Ooopps", "METHOD enterred is either wrong or there isn't entry for this.")		
			else:		
				tablemodel = MyTableModel(self, temp, self.header)
				self.tableview.setModel(tablemodel) 
				self.tableview.resizeColumnsToContents()   	 	
				hh = self.tableview.horizontalHeader()
				hh.setStretchLastSection(True)
		
		else:
			if len(self.tabledata) == 0:
				QMessageBox.about(self, "Ooopps", "Table is empty")		
			else:
				QMessageBox.about(self, "Ooopps", "Check your enterred expression!!")        		
    def up(self):
    	print "Up"
    	
    def myrefresh(self):
    	print "refresh"	
    	
    def down(self):
    	print "down"    
        
    def show_graph(self):
		self.tableview.setVisible(False)
		self.list.setVisible(False)
		print "graph" 
		self.canvas.setVisible(True)
		self.mpl_toolbar.setVisible(True)
		self.on_draw()

    def show_table(self):
		self.canvas.setVisible(False)
		self.mpl_toolbar.setVisible(False)
		print "show_table"
		self.tableview.setVisible(True)
		self.list.setVisible(True)

    
    def myopen(self):
		print "open" 

		self.tabledata = []
		self.data = []
		filename = QFileDialog.getOpenFileName(self, 'Open File', '/')
		print filename
		
		f = open(filename,'r+')

		for line in f:
			matchObj = re.match( r'(.*?) (.*?) (.*?) \[(.*?) (.*?)\] "(.*?) (.*?) (.*?)" (.*?) (.*?) "(.*?)" "(.*)"', line, re.M|re.I)
			if matchObj:
				a = (matchObj.group(1),matchObj.group(4),matchObj.group(6),matchObj.group(9),matchObj.group(10),matchObj.group(7))      
				self.tabledata.append(a)
				b = (matchObj.group(1),matchObj.group(2),matchObj.group(3),matchObj.group(4),matchObj.group(5),matchObj.group(6),matchObj.group(7),matchObj.group(8),matchObj.group(9),matchObj.group(10),matchObj.group(11),matchObj.group(12))
				self.data.append(b)
        
		tablemodel = MyTableModel(self, self.tabledata, self.header)
		self.tableview.setModel(tablemodel)
		self.tableview.resizeColumnsToContents()   	 	
		hh = self.tableview.horizontalHeader()
		hh.setStretchLastSection(True)		
		
		self.btn.setEnabled(True)

    	
    def myclose(self):
    	print "close"
    	self.close()    
    		
    def viewclicked(self,index):
		row = index.row()
		self.list.clear()
		self.list.addItem(QListWidgetItem("Ip address         "+self.data[row][0]))	 
		self.list.addItem(QListWidgetItem("User-identifier    "+self.data[row][1]))
		self.list.addItem(QListWidgetItem("Frank              "+self.data[row][2]))
		self.list.addItem(QListWidgetItem("Date and Time      "+self.data[row][3]))
		self.list.addItem(QListWidgetItem("Request Method     "+self.data[row][5]))
		self.list.addItem(QListWidgetItem("URL                "+self.data[row][6]))
		self.list.addItem(QListWidgetItem("Http version       "+self.data[row][7]))
		self.list.addItem(QListWidgetItem("Status             "+self.data[row][8]))
		self.list.addItem(QListWidgetItem("Bytes sent         "+self.data[row][9]))
		self.list.addItem(QListWidgetItem("Web page referred  "+self.data[row][10]))
		self.list.addItem(QListWidgetItem("Browser information"+self.data[row][11]))
    		    		    
    def create_main_frame(self):
		self.main_frame = QWidget()

		self.data = []

		exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.myclose)

		openAction = QtGui.QAction(QtGui.QIcon('open24.jpeg'), 'Open', self)
		openAction.setShortcut('Ctrl+O')
		openAction.setStatusTip('Open File')
		openAction.triggered.connect(self.myopen)
		
		tableAction = QtGui.QAction(QtGui.QIcon('table24.png'), 'Table', self)
		tableAction.setShortcut('Ctrl+T')
		tableAction.setStatusTip('Table View')
		tableAction.triggered.connect(self.show_table)

		graphAction = QtGui.QAction(QtGui.QIcon('graph24.png'), 'Graph', self)
		graphAction.setShortcut('Ctrl+G')
		graphAction.setStatusTip('Graphical View')
		graphAction.triggered.connect(self.show_graph)

		refreshAction = QtGui.QAction(QtGui.QIcon('refresh24.gif'), 'Refresh', self)
		refreshAction.setStatusTip('Refresh')
		refreshAction.triggered.connect(self.myrefresh)

		upAction = QtGui.QAction(QtGui.QIcon('up24.gif'), 'Up', self)
		upAction.setStatusTip('Up')
		upAction.triggered.connect(self.up)

		downAction = QtGui.QAction(QtGui.QIcon('down24.gif'), 'Down', self)
		downAction.setStatusTip('Down')
		downAction.triggered.connect(self.down)

		self.dpi = 150
		self.fig = Figure((5.0, 4.0), dpi=self.dpi)
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self.main_frame)
		
		self.axes = self.fig.add_subplot(111)
        
		self.canvas.mpl_connect('pick_event', self.on_pick)
        
		self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

		self.canvas.move(280,80)		
		self.mpl_toolbar.move(280,80)
		self.canvas.setVisible(False)
		self.mpl_toolbar.setVisible(False)
                
		toolbar = self.addToolBar('Exit')

		toolbar.setStyleSheet('QToolBar{spacing:10px;}')
		toolbar.addAction(openAction)
		toolbar.addSeparator()
		toolbar.addAction(tableAction)
		toolbar.addAction(graphAction)
		toolbar.addSeparator()		
		toolbar.addAction(refreshAction)
		toolbar.addAction(upAction)
		toolbar.addAction(downAction)
		toolbar.addSeparator()
		toolbar.addAction(exitAction)
		 
		self.textbox = QtGui.QLineEdit(self)
		self.textbox.resize(280,35)
		self.textbox.move(10, 70)

		self.btn = QPushButton('Apply', self)
		self.btn.setToolTip('Click to apply expression')
		self.btn.resize(self.btn.sizeHint())	
		self.btn.move(300, 73)		
		self.btn.clicked.connect(self.myapply)
		self.btn.setEnabled(False)

		self.tabledata = [()]

		self.header = ["  IP address  ","  Date and time  ","  Request Method  ","  Status code  ","  Number of bytes  ","  URL  "]
		
		tablemodel = MyTableModel(self, self.tabledata, self.header)
		self.tableview = QTableView(self)
		self.tableview.setModel(tablemodel)
		
		self.tableview.move(10, 130)
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.tableview.resize((screen.width())-100, ((screen.height())/7)*3)
        # set font
		font = QFont("Arial Black", 10)
		self.tableview.setFont(font)
        # set column width to fit contents (set font first!)
		#self.tableview.resizeColumnsToContents()
		self.tableview.setShowGrid(False)
		self.tableview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.tableview.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.tableview.setStyleSheet('background-color:rgb(180, 250, 140);')
		self.tableview.clicked.connect(self.viewclicked)
		
		#hh = self.tableview.horizontalHeader()
		#hh.setStretchLastSection(True)        
		# set row height
		
		nrows = len(self.tabledata)
		for row in xrange(nrows):
			self.tableview.setRowHeight(row, 24)		
			
		vh = self.tableview.verticalHeader()
		vh.setVisible(False)
        
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.list = QListWidget(self)
		self.list.move(10 , 150 + ((screen.height())/7)*3)
		self.list.resize((screen.width())-100, ((screen.height())/4))

		self.showMaximized()
		self.setCentralWidget(self.canvas)
    
    def create_status_bar(self):
        self.status_text = QLabel("Ready")
        self.statusBar().addWidget(self.status_text, 1)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plot, 
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (load_file_action, None, quit_action))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

def main():
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()

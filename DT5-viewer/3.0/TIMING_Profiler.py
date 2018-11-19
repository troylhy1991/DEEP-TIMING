import re
import operator
import os
import sys 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

import numpy as np

class Nanowell_Tag():
	def __init__(self):
		self.dataset = 'Dataset ID'
		self.BID = 1
		self.R = 1
		self.C = 1
		self.E_Num = 0
		self.T_Num = 0
		self.tSeek1 = 0
		self.TimInt = 0
		self.DInt = 0
		self.EDInt = 0

 
class TIMING_Profiler(QMainWindow): 
	def __init__(self, Data_Info, Tag): 
		QWidget.__init__(self)

		
		self.Tag = Nanowell_Tag()
		self.Tag.dataset = Tag.dataset
		self.Tag.TimInt = Tag.TimInt
		self.Tag.DInt = Tag.DInt
		self.Tag.EDInt = Tag.EDInt

		self.object_selected = 0
		self.path = Data_Info.path

		export_data_action = QAction('&Export Table',self)
		export_data_action.setShortcut('Ctrl+E')
		#export_data_action.triggered.connect(self.export_data)
		menubar = self.menuBar()
		OPTMenu = menubar.addMenu('&Operations')
		OPTMenu.addAction(export_data_action)

		# add Dataset ID and Table Selection
		HBox1 = QHBoxLayout()
		dataset_tag = QLabel("Dataset:     ")
		HBox1.addWidget(dataset_tag)
		dataset_ID = QLabel(Data_Info.name)
		HBox1.addWidget(dataset_ID)
		
		HBox2 = QHBoxLayout()
		table_tag = QLabel("Profile Table:")
		HBox2.addWidget(table_tag)
		self.table_combo = QComboBox(self)
		self.table_combo.addItem('Table_1E0T')
		self.table_combo.addItem('Table_0E1T')
		self.table_combo.addItem('Table_1E1T')
		self.table_combo.addItem('Table_1E2T')
		self.table_combo.addItem('Table_1E3T')
		HBox2.addWidget(self.table_combo)
		
		self.table_combo.currentIndexChanged.connect(self.load_another_table)
		
		self.nanowells = QLabel('')
		HBox3 = QHBoxLayout()
		number_tag = QLabel('# of Nanowells')
		HBox3.addWidget(number_tag)
		HBox3.addWidget(self.nanowells)
		
		# create table
		self.get_table_data()
		self.table = self.createTable(self.Table_1E0T, self.Header_1E0T) 
		self.table.selectRow(self.object_selected)
		
		

		
		self.VBox = QVBoxLayout()
		self.VBox.addLayout(HBox1)
		self.VBox.addLayout(HBox2)
		self.VBox.addLayout(HBox3)
		self.VBox.addWidget(self.table)
		
		self.main_widget = QWidget()
		self.main_widget.setLayout(self.VBox)
		
		self.setCentralWidget(self.main_widget)
		self.setWindowTitle("TIMING2 Viewer 2.0 Profiler")
		self.show()
		
	def export_data(self):
		# path = str(QFileDialog.getExistingDirectory(self,"Save feature table ..."))
		# path = path + "\\"
		# filename = path + "feature_table.txt"
		# np.savetxt(filename, self.feature_table.tolist(), fmt = '%d \t %d \t %d \t %d \t %1.2f \t %d \t %1.2f \t %1.2f \t %1.2f \t %1.2f')
		print "Not Enabled yet..."
		
	def get_table_data(self):
		self.Table_1E0T = []
		self.Header_1E0T = []
		filename = os.getenv("HOME") + '/Table_1E0T.txt'
		f = open(filename,'r')
		head_temp = f.readline()
		table_temp = f.readlines()
		f.close()
		
		self.Header_1E0T = head_temp.strip('\n').split('\t')
		self.Header_1E0T.append('Status')
		for line in table_temp:
			temp1 = line.strip('\n').split('\t')
			temp = []
			temp.append(int(temp1[0]))
			for x in temp1[1:]:
				temp.append(float("{0:.2f}".format(float(x))))
			temp.append(0)
			self.Table_1E0T.append(temp)
				
		
		self.Table_0E1T = []
		self.Header_0E1T = []
		filename = os.getenv("HOME") + '/Table_0E1T.txt'
		f = open(filename,'r')
		head_temp = f.readline()
		table_temp = f.readlines()
		f.close()
		
		self.Header_0E1T = head_temp.strip('\n').split('\t')
		self.Header_0E1T.append('Status')
		for line in table_temp:
			temp1 = line.strip('\n').split('\t')
			temp = []
			temp.append(int(temp1[0]))
			for x in temp1[1:]:
				temp.append(float("{0:.2f}".format(float(x))))
			temp.append(0)
			self.Table_0E1T.append(temp)
		
		
		self.Table_1E1T = []
		self.Header_1E1T = []
		
		filename = os.getenv("HOME") + '/Table_1E1T.txt'
		f = open(filename,'r')
		head_temp = f.readline()
		table_temp = f.readlines()
		f.close()
		
		self.Header_1E1T = head_temp.strip('\n').split('\t')
		self.Header_1E1T.append('Status')
		for line in table_temp:
			temp1 = line.strip('\n').split('\t')
			temp = []
			temp.append(int(temp1[0]))
			for x in temp1[1:]:
				temp.append(float("{0:.2f}".format(float(x))))
			temp.append(0)
			self.Table_1E1T.append(temp)
		
		self.Table_1E2T = []
		self.Header_1E2T = []
		
		filename = os.getenv("HOME") + '/Table_1E2T.txt'
		f = open(filename,'r')
		head_temp = f.readline()
		table_temp = f.readlines()
		f.close()
		
		self.Header_1E2T = head_temp.strip('\n').split('\t')
		self.Header_1E2T.append('Status')
		for line in table_temp:
			temp1 = line.strip('\n').split('\t')
			temp = []
			temp.append(int(temp1[0]))
			for x in temp1[1:]:
				temp.append(float("{0:.2f}".format(float(x))))
			temp.append(0)
			self.Table_1E2T.append(temp)
		
		self.Table_1E3T = []
		self.Header_1E3T = []
		
		filename = os.getenv("HOME") + '/Table_1E3T.txt'
		f = open(filename,'r')
		head_temp = f.readline()
		table_temp = f.readlines()
		f.close()
		
		self.Header_1E3T = head_temp.strip('\n').split('\t')
		self.Header_1E3T.append('Status')
		for line in table_temp:
			temp1 = line.strip('\n').split('\t')
			temp = []
			temp.append(int(temp1[0]))
			for x in temp1[1:]:
				temp.append(float("{0:.2f}".format(float(x))))
			temp.append(0)
			self.Table_1E3T.append(temp)
		
	def createTable(self, table, header):
		# create the view
		tv = QTableView()

		# set the table model
		tm = MyTableModel(table, header, self) 
		tv.setModel(tm)

		# set the minimum size
		tv.setMinimumSize(600, 300)

		# hide grid
		tv.setShowGrid(False)

		# set the font
		font = QFont("Courier New", 8)
		tv.setFont(font)

		# hide vertical header
		vh = tv.verticalHeader()
		vh.setVisible(False)

		# set horizontal header properties
		hh = tv.horizontalHeader()
		hh.setStretchLastSection(True)

		# set column width to fit contents
		tv.resizeColumnsToContents()

		# set row height
		nrows = len(table)
		for row in xrange(nrows):
			tv.setRowHeight(row, 18)
		
		self.nanowells.setText(str(nrows))

		# enable sorting
		tv.setSortingEnabled(True)

		tv.setSelectionBehavior(QAbstractItemView.SelectRows)

		# mouse click setting
		tv.clicked.connect(self.nanowell_was_clicked)

		return tv

	def nanowell_was_clicked(self):
		row = self.table.selectionModel().currentIndex().row()
		column = 0
		model = self.table.model()
		index = model.index(row, column)
		Nanowell_ID = int(model.data(index, Qt.DisplayRole).toString())
		
		BID = Nanowell_ID/10000
		C = Nanowell_ID%100
		R = (Nanowell_ID - BID*10000)/100
		
		self.Tag.BID = BID
		self.Tag.C = C
		self.Tag.R = R
		
		current_table = self.table_combo.currentText()
		
		if current_table == 'Table_0E1T':
			self.Tag.E_Num = 0
			self.Tag.T_Num = 1
		
		if current_table == 'Table_1E0T':
			self.Tag.E_Num = 1
			self.Tag.T_Num = 0
			
		if current_table == 'Table_1E1T':
			self.Tag.E_Num = 1
			self.Tag.T_Num = 1
			index = model.index(row, 1)
			tSeek = int(model.data(index, Qt.DisplayRole).toString())
			tSeek = int(tSeek/self.Tag.TimInt)
			if tSeek<0:
				tSeek = 0
			self.Tag.tSeek1 = tSeek
			
		if current_table == 'Table_1E2T':
			self.Tag.E_Num = 1
			self.Tag.T_Num = 2
			index = model.index(row, 1)
			tSeek = int(model.data(index, Qt.DisplayRole).toString())
			tSeek = int(tSeek/self.Tag.TimInt)
			if tSeek<0:
				tSeek = 0
			self.Tag.tSeek1 = tSeek
			
		if current_table == 'Table_1E3T':
			self.Tag.E_Num = 1
			self.Tag.T_Num = 3
			index = model.index(row, 1)
			tSeek = int(model.data(index, Qt.DisplayRole).toString())
			tSeek = int(tSeek/self.Tag.TimInt)
			if tSeek<0:
				tSeek = 0
			self.Tag.tSeek1 = tSeek
		
		self.emit(SIGNAL("Nanowell_Table_Selection"), self.path, self.Tag)
		
	def object_selection_slot(self, cell_selection_ID = None):
		# nrows = len(self.tabledata)
		# for row in range(0,nrows):
			# column = 0
			# model = self.table.model()
			# index = model.index(row, column)
			# cell_ID = int(model.data(index, Qt.DisplayRole).toString())
			# if cell_ID == cell_selection_ID:
				# self.object_selected = cell_selection_ID
				# self.table.selectRow(row)
				# return
		print "Object Selected"

	def load_another_table(self):
		self.table.deleteLater()
		current_table = self.table_combo.currentText()
		
		if current_table == 'Table_0E1T':
			table = self.Table_0E1T
			header = self.Header_0E1T
		
		if current_table == 'Table_1E0T':
			table = self.Table_1E0T
			header = self.Header_1E0T
		
		if current_table == 'Table_1E1T':
			table = self.Table_1E1T
			header = self.Header_1E1T
			
		if current_table == 'Table_1E2T':
			table = self.Table_1E2T
			header = self.Header_1E2T
			
		if current_table == 'Table_1E3T':
			table = self.Table_1E3T
			header = self.Header_1E3T
		
		self.table = self.createTable(table,header)
		
		self.VBox.addWidget(self.table)
 
class MyTableModel(QAbstractTableModel): 
	def __init__(self, datain, headerdata, parent=None, *args): 
		""" datain: a list of lists
			headerdata: a list of strings
		"""
		QAbstractTableModel.__init__(self, parent, *args) 
		self.arraydata = datain
		self.headerdata = headerdata

	def rowCount(self, parent): 
		return len(self.arraydata) 
 
	def columnCount(self, parent): 
		return len(self.arraydata[0]) 
 
	def data(self, index, role): 
		if not index.isValid(): 
			return QVariant() 
		elif role != Qt.DisplayRole: 
			return QVariant() 
		return QVariant(self.arraydata[index.row()][index.column()]) 

	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.headerdata[col])
		return QVariant()

	def sort(self, Ncol, order):
		"""Sort table by given column number.
		"""
		self.emit(SIGNAL("layoutAboutToBeChanged()"))
		self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
		if order == Qt.DescendingOrder:
			self.arraydata.reverse()
		self.emit(SIGNAL("layoutChanged()"))


def main(): 
    app = QApplication(sys.argv) 
    w = TIMING_Profiler() 
    #w.show() 
    sys.exit(app.exec_()) 

		
if __name__ == "__main__": 
	main()

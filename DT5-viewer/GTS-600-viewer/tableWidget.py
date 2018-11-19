import re
import operator
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np

class Nanowell_Tag():
	'''
	A Nanowell Tag instance is created anytime a nanowell is clicked.
	And the Nanowell Tag will be passed to the slider widget
	'''
	def __init__(self):
		self.DATASET = 1
		self.GROUP = 1
		self.GLOBAL_SEQ = 1
		self.SEQ = 1
		self.FRAMES = 1
		self.E_num = 0
		self.T_num = 0


class tableWidget(QWidget):
	def __init__(self, Dataset_Tag):
		QWidget.__init__(self)

		self.Tag = Dataset_Tag
		self.object_selected = 0
		self.path = Dataset_Tag.path

		# add Dataset ID
		HBox1 = QHBoxLayout()
		dataset_tag = QLabel("Dataset:     ")
		HBox1.addWidget(dataset_tag)
		dataset_ID = QLabel(Dataset_Tag.dataset)
		HBox1.addWidget(dataset_ID)


		self.nanowells = QLabel('')
		HBox2 = QHBoxLayout()
		number_tag = QLabel('# of Nanowells')
		HBox2.addWidget(number_tag)
		HBox2.addWidget(self.nanowells)

		# create table
		# self.Header = ['Block ID', 'Nano ID', 'E #', 'T #', 'Error_Video', 'Error_Frames', 'Edited']
		self.Header = ['INDEX' , 'DATASET' , 'GROUP' , 'SEQ' , 'FRAMES' , 'E#' , 'T#']
		self.Table_Data = [[1,1,1,1,1,0,0]]
		self.table = self.createTable(self.Table_Data, self.Header)
		self.table.selectRow(self.object_selected)


		self.VBox = QVBoxLayout()
		self.VBox.addLayout(HBox1)
		self.VBox.addLayout(HBox2)
		self.VBox.addWidget(self.table)

		self.setLayout(self.VBox)
		self.show()


	def get_table_data(self):
		self.table.deleteLater()
		self.Table_Data = []

		filename = self.Tag.path + '/GTS-1000-table-LOG.txt'

		if os.path.isfile(filename) == True:
			print("Reload table data ... ")
			f = open(filename,'r')
			table_temp = f.readlines()
			f.close()

			for line in table_temp:
				temp1 = line.strip('\n').split('\t')
				#temp = [int(i) for i in temp1]
				temp1[0] = int(temp1[0])
				temp1[4] = int(temp1[4])
				temp1[5] = int(temp1[5])
				temp1[6] = int(temp1[6])
				self.Table_Data.append(temp1)

		else:
			print("Load New table data ... ")
			for block in self.Tag.block_list:
				fname = self.Tag.path + block + '/labels/DET/FRCNN-Fast/raw/selected_nanowells.txt'
				#print(int(block[1:]))
				f = open(fname)
				lines = f.readlines()
				f.close()

				for line in lines:
					line = line.rstrip().split('\t')
					line = [int(i) for i in line]
					temp = []
					temp.append(int(block[1:]))
					temp.append(line[0])
					temp.append(line[1])
					temp.append(line[2])
					temp.append(0)
					temp.append(0)
					temp.append(0)
					#print(temp)
					self.Table_Data.append(temp)

		self.table = self.createTable(self.Table_Data, self.Header)
		self.VBox.addWidget(self.table)
		#print(self.Table_Data)
		#self.Table_Data = Table_Data

	# def refreshTable(self):
		# '''
		# After the correction of the annotation, the table will update some values and refresh its own look.
		# '''
		# self.table = self.createTable(self.Table_Data, self.Header)


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
		GLOBAL_SEQ = int(model.data(index, Qt.DisplayRole).toString())

		column = 1
		model = self.table.model()
		index = model.index(row, column)
		DATASET = (model.data(index, Qt.DisplayRole).toString())

		column = 2
		model = self.table.model()
		index = model.index(row, column)
		GROUP = (model.data(index, Qt.DisplayRole).toString())

		column = 3
		model = self.table.model()
		index = model.index(row, column)
		SEQ = (model.data(index, Qt.DisplayRole).toString())

		column = 4
		model = self.table.model()
		index = model.index(row, column)
		FRAMES = int(model.data(index, Qt.DisplayRole).toString())

		column = 5
		model = self.table.model()
		index = model.index(row, column)
		E_num = int(model.data(index, Qt.DisplayRole).toString())

		column = 6
		model = self.table.model()
		index = model.index(row, column)
		T_num = int(model.data(index, Qt.DisplayRole).toString())

		self.Nanowell_Selected_Tag = Nanowell_Tag()
		self.Nanowell_Selected_Tag.DATASET = DATASET
		self.Nanowell_Selected_Tag.GROUP = GROUP
		self.Nanowell_Selected_Tag.GLOBAL_SEQ = GLOBAL_SEQ
		self.Nanowell_Selected_Tag.SEQ = SEQ
		self.Nanowell_Selected_Tag.FRAMES = FRAMES
		self.Nanowell_Selected_Tag.E_num = E_num
		self.Nanowell_Selected_Tag.T_num = T_num

		self.object_selected = row
		self.emit(SIGNAL("Nanowell_Table_Selection"), self.Tag, self.Nanowell_Selected_Tag)


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

	def arrayData(self):
		return self.arraydata

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

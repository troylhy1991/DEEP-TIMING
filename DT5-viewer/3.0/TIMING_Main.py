import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

helper_path1 = "./helper/"
sys.path.append(os.path.abspath(helper_path1))
from TIMING_Profiler_Processor import *

from TIMING_Profiler import *
from TIMING_Nanowell import *

class Dataset_Info():
	def __init__(self):
		self.name = 'Dataset ID'
		self.path = ''
		self.blocks = 0
		self.snapshots = 0
		self.DInt = 0
		self.EDInt = 0
		self.ContInt = 0
		self.TimInt = 0
		self.Pix = 0

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


class Dataset_Query(QWidget):
	def __init__(self):
		super(Dataset_Query, self).__init__()

		self.label0 = QLabel("Dataset ID    :")
		self.label1 = QLabel("# of Blocks   :")
		self.label2 = QLabel("# of SnapShots:")
		self.label3 = QLabel("DInt          :")
		self.label3_E = QLabel("EDInt         :")
		self.label4 = QLabel("ContInt       :")
		self.label5 = QLabel("TimInt        :")
		self.label6 = QLabel("Micros per Pix:")

		self.textbox0 = QLineEdit(self)
		self.textbox1 = QLineEdit(self)
		self.textbox2 = QLineEdit(self)
		self.textbox3 = QLineEdit(self)
		self.textbox3_E = QLineEdit(self)
		self.textbox4 = QLineEdit(self)
		self.textbox5 = QLineEdit(self)
		self.textbox6 = QLineEdit(self)

		self.textbox0.setText("20160211_GR_01_CARTAR_M")
		self.textbox1.setText("130")
		self.textbox2.setText("72")
		self.textbox3.setText("125")
		self.textbox3_E.setText("125")
		self.textbox4.setText("0.01")
		self.textbox5.setText("5")
		self.textbox6.setText("0.325")

		self.button = QPushButton('Set',self)
		self.button.clicked.connect(self.on_click_slot)

		HLayoutBox0 = QHBoxLayout()
		HLayoutBox0.addWidget(self.label0)
		HLayoutBox0.addWidget(self.textbox0)


		HLayoutBox1 = QHBoxLayout()
		HLayoutBox1.addWidget(self.label1)
		HLayoutBox1.addWidget(self.textbox1)

		HLayoutBox2 = QHBoxLayout()
		HLayoutBox2.addWidget(self.label2)
		HLayoutBox2.addWidget(self.textbox2)

		HLayoutBox3 = QHBoxLayout()
		HLayoutBox3.addWidget(self.label3)
		HLayoutBox3.addWidget(self.textbox3)

		HLayoutBox3_E = QHBoxLayout()
		HLayoutBox3_E.addWidget(self.label3_E)
		HLayoutBox3_E.addWidget(self.textbox3_E)

		HLayoutBox4 = QHBoxLayout()
		HLayoutBox4.addWidget(self.label4)
		HLayoutBox4.addWidget(self.textbox4)

		HLayoutBox5 = QHBoxLayout()
		HLayoutBox5.addWidget(self.label5)
		HLayoutBox5.addWidget(self.textbox5)

		HLayoutBox6 = QHBoxLayout()
		HLayoutBox6.addWidget(self.label6)
		HLayoutBox6.addWidget(self.textbox6)

		VLayoutBox = QVBoxLayout()
		VLayoutBox.addLayout(HLayoutBox0)
		VLayoutBox.addLayout(HLayoutBox1)
		VLayoutBox.addLayout(HLayoutBox2)
		VLayoutBox.addLayout(HLayoutBox3)
		VLayoutBox.addLayout(HLayoutBox3_E)
		VLayoutBox.addLayout(HLayoutBox4)
		VLayoutBox.addLayout(HLayoutBox5)
		VLayoutBox.addLayout(HLayoutBox6)

		VLayoutBox.addWidget(self.button)
		self.setLayout(VLayoutBox)
		self.resize(300,500)

		self.show()


	def on_click_slot(self):
		dataset_ID = self.textbox0.text()
		blocks = int(self.textbox1.text())
		snapshots = int(self.textbox2.text())
		DInt = float(self.textbox3.text())
		EDInt = float(self.textbox3_E.text())
		ContInt = float(self.textbox4.text())
		TimInt = int(self.textbox5.text())
		Pix = float(self.textbox6.text())

		self.emit(SIGNAL("Dataset_Configure_Done"),blocks,snapshots,DInt,EDInt,ContInt,TimInt,Pix,dataset_ID)



class TPS(QMainWindow):
	def __init__(self):
		super(TPS, self).__init__()

		self.dataset = Dataset_Info()
		self.Tag = Nanowell_Tag()

		# File Menu
		exit_action = QAction(QIcon('exit.png'), '&Exit', self)
		exit_action.setShortcut('Ctrl+Q')
		exit_action.setStatusTip('Exit application')
		exit_action.triggered.connect(qApp.quit)

		config_action = QAction('&Configure', self)
		config_action.triggered.connect(self.config_func)

		profile_action = QAction('&Profiler', self)
		profile_action.triggered.connect(self.profile_func)

		menu_bar = self.menuBar()
		file_menu = menu_bar.addMenu('&File')
		file_menu.addAction(config_action)
		file_menu.addAction(profile_action)
		file_menu.addAction(exit_action)

		# About Menu
		about_action = QAction('&About', self)
		about_action.triggered.connect(self.about_func)

		help_menu = menu_bar.addMenu('&Help')
		help_menu.addAction(about_action)


		# Main Window Show
		self.move(300,150)
		self.resize(400,20)
		self.setWindowTitle('TIMING 2 Viewer')
		self.show()

	def config_func(self):
		self.Query = Dataset_Query()
		self.connect(self.Query,SIGNAL("Dataset_Configure_Done"),self.config_func_slot)


	def config_func_slot(self, blocks, snapshots, DInt, EDInt, ContInt, TimInt, Pix, dataset_ID):

		self.dataset.blocks = blocks
		self.dataset.snapshots = snapshots
		self.dataset.DInt = DInt
		self.dataset.EDInt = EDInt
		self.dataset.ContInt = ContInt
		self.dataset.TimInt = TimInt
		self.dataset.Pix = Pix
		self.dataset.name = dataset_ID

		self.Tag.dataset = dataset_ID
		self.Tag.TimInt = TimInt
		self.Tag.DInt = DInt
		self.Tag.EDInt = EDInt


		self.dataset.path = str(QFileDialog.getExistingDirectory(self,"Select Directory"))
		self.dataset.path = self.dataset.path + "/"

		self.Query.deleteLater()

	def profile_func(self):
		TIMING_Profiler_Processor(self.dataset.path, self.dataset.DInt, self.dataset.EDInt, self.dataset.ContInt, self.dataset.TimInt, self.dataset.Pix)
		self.Profiler = TIMING_Profiler(self.dataset, self.Tag)
		self.connect(self.Profiler,SIGNAL("Nanowell_Table_Selection"),self.nanowell_click_slot)

	def nanowell_click_slot(self,path,tag):
		temp_tag = Nanowell_Tag()
		BID = tag.BID
		row = tag.R
		col = tag.C

		temp_tag.dataset = tag.dataset
		temp_tag.BID = tag.BID
		temp_tag.R = tag.R
		temp_tag.C = tag.C
		temp_tag.E_Num = tag.E_Num
		temp_tag.T_Num = tag.T_Num
		temp_tag.tSeek1 = tag.tSeek1
		temp_tag.TimInt = tag.TimInt
		temp_tag.DInt = tag.DInt
		temp_tag.EDInt = tag.EDInt

		try:
			self.Nanowell.deleteLater()
		except:
			print "No Nanowell Exist!"

		well_ID = (row-1)*6+col
		self.Nanowell = TIMING_Nanowell(path, BID, well_ID, 1, self.dataset.snapshots, temp_tag)




	def about_func(self):
		QMessageBox.information(self,"About","Version: TIMING 2 Viewer \n Author: Hengyang Lu \n Email: hlu9@uh.edu \n Copy Rights Reserved.")


def main():
	App = QApplication(sys.argv)
	TPS1 = TPS()
	sys.exit(App.exec_())

if __name__ == '__main__':
	main()

import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

helper_path = "./helper/"
sys.path.append(os.path.abspath(helper_path))

#from TIMING_sliderWindow import *

from sliderWidget import *

from TIMING_radarMap import *
from TIMING_TSPlot import *

from functools import partial


class Nanowell_Tag0():
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


class Dataset_Tag1():
    '''
    A Dataset Tag will be created anytime a dataset is loaded
    '''
    def __init__(self):
        self.path = ''
        self.dataset = 'Dataset ID'
        self.blocks = 30
        self.block_list = []
        self.frames = 72

class Nanowell_Tag1():
    '''
    A Nanowell Tag instance is created anytime a nanowell is clicked.
    And the Nanowell Tag will be passed to the slider widget
    '''
    def __init__(self):
        self.BID = 1
        self.Nanowell_ID = 1
        self.E_num = 0
        self.T_num = 0



class TIMING_Feature_Board(QMainWindow):
	def __init__(self, path, BID, Well_ID, E, T, tag, t = 1, t_span =80):
		super(TIMING_Feature_Board, self).__init__()

		self.path = path
		self.BID = BID
		self.Well_ID = Well_ID

		self.E = E
		self.T = T

		self.t = t
		self.t_span = t_span

		self.Tag = Nanowell_Tag()
		self.Tag.BID = tag.BID
		self.Tag.R = tag.R
		self.Tag.C = tag.C
		self.Tag.E_Num = tag.E_Num
		self.Tag.T_Num = tag.T_Num
		self.Tag.tSeek1 = tag.tSeek1
		self.Tag.TimInt = tag.TimInt
		self.Tag.DInt = tag.DInt
		self.Tag.EDInt = tag.EDInt

		self.nanowell_tag1 = Nanowell_Tag1()
		self.nanowell_tag1.BID = tag.BID
		self.nanowell_tag1.Nanowell_ID = Well_ID
		self.nanowell_tag1.E_num = E
		self.nanowell_tag1.T_num = T

		self.dataset_tag1 = Dataset_Tag1()
		self.dataset_tag1.path = path
		self.dataset_tag1.frames = t_span



		# Menu Bar set-up
		menubar = self.menuBar()
		panelMenu = menubar.addMenu('&Panel')

		panel1Menu = panelMenu.addMenu('&Slider Window')
		panel2Menu = panelMenu.addMenu('&Radar Map')
		panel3Menu = panelMenu.addMenu('&Time Series L')
		panel4Menu = panelMenu.addMenu('&Time Series R')

		centroidAction = QAction('&Show Centroids',self)
		IDAction = QAction('&Show ID', self)

		centroidAction.setCheckable(True)
		IDAction.setCheckable(True)

		panel1Menu.addAction(centroidAction)
		panel1Menu.addAction(IDAction)

		cellMenuL = panel3Menu.addMenu('&Select Cells')
		featMenuL = panel3Menu.addMenu('&Select Features')

		cellMenuR = panel4Menu.addMenu('&Select Cells')
		featMenuR = panel4Menu.addMenu('&Select Features')


		#L
		self.E1ActionL= QAction('&E1',self)
		self.E2ActionL= QAction('&E2',self)
		self.E3ActionL= QAction('&E3',self)
		self.E4ActionL= QAction('&E4',self)

		self.T1ActionL = QAction('&T1',self)
		self.T2ActionL = QAction('&T2',self)
		self.T3ActionL = QAction('&T3',self)
		self.T4ActionL = QAction('&T4',self)

		self.E1ActionL.setCheckable(True)
		self.E2ActionL.setCheckable(True)
		self.E3ActionL.setCheckable(True)
		self.E4ActionL.setCheckable(True)
		self.T1ActionL.setCheckable(True)
		self.T2ActionL.setCheckable(True)
		self.T3ActionL.setCheckable(True)
		self.T4ActionL.setCheckable(True)

		cellMenuL.addAction(self.E1ActionL)
		cellMenuL.addAction(self.E2ActionL)
		cellMenuL.addAction(self.E3ActionL)
		cellMenuL.addAction(self.E4ActionL)
		cellMenuL.addAction(self.T1ActionL)
		cellMenuL.addAction(self.T2ActionL)
		cellMenuL.addAction(self.T3ActionL)
		cellMenuL.addAction(self.T4ActionL)

		self.AR_ActionL = QAction('&Aspect Ratio',self)
		self.speed_ActionL = QAction('&Speed',self)
		self.DM_ActionL = QAction('&Death Marker',self)
		self.CR_ActionL = QAction('&Contact Ratio',self)

		self.AR_ActionL.setCheckable(True)
		self.speed_ActionL.setCheckable(True)
		self.DM_ActionL.setCheckable(True)
		self.CR_ActionL.setCheckable(True)

		featMenuL.addAction(self.AR_ActionL)
		featMenuL.addAction(self.speed_ActionL)
		featMenuL.addAction(self.DM_ActionL)
		featMenuL.addAction(self.CR_ActionL)



		#R
		self.E1ActionR= QAction('&E1',self)
		self.E2ActionR= QAction('&E2',self)
		self.E3ActionR= QAction('&E3',self)
		self.E4ActionR= QAction('&E4',self)

		self.T1ActionR = QAction('&T1',self)
		self.T2ActionR = QAction('&T2',self)
		self.T3ActionR = QAction('&T3',self)
		self.T4ActionR = QAction('&T4',self)

		self.E1ActionR.setCheckable(True)
		self.E2ActionR.setCheckable(True)
		self.E3ActionR.setCheckable(True)
		self.E4ActionR.setCheckable(True)
		self.T1ActionR.setCheckable(True)
		self.T2ActionR.setCheckable(True)
		self.T3ActionR.setCheckable(True)
		self.T4ActionR.setCheckable(True)

		cellMenuR.addAction(self.E1ActionR)
		cellMenuR.addAction(self.E2ActionR)
		cellMenuR.addAction(self.E3ActionR)
		cellMenuR.addAction(self.E4ActionR)
		cellMenuR.addAction(self.T1ActionR)
		cellMenuR.addAction(self.T2ActionR)
		cellMenuR.addAction(self.T3ActionR)
		cellMenuR.addAction(self.T4ActionR)

		self.AR_ActionR = QAction('&Aspect Ratio',self)
		self.speed_ActionR = QAction('&Speed',self)
		self.DM_ActionR = QAction('&Death Marker',self)
		self.CR_ActionR = QAction('&Contact Ratio',self)

		self.AR_ActionR.setCheckable(True)
		self.speed_ActionR.setCheckable(True)
		self.DM_ActionR.setCheckable(True)
		self.CR_ActionR.setCheckable(True)

		featMenuR.addAction(self.AR_ActionR)
		featMenuR.addAction(self.speed_ActionR)
		featMenuR.addAction(self.DM_ActionR)
		featMenuR.addAction(self.CR_ActionR)



		# self.S1 = sliderWindow(self.path, self.BID, self.Well_ID, self.t_span, self.E, self.T, self.Tag)
		self.S1 = sliderWidget(self.dataset_tag1, self.nanowell_tag1)


		self.S2 = radarMap(self.E, self.T, self.t_span)

		self.S1.slider.valueChanged[int].connect(self.S2.update_main_frame)

		self.S3 = TSPlot(self.E,self.T,[1,0,0,0,0,0,0,0],[0,0,0,0,1,0],self.Tag.tSeek1,self.Tag.DInt,self.Tag.EDInt,self.t_span)

		self.S4 = TSPlot(self.E,self.T,[0,0,0,0,1,0,0,0],[0,0,0,0,1,0],self.Tag.tSeek1,self.Tag.DInt,self.Tag.EDInt,self.t_span)

		#self.S3 = ApplicationWindow()

		HBox = QHBoxLayout()
		HBox.addWidget(self.S1)
		HBox.addWidget(self.S2)

		HBox2 = QHBoxLayout()
		HBox2.addWidget(self.S3)
		HBox2.addWidget(self.S4)


		VBox = QVBoxLayout()
		VBox.addLayout(HBox)
		VBox.addLayout(HBox2)



		window = QWidget()
		window.setLayout(VBox)
		self.setCentralWidget(window)

		self.setWindowTitle("TIMING 2 Feature Board")

		self.build_links()

		self.show()

	def build_links(self):
		#L
		self.E1ActionL.triggered.connect(self.E1_Func_L)
		self.E1ActionL.triggered.connect(self.S3.update_main_frame)

		self.E2ActionL.triggered.connect(self.E2_Func_L)
		self.E2ActionL.triggered.connect(self.S3.update_main_frame)

		self.E3ActionL.triggered.connect(self.E3_Func_L)
		self.E3ActionL.triggered.connect(self.S3.update_main_frame)

		self.E4ActionL.triggered.connect(self.E4_Func_L)
		self.E4ActionL.triggered.connect(self.S3.update_main_frame)

		self.T1ActionL.triggered.connect(self.T1_Func_L)
		self.T1ActionL.triggered.connect(self.S3.update_main_frame)

		self.T2ActionL.triggered.connect(self.T2_Func_L)
		self.T2ActionL.triggered.connect(self.S3.update_main_frame)

		self.T3ActionL.triggered.connect(self.T3_Func_L)
		self.T3ActionL.triggered.connect(self.S3.update_main_frame)

		self.T4ActionL.triggered.connect(self.T4_Func_L)
		self.T4ActionL.triggered.connect(self.S3.update_main_frame)

		#R
		self.E1ActionR.triggered.connect(self.E1_Func_R)
		self.E1ActionR.triggered.connect(self.S4.update_main_frame)

		self.E2ActionR.triggered.connect(self.E2_Func_R)
		self.E2ActionR.triggered.connect(self.S4.update_main_frame)

		self.E3ActionR.triggered.connect(self.E3_Func_R)
		self.E3ActionR.triggered.connect(self.S4.update_main_frame)

		self.E4ActionR.triggered.connect(self.E4_Func_R)
		self.E4ActionR.triggered.connect(self.S4.update_main_frame)

		self.T1ActionR.triggered.connect(self.T1_Func_R)
		self.T1ActionR.triggered.connect(self.S4.update_main_frame)

		self.T2ActionR.triggered.connect(self.T2_Func_R)
		self.T2ActionR.triggered.connect(self.S4.update_main_frame)

		self.T3ActionR.triggered.connect(self.T3_Func_R)
		self.T3ActionR.triggered.connect(self.S4.update_main_frame)

		self.T4ActionR.triggered.connect(self.T4_Func_R)
		self.T4ActionR.triggered.connect(self.S4.update_main_frame)


		#L Features
		self.AR_ActionL.triggered.connect(self.AR_Func_L)
		self.AR_ActionL.triggered.connect(self.S3.update_main_frame)

		self.speed_ActionL.triggered.connect(self.speed_Func_L)
		self.speed_ActionL.triggered.connect(self.S3.update_main_frame)

		self.DM_ActionL.triggered.connect(self.DM_Func_L)
		self.DM_ActionL.triggered.connect(self.S3.update_main_frame)

		self.CR_ActionL.triggered.connect(self.CR_Func_L)
		self.CR_ActionL.triggered.connect(self.S3.update_main_frame)

		#R Features
		self.AR_ActionR.triggered.connect(self.AR_Func_R)
		self.AR_ActionR.triggered.connect(self.S4.update_main_frame)

		self.speed_ActionR.triggered.connect(self.speed_Func_R)
		self.speed_ActionR.triggered.connect(self.S4.update_main_frame)

		self.DM_ActionR.triggered.connect(self.DM_Func_R)
		self.DM_ActionR.triggered.connect(self.S4.update_main_frame)

		self.CR_ActionR.triggered.connect(self.CR_Func_R)
		self.CR_ActionR.triggered.connect(self.S4.update_main_frame)

	#R
	def E1_Func_L(self):
		self.E1ActionL.setChecked(True)
		self.E2ActionL.setChecked(False)
		self.E3ActionL.setChecked(False)
		self.E4ActionL.setChecked(False)
		self.T1ActionL.setChecked(False)
		self.T2ActionL.setChecked(False)
		self.T3ActionL.setChecked(False)
		self.T4ActionL.setChecked(False)

		self.S3.cell_flag = [1,0,0,0,0,0,0,0]

	def E2_Func_L(self):
		self.E1ActionL.setChecked(False)
		self.E2ActionL.setChecked(True)
		self.E3ActionL.setChecked(False)
		self.E4ActionL.setChecked(False)
		self.T1ActionL.setChecked(False)
		self.T2ActionL.setChecked(False)
		self.T3ActionL.setChecked(False)
		self.T4ActionL.setChecked(False)

		self.S3.cell_flag = [0,1,0,0,0,0,0,0]

	def E3_Func_L(self):
		self.E1ActionL.setChecked(False)
		self.E2ActionL.setChecked(False)
		self.E3ActionL.setChecked(True)
		self.E4ActionL.setChecked(False)
		self.T1ActionL.setChecked(False)
		self.T2ActionL.setChecked(False)
		self.T3ActionL.setChecked(False)
		self.T4ActionL.setChecked(False)

		self.S3.cell_flag = [0,0,1,0,0,0,0,0]

	def E4_Func_L(self):
		self.E1ActionL.setChecked(False)
		self.E2ActionL.setChecked(False)
		self.E3ActionL.setChecked(False)
		self.E4ActionL.setChecked(True)
		self.T1ActionL.setChecked(False)
		self.T2ActionL.setChecked(False)
		self.T3ActionL.setChecked(False)
		self.T4ActionL.setChecked(False)

		self.S3.cell_flag = [0,0,0,1,0,0,0,0]


	def T1_Func_L(self):
		self.E1ActionL.setChecked(False)
		self.E2ActionL.setChecked(False)
		self.E3ActionL.setChecked(False)
		self.E4ActionL.setChecked(False)
		self.T1ActionL.setChecked(True)
		self.T2ActionL.setChecked(False)
		self.T3ActionL.setChecked(False)
		self.T4ActionL.setChecked(False)

		self.S3.cell_flag = [0,0,0,0,1,0,0,0]

	def T2_Func_L(self):
		self.E1ActionL.setChecked(False)
		self.E2ActionL.setChecked(False)
		self.E3ActionL.setChecked(False)
		self.E4ActionL.setChecked(False)
		self.T1ActionL.setChecked(False)
		self.T2ActionL.setChecked(True)
		self.T3ActionL.setChecked(False)
		self.T4ActionL.setChecked(False)

		self.S3.cell_flag = [0,0,0,0,0,1,0,0]

	def T3_Func_L(self):
		self.E1ActionL.setChecked(False)
		self.E2ActionL.setChecked(False)
		self.E3ActionL.setChecked(False)
		self.E4ActionL.setChecked(False)
		self.T1ActionL.setChecked(False)
		self.T2ActionL.setChecked(False)
		self.T3ActionL.setChecked(True)
		self.T4ActionL.setChecked(False)

		self.S3.cell_flag = [0,0,0,0,0,0,1,0]

	def T4_Func_L(self):
		self.E1ActionL.setChecked(False)
		self.E2ActionL.setChecked(False)
		self.E3ActionL.setChecked(False)
		self.E4ActionL.setChecked(False)
		self.T1ActionL.setChecked(False)
		self.T2ActionL.setChecked(False)
		self.T3ActionL.setChecked(False)
		self.T4ActionL.setChecked(True)

		self.S3.cell_flag = [0,0,0,0,0,0,0,1]




	def E1_Func_R(self):
		self.E1ActionR.setChecked(True)
		self.E2ActionR.setChecked(False)
		self.E3ActionR.setChecked(False)
		self.E4ActionR.setChecked(False)
		self.T1ActionR.setChecked(False)
		self.T2ActionR.setChecked(False)
		self.T3ActionR.setChecked(False)
		self.T4ActionR.setChecked(False)

		self.S4.cell_flag = [1,0,0,0,0,0,0,0]

	def E2_Func_R(self):
		self.E1ActionR.setChecked(False)
		self.E2ActionR.setChecked(True)
		self.E3ActionR.setChecked(False)
		self.E4ActionR.setChecked(False)
		self.T1ActionR.setChecked(False)
		self.T2ActionR.setChecked(False)
		self.T3ActionR.setChecked(False)
		self.T4ActionR.setChecked(False)

		self.S4.cell_flag = [0,1,0,0,0,0,0,0]

	def E3_Func_R(self):
		self.E1ActionR.setChecked(False)
		self.E2ActionR.setChecked(False)
		self.E3ActionR.setChecked(True)
		self.E4ActionR.setChecked(False)
		self.T1ActionR.setChecked(False)
		self.T2ActionR.setChecked(False)
		self.T3ActionR.setChecked(False)
		self.T4ActionR.setChecked(False)

		self.S4.cell_flag = [0,0,1,0,0,0,0,0]

	def E4_Func_R(self):
		self.E1ActionR.setChecked(False)
		self.E2ActionR.setChecked(False)
		self.E3ActionR.setChecked(False)
		self.E4ActionR.setChecked(True)
		self.T1ActionR.setChecked(False)
		self.T2ActionR.setChecked(False)
		self.T3ActionR.setChecked(False)
		self.T4ActionR.setChecked(False)

		self.S4.cell_flag = [0,0,0,1,0,0,0,0]


	def T1_Func_R(self):
		self.E1ActionR.setChecked(False)
		self.E2ActionR.setChecked(False)
		self.E3ActionR.setChecked(False)
		self.E4ActionR.setChecked(False)
		self.T1ActionR.setChecked(True)
		self.T2ActionR.setChecked(False)
		self.T3ActionR.setChecked(False)
		self.T4ActionR.setChecked(False)

		self.S4.cell_flag = [0,0,0,0,1,0,0,0]

	def T2_Func_R(self):
		self.E1ActionR.setChecked(False)
		self.E2ActionR.setChecked(False)
		self.E3ActionR.setChecked(False)
		self.E4ActionR.setChecked(False)
		self.T1ActionR.setChecked(False)
		self.T2ActionR.setChecked(True)
		self.T3ActionR.setChecked(False)
		self.T4ActionR.setChecked(False)

		self.S4.cell_flag = [0,0,0,0,0,1,0,0]

	def T3_Func_R(self):
		self.E1ActionR.setChecked(False)
		self.E2ActionR.setChecked(False)
		self.E3ActionR.setChecked(False)
		self.E4ActionR.setChecked(False)
		self.T1ActionR.setChecked(False)
		self.T2ActionR.setChecked(False)
		self.T3ActionR.setChecked(True)
		self.T4ActionR.setChecked(False)

		self.S4.cell_flag = [0,0,0,0,0,0,1,0]

	def T4_Func_R(self):
		self.E1ActionR.setChecked(False)
		self.E2ActionR.setChecked(False)
		self.E3ActionR.setChecked(False)
		self.E4ActionR.setChecked(False)
		self.T1ActionR.setChecked(False)
		self.T2ActionR.setChecked(False)
		self.T3ActionR.setChecked(False)
		self.T4ActionR.setChecked(True)

		self.S4.cell_flag = [0,0,0,0,0,0,0,1]



	def AR_Func_L(self):
		self.AR_ActionL.setChecked(True)
		self.speed_ActionL.setChecked(False)
		self.DM_ActionL.setChecked(False)
		self.CR_ActionL.setChecked(False)

		self.S3.feat_flag = [0,0,1,0,0,0]


	def speed_Func_L(self):
		self.AR_ActionL.setChecked(False)
		self.speed_ActionL.setChecked(True)
		self.DM_ActionL.setChecked(False)
		self.CR_ActionL.setChecked(False)

		self.S3.feat_flag = [0,0,0,1,0,0]

	def DM_Func_L(self):
		self.AR_ActionL.setChecked(False)
		self.speed_ActionL.setChecked(False)
		self.DM_ActionL.setChecked(True)
		self.CR_ActionL.setChecked(False)

		self.S3.feat_flag = [0,0,0,0,1,0]

	def CR_Func_L(self):
		self.AR_ActionL.setChecked(False)
		self.speed_ActionL.setChecked(False)
		self.DM_ActionL.setChecked(False)
		self.CR_ActionL.setChecked(True)

		self.S3.feat_flag = [0,0,0,0,0,1]


	def AR_Func_R(self):
		self.AR_ActionR.setChecked(True)
		self.speed_ActionR.setChecked(False)
		self.DM_ActionR.setChecked(False)
		self.CR_ActionR.setChecked(False)

		self.S4.feat_flag = [0,0,1,0,0,0]


	def speed_Func_R(self):
		self.AR_ActionR.setChecked(False)
		self.speed_ActionR.setChecked(True)
		self.DM_ActionR.setChecked(False)
		self.CR_ActionR.setChecked(False)

		self.S4.feat_flag = [0,0,0,1,0,0]

	def DM_Func_R(self):
		self.AR_ActionR.setChecked(False)
		self.speed_ActionR.setChecked(False)
		self.DM_ActionR.setChecked(True)
		self.CR_ActionR.setChecked(False)

		self.S4.feat_flag = [0,0,0,0,1,0]


	def CR_Func_R(self):
		self.AR_ActionR.setChecked(False)
		self.speed_ActionR.setChecked(False)
		self.DM_ActionR.setChecked(False)
		self.CR_ActionR.setChecked(True)

		self.S4.feat_flag = [0,0,0,0,0,1]


def main():
	app = QApplication(sys.argv)
	ex = TIMING_featureBoard()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()

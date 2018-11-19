import os
import sys
import copy

import SimpleITK as sitk
import numpy as np

from skimage import io

from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from TIMING_Feature_Board import *

helper_path = "./helper/"
sys.path.append(os.path.abspath(helper_path))
import TIMING_QImageConverter as QC

tracker_path = "./timing2-tracker/"
sys.path.append(os.path.abspath(tracker_path))
from cell_tracker import TIMING_Cell_Tracker

feature_path = "./timing2-features/"
sys.path.append(os.path.abspath(feature_path))
from feature_worker import generate_cell_pool


class Quick_Seg_Fix(QWidget):
	def __init__(self):
		super(Quick_Seg_Fix, self).__init__()
		
		self.label1 = QLabel("# of Effectors    :")
		self.textbox1 = QLineEdit(self)
		HBox1 = QHBoxLayout()
		HBox1.addWidget(self.label1)
		HBox1.addWidget(self.textbox1)
		
		self.label2 = QLabel("Snapshots to ReSegment:")
		self.textbox2 = QLineEdit(self)
		HBox2 = QHBoxLayout()
		HBox2.addWidget(self.label2)
		HBox2.addWidget(self.textbox2)
		
		self.button1 = QPushButton('Resegment Effector',self)
		self.button1.clicked.connect(self.E_ReSeG_func)
		
		self.label3 = QLabel("# of Targets      :")
		self.textbox3 = QLineEdit(self)
		HBox3 = QHBoxLayout()
		HBox3.addWidget(self.label3)
		HBox3.addWidget(self.textbox3)
		
		self.label4 = QLabel("Snapshots to ReSegment:")
		self.textbox4 = QLineEdit(self)
		HBox4 = QHBoxLayout()
		HBox4.addWidget(self.label4)
		HBox4.addWidget(self.textbox4)
		
		self.button2 = QPushButton('Resegment Target', self)
		self.button2.clicked.connect(self.T_ReSeG_func)
		
		VBox = QVBoxLayout()
		VBox.addLayout(HBox1)
		VBox.addLayout(HBox2)
		VBox.addWidget(self.button1)
		VBox.addLayout(HBox3)
		VBox.addLayout(HBox4)
		VBox.addWidget(self.button2)	

		self.setWindowTitle("Quick ReSegment")
		self.setFixedSize(300,500)
		self.setLayout(VBox)
		
	def frame_parse(self, ET):
		if ET == 'E':
			frames = []
			temp_string = str(self.textbox2.text())
			temp = temp_string.strip('\n').split(',')
			for item in temp:
				if ':' in item:
					xy = item.split(':')
					x = int(xy[0])
					y = int(xy[1])
					for i in range(x,y+1):
						if i not in frames:
							frames.append(i)
				else:
					frames.append(int(item))
					
		if ET == 'T':
			frames = []
			temp_string = str(self.textbox4.text())
			temp = temp_string.strip('\n').split(',')
			for item in temp:
				if ':' in item:
					xy = item.split(':')
					x = int(xy[0])
					y = int(xy[1])
					for i in range(x,y+1):
						if i not in frames:
							frames.append(i)
				else:
					frames.append(int(item))
		
		return frames
		
	def E_ReSeG_func(self):
	
		CH = 'E'
		k = int(self.textbox1.text())
		frames = self.frame_parse('E')
		
		self.emit(SIGNAL('ReSeG_Effector_Channel'),CH,k,frames)
	
	
	def T_ReSeG_func(self):

		CH = 'T'
		k = int(self.textbox3.text())
		frames = self.frame_parse('T')
		
		self.emit(SIGNAL('ReSeG_Target_Channel'),CH,k,frames)
		
class Quick_Tracker_Fix(QWidget):
	def __init__(self):
		super(Quick_Tracker_Fix, self).__init__()
		
		self.label1 = QLabel("Effector Switch Pair  :")
		self.textbox1 = QLineEdit()
		HBox1 = QHBoxLayout()
		HBox1.addWidget(self.label1)
		HBox1.addWidget(self.textbox1)
		
		self.label2 = QLabel("Frames to Switch      :")
		self.textbox2 = QLineEdit()
		HBox2 = QHBoxLayout()
		HBox2.addWidget(self.label2)
		HBox2.addWidget(self.textbox2)
		
		self.button1 = QPushButton("Switch Effectors")
		self.button1.clicked.connect(self.switch_effector_slot)
		
		self.label3 = QLabel("Target Switch Pair    :")
		self.textbox3 = QLineEdit()
		HBox3 = QHBoxLayout()
		HBox3.addWidget(self.label3)
		HBox3.addWidget(self.textbox3)
		
		self.label4 = QLabel("Frames to Switch      :")
		self.textbox4 = QLineEdit()
		HBox4 = QHBoxLayout()
		HBox4.addWidget(self.label4)
		HBox4.addWidget(self.textbox4)
		
		self.button2 = QPushButton("Switch Targets")
		self.button2.clicked.connect(self.switch_target_slot)

		VBox = QVBoxLayout()
		VBox.addLayout(HBox1)
		VBox.addLayout(HBox2)
		VBox.addWidget(self.button1)
		VBox.addLayout(HBox3)
		VBox.addLayout(HBox4)
		VBox.addWidget(self.button2)	

		self.setWindowTitle("Quick Switch")
		self.setFixedSize(300,500)
		self.setLayout(VBox)
		
	def frame_parse(self, ET):
		if ET == 'E':
			frames = []
			temp_string = str(self.textbox2.text())
			temp = temp_string.strip('\n').split(',')
			for item in temp:
				if ':' in item:
					xy = item.split(':')
					x = int(xy[0])
					y = int(xy[1])
					for i in range(x,y+1):
						if i not in frames:
							frames.append(i)
				else:
					frames.append(int(item))
					
		if ET == 'T':
			frames = []
			temp_string = str(self.textbox4.text())
			temp = temp_string.strip('\n').split(',')
			for item in temp:
				if ':' in item:
					xy = item.split(':')
					x = int(xy[0])
					y = int(xy[1])
					for i in range(x,y+1):
						if i not in frames:
							frames.append(i)
				else:
					frames.append(int(item))		
		
		return frames		
	
	def switch_effector_slot(self):
		
		CH = 'E'
		pair = self.textbox1.text()
		p1 = int(pair.split(',')[0])
		p2 = int(pair.split(',')[1])
		
		frames = self.frame_parse('E')
		
		self.emit(SIGNAL("SWITCH_EFFECTORS"), CH, p1, p2, frames)
	
	
	def switch_target_slot(self):
		CH = 'T'
		pair = self.textbox3.text()
		p1 = int(pair.split(',')[0])
		p2 = int(pair.split(',')[1])
		
		frames = self.frame_parse('T')
		
		self.emit(SIGNAL("SWITCH_TARGETS"), CH, p1, p2, frames)
		
		
class TIMING_Painter(QWidget):
	def __init__(self):
		super(TIMING_Painter, self).__init__()
		

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

		
class TIMING_ReEditBox(QMainWindow):
	def __init__(self, dataPath, BID, Well_ID, t, t_span, tag):
		super(TIMING_ReEditBox, self).__init__()
		
		self.path = dataPath
		self.BID = BID
		#self.row = row
		#self.col = col
		self.Well_ID = Well_ID
		self.t = t
		self.t_span = t_span
		
		self.Tag = Nanowell_Tag()
		self.Tag.dataset = tag.dataset
		self.Tag.BID = tag.BID
		self.Tag.R = tag.R
		self.Tag.C = tag.C
		self.Tag.E_Num = tag.E_Num
		self.Tag.T_Num = tag.T_Num
		self.Tag.tSeek1 = tag.tSeek1
		self.Tag.TimInt = tag.TimInt
		self.Tag.DInt = tag.DInt
		self.Tag.EDInt = tag.EDInt	
		

		self.Width = 281
		self.Height = 281
		
		self.CH0 = []
		self.CH1 = []
		self.CH2 = []
		self.CH3 = []
		self.CH1_label = []
		self.CH2_label = []
		
		self.CH0_dict = {}
		self.CH1_dict = {}
		self.CH2_dict = {}
		self.CH3_dict = {}
		self.CH1_label_dict = {}
		self.CH2_label_dict = {}
		
		self.CH1_label_edit = []
		self.CH2_label_edit = []
		
		self.CH1_label_dict_edit = {}
		self.CH2_label_dict_edit = {}
		
		self.edit_flags = np.zeros(t_span)
		self.mixing_mode_flag = 0
		self.label_image_2_flag = 0
		self.label_image_3_flag = 0
		
		self.Display_Flags = {'CH0': True, 'CH1': True, 'CH2': True, 'CH3': False, 'CH1_label': True, 'CH2_label': True}
		self.timer = QTimer()
		self.timer.timeout.connect(self.tick_timer)
		
		self.imageLabel = QLabel()
		self.scrollArea = QScrollArea()
		
		self.imageLabel_R1 = QLabel()
		self.scrollArea_R1 = QScrollArea()
		
		self.imageLabel_R2 = QLabel()
		self.scrollArea_R2 = QScrollArea()
		
		self.slider = QSlider(Qt.Horizontal)
		self.spinBox = QSpinBox()
		self.playButton = QPushButton()
		self.pauseButton = QPushButton()
		self.stopButton = QPushButton()
		self.starButton = QPushButton()
		self.progress = QProgressBar()		
		
		self.loadImages()
		self.setupUI()
		
	def setupUI(self):
		# Editing Menu
		Quick_Seg_Action = QAction('&Quick Resegment', self)
		Quick_Seg_Action.triggered.connect(self.quick_seg_fix_func)
		
		Quick_Track_Action = QAction('&Quick Switch', self)
		Quick_Track_Action.triggered.connect(self.quick_track_fix_func)
		
		Manual_Edit_Action = QAction('Manual Mode', self)
		Manual_Edit_Action.triggered.connect(self.manual_edit_func)
		
		Save_Action = QAction('Save', self)
		Save_Action.triggered.connect(self.save_edit_func)
		
		menu_bar = self.menuBar()
		edit_menu = menu_bar.addMenu('&Edit')
		edit_menu.addAction(Quick_Seg_Action)
		edit_menu.addAction(Quick_Track_Action)
		edit_menu.addAction(Manual_Edit_Action)
		edit_menu.addAction(Save_Action)
	
	
		self.imageLabel.setBackgroundRole(QPalette.Base)
		self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
		self.imageLabel.setMouseTracking(True)
		self.imageLabel.setScaledContents(True)	

		pic = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		pic.fill(qRgb(0,0,0))
		painter = QPainter(pic)
		painter.setCompositionMode(QPainter.CompositionMode_Plus)
		
		channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		channelImage.fill(qRgb(255,255,255))
		channelImage.setAlphaChannel(self.CH0)
		painter.drawImage(0,0,channelImage)
		
		channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		channelImage.fill(qRgb(255,0,0))
		channelImage.setAlphaChannel(self.CH1)
		painter.drawImage(0,0,channelImage)

		channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		channelImage.fill(qRgb(0,255,0))
		channelImage.setAlphaChannel(self.CH2)
		painter.drawImage(0,0,channelImage)

		if self.Display_Flags['CH0'] == True:
			pen = QPen(Qt.white)
		else:
			pen = QPen(Qt.cyan)
		painter.setPen(pen)
		if self.Display_Flags['CH1_label'] == True:
			for i in range(1,280):
				for j in range(1,280):
					v = self.CH1_label[i][j]
					if v >0:
						v1 = self.CH1_label[i][j+1]
						v2 = self.CH1_label[i+1][j]
						v3 = self.CH1_label[i][j-1]
						v4 = self.CH1_label[i-1][j]
						if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
							for k1 in range(-1,2):
								for k2 in range (-1,2):
									painter.drawPoint(j+k1,i+k2)
							
						
		if self.Display_Flags['CH0'] == True:
			pen = QPen(Qt.yellow)
		else:						
			pen.setColor(Qt.magenta)
		painter.setPen(pen)
		if self.Display_Flags['CH2_label'] == True:
			for i in range(1,280):
				for j in range(1,280):
					v = self.CH2_label[i][j]
					if v >0:
						v1 = self.CH2_label[i][j+1]
						v2 = self.CH2_label[i+1][j]
						v3 = self.CH2_label[i][j-1]
						v4 = self.CH2_label[i-1][j]
						if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
							for k1 in range(-1,2):
								for k2 in range (-1,2):
									painter.drawPoint(j+k1,i+k2)
		
		# paint some information
		#Time
		pen.setColor(Qt.white)
		painter.setPen(pen)
		font = QFont()
		font.setFamily('Lucida')
		font.setFixedPitch(True)
		font.setPointSize(15)
		font.setBold(True)
		painter.setFont(font)
		t = self.t
		TimInt = self.Tag.TimInt
		N = 60/TimInt
		hour = t/N
		minute = (t%N)*TimInt
		Time_str = 'TIME: ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00'
		painter.drawText(30,30,Time_str)
		
		#Legend
		pen.setColor(Qt.red)
		painter.setPen(pen)
		painter.setBrush(Qt.red)
		painter.drawEllipse(25,230,10,10)
		
		pen.setColor(Qt.green)
		painter.setPen(pen)
		painter.setBrush(Qt.green)
		painter.drawEllipse(25,250,10,10)
		
		pen.setColor(Qt.white)
		painter.setPen(pen)
		font = QFont()
		font.setFamily('Lucida')
		font.setFixedPitch(True)
		font.setPointSize(10)
		font.setBold(True)
		painter.setFont(font)
		
		painter.drawText(45,240,'Effector')
		painter.drawText(45,260,'Target')
		
		#scale
		mu = QChar(0x00b5)
		scale1 = '25 '
		scale2 = 'm'
		
		pen.setColor(Qt.white)
		painter.setPen(pen)
		painter.setBrush(Qt.white)
		painter.drawRect(170,230,75,5)
		
		pen.setColor(Qt.white)
		painter.setPen(pen)
		font = QFont()
		font.setFamily('Lucida')
		font.setFixedPitch(True)
		font.setPointSize(10)
		font.setBold(True)
		painter.setFont(font)
		
		painter.drawText(195,250,scale1)
		painter.drawText(215,250,mu)
		painter.drawText(225,250,scale2)
									
									
		del pen
		del painter
		
		self.imageLabel.setPixmap(QPixmap.fromImage(pic))
	
		self.scrollArea.setMouseTracking(True)
		self.scrollArea.setBackgroundRole(QPalette.Dark)
		self.scrollArea.setWidget(self.imageLabel)
		self.scrollArea.horizontalScrollBar().setRange(0,0)
		self.scrollArea.verticalScrollBar().setRange(0,0)
		self.scrollArea.horizontalScrollBar().setValue(0)
		self.scrollArea.verticalScrollBar().setValue(0)
		self.scrollArea.setFixedSize(284,284)

		
		self.imageLabel_R1.setBackgroundRole(QPalette.Base)
		self.imageLabel_R1.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
		self.imageLabel_R1.setMouseTracking(True)
		self.imageLabel_R1.setScaledContents(True)	

		pic2 = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		pic2.fill(qRgb(0,0,0))
		painter2 = QPainter(pic2)
		painter2.setCompositionMode(QPainter.CompositionMode_Plus)
		
		pen2 = QPen()
		for i in range(1,280):
			for j in range(1,280):
				v = self.CH1_label_edit[i][j]
				if v == 1:
					pen2.setColor(QColor(200,0,0))
					painter2.setPen(pen2)
					painter2.drawPoint(j,i)
				if v == 2:
					pen2.setColor(QColor(150,0,0))
					painter2.setPen(pen2)
					painter2.drawPoint(j,i)
				if v == 3:
					pen2.setColor(QColor(100,0,0))
					painter2.setPen(pen2)
					painter2.drawPoint(j,i)
				if v == 4:
					pen2.setColor(QColor(50,0,0))
					painter2.setPen(pen2)
					painter2.drawPoint(j,i)
		del pen2
		del painter2
		
		self.imageLabel_R1.setPixmap(QPixmap.fromImage(pic2))
		
		self.scrollArea_R1.setMouseTracking(True)
		self.scrollArea_R1.setBackgroundRole(QPalette.Dark)
		self.scrollArea_R1.setWidget(self.imageLabel_R1)
		self.scrollArea_R1.horizontalScrollBar().setRange(0,0)
		self.scrollArea_R1.verticalScrollBar().setRange(0,0)
		self.scrollArea_R1.horizontalScrollBar().setValue(0)
		self.scrollArea_R1.verticalScrollBar().setValue(0)
		self.scrollArea_R1.setFixedSize(284,284)
	
		self.imageLabel_R2.setBackgroundRole(QPalette.Base)
		self.imageLabel_R2.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
		self.imageLabel_R2.setMouseTracking(True)
		self.imageLabel_R2.setScaledContents(True)	

		pic3 = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		pic3.fill(qRgb(0,0,0))
		painter3 = QPainter(pic3)
		painter3.setCompositionMode(QPainter.CompositionMode_Plus)
		
		pen3 = QPen()
		for i in range(1,280):
			for j in range(1,280):
				v = self.CH1_label_edit[i][j]
				if v == 1:
					pen3.setColor(QColor(200,0,0))
					painter3.setPen(pen3)
					painter3.drawPoint(j,i)
				if v == 2:
					pen3.setColor(QColor(150,0,0))
					painter3.setPen(pen3)
					painter3.drawPoint(j,i)
				if v == 3:
					pen3.setColor(QColor(100,0,0))
					painter3.setPen(pen3)
					painter3.drawPoint(j,i)
				if v == 4:
					pen3.setColor(QColor(50,0,0))
					painter3.setPen(pen3)
					painter3.drawPoint(j,i)
		del pen3
		del painter3
		
		self.imageLabel_R2.setPixmap(QPixmap.fromImage(pic3))
				
		self.scrollArea_R2.setMouseTracking(True)
		self.scrollArea_R2.setBackgroundRole(QPalette.Dark)
		self.scrollArea_R2.setWidget(self.imageLabel_R2)
		self.scrollArea_R2.horizontalScrollBar().setRange(0,0)
		self.scrollArea_R2.verticalScrollBar().setRange(0,0)
		self.scrollArea_R2.horizontalScrollBar().setValue(0)
		self.scrollArea_R2.verticalScrollBar().setValue(0)
		self.scrollArea_R2.setFixedSize(284,284)
		
		#self.slider.setDisabled(True)
		self.slider.setRange(1,self.t_span)
		self.slider.setValue(1)
		self.slider.valueChanged.connect(self.sliderChange)
		
		#self.spinBox.setDisabled(True)
		self.spinBox.setRange(1,self.t_span)
		self.spinBox.setValue(1)
		self.spinBox.valueChanged.connect(self.spinChange)
		
		self.starButton.setIcon(QIcon("../LoneStar.png"))
		self.starButton.clicked.connect(self.starButtonEvent)
		
		self.playButton.setIcon(QIcon("../play.png"))
		self.playButton.clicked.connect(self.playButtonEvent)

		self.pauseButton.setIcon(QIcon("../pause.png"))
		self.pauseButton.clicked.connect(self.pauseButtonEvent)

		self.stopButton.setIcon(QIcon("../stop.png"))
		self.stopButton.clicked.connect(self.stopButtonEvent)
		
		
		hLabel = QLabel("t")
		hLabel.setDisabled(True)
		
		GridLayout = QGridLayout()
		HBoxLayout_top = QHBoxLayout()
		HBoxLayout_bottom = QHBoxLayout()
		HBoxLayout = QHBoxLayout()
		
		HBoxLayout.addWidget(self.scrollArea)
		HBoxLayout.addWidget(self.scrollArea_R1)
		HBoxLayout.addWidget(self.scrollArea_R2)
		
		HBoxLayout_top.addWidget(self.progress)
		HBoxLayout_top.addWidget(self.playButton)
		HBoxLayout_top.addWidget(self.pauseButton)
		HBoxLayout_top.addWidget(self.stopButton)
		HBoxLayout_top.addWidget(self.starButton)

		
		HBoxLayout_bottom.addWidget(self.spinBox)
		HBoxLayout_bottom.addWidget(hLabel)
		HBoxLayout_bottom.addWidget(self.slider)

		
		# add one line of objects
		self.R2_Label1 = QLabel("1.MIXING MODE")
		self.R2_combo1 = QComboBox(self)
		self.R2_combo1.addItem('MIX_ORG')
		self.R2_combo1.addItem('MIX_EDIT')
		self.R2_combo1.currentIndexChanged.connect(self.mixing_mode_change_func)
		
		self.R2_Label2 = QLabel("2.ORIGINAL")
		self.R2_combo2 = QComboBox(self)
		self.R2_combo2.addItem('CH1_Label_IMG')
		self.R2_combo2.addItem('CH2_Label_IMG')
		self.R2_combo2.currentIndexChanged.connect(self.original_label_flag_func)
		
		self.R2_Label3 = QLabel("3.EDITED")
		self.R2_combo3 = QComboBox(self)
		self.R2_combo3.addItem('CH1_Label_IMG')
		self.R2_combo3.addItem('CH2_Label_IMG')
		self.R2_combo3.currentIndexChanged.connect(self.edited_label_flag_func)
		
		R2_Layout = QHBoxLayout()
		R2_Layout.addWidget(self.R2_Label1)
		R2_Layout.addWidget(self.R2_combo1)
		R2_Layout.addWidget(self.R2_Label2)
		R2_Layout.addWidget(self.R2_combo2)
		R2_Layout.addWidget(self.R2_Label3)
		R2_Layout.addWidget(self.R2_combo3)
		
		
		GridLayout.addLayout(HBoxLayout_top,0,0)
		GridLayout.addLayout(R2_Layout,1,0)
		GridLayout.addLayout(HBoxLayout,2,0)
		GridLayout.addLayout(HBoxLayout_bottom,3,0)
		
		Holder = QWidget()
		Holder.setLayout(GridLayout)
		
		self.setCentralWidget(Holder)
		self.setWindowTitle("TIMING Protocol s/w 1.5 Editing")
		self.show()
	
	def getImagePath(self, CH):
		path = self.path + "B" + str(self.BID).zfill(3) + "/crops_8bit_s/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"_t"+str(self.t)+".tif"
		return path

	def getBGImagePath(self,CH):
		path = self.path + "B" + str(self.BID).zfill(3) + "/crops_8bit_s/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg_t"+str(self.t)+".tif"
		return path

	def getLabelImagePath(self, CH):
		path = self.path + "B" + str(self.BID).zfill(3) +"/label_img/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg_t"+str(self.t)+".tif"
		return path
		
		
	def loadImages(self):
		
		if str(self.t) in self.CH0_dict.keys():
			self.CH0 = self.CH0_dict[str(self.t)]
		else:
			if os.path.isfile(self.getImagePath(0)):
				self.CH0_dict[str(self.t)] = QImage(self.getImagePath(0))
			else:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH0_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH0 = self.CH0_dict[str(self.t)]
		
		if str(self.t) in self.CH1_dict.keys():
			self.CH1 = self.CH1_dict[str(self.t)]
		else:
			if os.path.isfile(self.getBGImagePath(1)):
				self.CH1_dict[str(self.t)] = QImage(self.getBGImagePath(1))
			else:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH1_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH1 = self.CH1_dict[str(self.t)]
		
		if str(self.t) in self.CH2_dict.keys():
			self.CH2 = self.CH2_dict[str(self.t)]
		else:
			if os.path.isfile(self.getBGImagePath(2)):
				self.CH2_dict[str(self.t)] = QImage(self.getBGImagePath(2))
			else:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH2_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH2 = self.CH2_dict[str(self.t)]
		
		
		if str(self.t) in self.CH3_dict.keys():
			self.CH3 = self.CH3_dict[str(self.t)]
		else:
			if os.path.isfile(self.getImagePath(3)):
				self.CH3_dict[str(self.t)] = QImage(self.getImagePath(3))
				
			else:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH3_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH3 = self.CH3_dict[str(self.t)]

		if str(self.t) in self.CH1_label_dict.keys():
			self.CH1_label = self.CH1_label_dict[str(self.t)]
		else:
			if os.path.isfile(self.getLabelImagePath(1)):
				CH1_label = sitk.ReadImage(self.getLabelImagePath(1))
				self.CH1_label_dict[str(self.t)] = sitk.GetArrayFromImage(CH1_label)
				
			else:
				self.CH1_label_dict[str(self.t)] = np.zeros([self.Width, self.Height], dtype = np.uint16)
			self.CH1_label = self.CH1_label_dict[str(self.t)]
		
		if str(self.t) in self.CH2_label_dict.keys():
			self.CH2_label = self.CH2_label_dict[str(self.t)]
		else:
			if os.path.isfile(self.getLabelImagePath(2)):
				CH2_label = sitk.ReadImage(self.getLabelImagePath(2))
				self.CH2_label_dict[str(self.t)] = sitk.GetArrayFromImage(CH2_label)
				
			else:
				self.CH2_label_dict[str(self.t)] = np.zeros([self.Width, self.Height], dtype = np.uint16)
			self.CH2_label = self.CH2_label_dict[str(self.t)]

		if str(self.t) in self.CH1_label_dict_edit.keys():
			self.CH1_label_edit = self.CH1_label_dict_edit[str(self.t)]
		else:
			self.CH1_label_dict_edit[str(self.t)] = copy.deepcopy(self.CH1_label_dict[str(self.t)])
			self.CH1_label_edit = self.CH1_label_dict_edit[str(self.t)]
		
		if str(self.t) in self.CH2_label_dict_edit.keys():
			self.CH2_label_edit = self.CH2_label_dict_edit[str(self.t)]
		else:
			self.CH2_label_dict_edit[str(self.t)] = copy.deepcopy(self.CH2_label_dict[str(self.t)])
			self.CH2_label_edit = self.CH2_label_dict_edit[str(self.t)]
			
		

	def loadAllImages(self):
		counts = len(self.CH0_dict)
		self.progress.setValue(counts)
		t_temp =self.t
		for t in range(1,self.t_span+1):
			self.t = t
			self.loadImages()			
			counts = len(self.CH0_dict)
			if counts == self.t_span:
				counts = 100
			self.progress.setValue(counts)
		self.t = t_temp
		
	def refreshImages(self):
		pic = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		pic.fill(qRgb(0,0,0))
		painter = QPainter(pic)
		painter.setCompositionMode(QPainter.CompositionMode_Plus)
		
		if self.Display_Flags['CH0'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(255,255,255))
			channelImage.setAlphaChannel(self.CH0)
			painter.drawImage(0,0,channelImage)
		
		if self.Display_Flags['CH1'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(255,0,0))
			channelImage.setAlphaChannel(self.CH1)
			painter.drawImage(0,0,channelImage)
		
		if self.Display_Flags['CH2'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(0,255,0))
			channelImage.setAlphaChannel(self.CH2)
			painter.drawImage(0,0,channelImage)
			
		if self.Display_Flags['CH3'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(127,0,255))
			channelImage.setAlphaChannel(self.CH3)
			painter.drawImage(0,0,channelImage)
		
		if self.mixing_mode_flag == 0:
		
			pen = QPen(Qt.cyan)
			painter.setPen(pen)
			if self.Display_Flags['CH1_label'] == True:
				for i in range(1,280):
					for j in range(1,280):
						v = self.CH1_label[i][j]
						if v >0:
							v1 = self.CH1_label[i][j+1]
							v2 = self.CH1_label[i+1][j]
							v3 = self.CH1_label[i][j-1]
							v4 = self.CH1_label[i-1][j]
							if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
								for k1 in range(-1,2):
									for k2 in range (-1,2):
										painter.drawPoint(j+k1,i+k2)
							
							
			pen.setColor(Qt.magenta)
			painter.setPen(pen)
			if self.Display_Flags['CH2_label'] == True:
				for i in range(1,280):
					for j in range(1,280):
						v = self.CH2_label[i][j]
						if v >0:
							v1 = self.CH2_label[i][j+1]
							v2 = self.CH2_label[i+1][j]
							v3 = self.CH2_label[i][j-1]
							v4 = self.CH2_label[i-1][j]
							if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
								for k1 in range(-1,2):
									for k2 in range (-1,2):
										painter.drawPoint(j+k1,i+k2)
								
		else:
			pen = QPen(Qt.cyan)
			painter.setPen(pen)
			if self.Display_Flags['CH1_label'] == True:
				for i in range(1,280):
					for j in range(1,280):
						v = self.CH1_label_edit[i][j]
						if v >0:
							v1 = self.CH1_label_edit[i][j+1]
							v2 = self.CH1_label_edit[i+1][j]
							v3 = self.CH1_label_edit[i][j-1]
							v4 = self.CH1_label_edit[i-1][j]
							if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
								for k1 in range(-1,2):
									for k2 in range (-1,2):
										painter.drawPoint(j+k1,i+k2)
							
							
			pen.setColor(Qt.magenta)
			painter.setPen(pen)
			if self.Display_Flags['CH2_label'] == True:
				for i in range(1,280):
					for j in range(1,280):
						v = self.CH2_label_edit[i][j]
						if v >0:
							v1 = self.CH2_label_edit[i][j+1]
							v2 = self.CH2_label_edit[i+1][j]
							v3 = self.CH2_label_edit[i][j-1]
							v4 = self.CH2_label_edit[i-1][j]
							if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
								for k1 in range(-1,2):
									for k2 in range (-1,2):
										painter.drawPoint(j+k1,i+k2)

		
		# paint some information
		#Time
		pen.setColor(Qt.white)
		painter.setPen(pen)
		font = QFont()
		font.setFamily('Lucida')
		font.setFixedPitch(True)
		font.setPointSize(15)
		font.setBold(True)
		painter.setFont(font)
		t = self.t
		TimInt = self.Tag.TimInt
		N = 60/TimInt
		hour = t/N
		minute = (t%N)*TimInt
		Time_str = 'TIME: ' + str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':00'
		painter.drawText(30,30,Time_str)
		
		#Legend
		pen.setColor(Qt.red)
		painter.setPen(pen)
		painter.setBrush(Qt.red)
		painter.drawEllipse(25,230,10,10)
		
		pen.setColor(Qt.green)
		painter.setPen(pen)
		painter.setBrush(Qt.green)
		painter.drawEllipse(25,250,10,10)
		
		pen.setColor(Qt.white)
		painter.setPen(pen)
		font = QFont()
		font.setFamily('Lucida')
		font.setFixedPitch(True)
		font.setPointSize(10)
		font.setBold(True)
		painter.setFont(font)
		
		painter.drawText(45,240,'Effector')
		painter.drawText(45,260,'Target')
		
		#scale
		mu = QChar(0x00b5)
		scale1 = '25 '
		scale2 = 'm'
		
		pen.setColor(Qt.white)
		painter.setPen(pen)
		painter.setBrush(Qt.white)
		painter.drawRect(170,230,75,5)
		
		pen.setColor(Qt.white)
		painter.setPen(pen)
		font = QFont()
		font.setFamily('Lucida')
		font.setFixedPitch(True)
		font.setPointSize(10)
		font.setBold(True)
		painter.setFont(font)
		
		painter.drawText(195,250,scale1)
		painter.drawText(215,250,mu)
		painter.drawText(225,250,scale2)
			
		del pen
		del painter
		
		self.imageLabel.setPixmap(QPixmap.fromImage(pic))

	def refreshImages2(self):
		
		if self.label_image_2_flag == 0:
			pic2 = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			pic2.fill(qRgb(0,0,0))
			painter2 = QPainter(pic2)
			painter2.setCompositionMode(QPainter.CompositionMode_Plus)
			
			pen2 = QPen()
			for i in range(1,280):
				for j in range(1,280):
					v = self.CH1_label[i][j]
					if v == 1:
						pen2.setColor(QColor(200,0,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
					if v == 2:
						pen2.setColor(QColor(150,0,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
					if v == 3:
						pen2.setColor(QColor(100,0,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
					if v == 4:
						pen2.setColor(QColor(50,0,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
			del pen2
			del painter2
			
			self.imageLabel_R1.setPixmap(QPixmap.fromImage(pic2))
		
		if self.label_image_2_flag == 1:
			pic2 = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			pic2.fill(qRgb(0,0,0))
			painter2 = QPainter(pic2)
			painter2.setCompositionMode(QPainter.CompositionMode_Plus)
			
			pen2 = QPen()
			for i in range(1,280):
				for j in range(1,280):
					v = self.CH2_label[i][j]
					if v == 1:
						pen2.setColor(QColor(0,200,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
					if v == 2:
						pen2.setColor(QColor(0,150,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
					if v == 3:
						pen2.setColor(QColor(0,100,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
					if v == 4:
						pen2.setColor(QColor(0,50,0))
						painter2.setPen(pen2)
						painter2.drawPoint(j,i)
			del pen2
			del painter2
			
			self.imageLabel_R1.setPixmap(QPixmap.fromImage(pic2))
		
		
	
	def refreshImages3(self):
		if self.label_image_3_flag == 0:
			pic3 = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			pic3.fill(qRgb(0,0,0))
			painter3 = QPainter(pic3)
			painter3.setCompositionMode(QPainter.CompositionMode_Plus)
			
			pen3 = QPen()
			for i in range(1,280):
				for j in range(1,280):
					v = self.CH1_label_edit[i][j]
					if v == 1:
						pen3.setColor(QColor(200,0,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
					if v == 2:
						pen3.setColor(QColor(150,0,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
					if v == 3:
						pen3.setColor(QColor(100,0,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
					if v == 4:
						pen3.setColor(QColor(50,0,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
			del pen3
			del painter3
			
			self.imageLabel_R2.setPixmap(QPixmap.fromImage(pic3))
		
		if self.label_image_3_flag == 1:
			pic3 = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			pic3.fill(qRgb(0,0,0))
			painter3 = QPainter(pic3)
			painter3.setCompositionMode(QPainter.CompositionMode_Plus)
			
			pen3 = QPen()
			for i in range(1,280):
				for j in range(1,280):
					v = self.CH2_label_edit[i][j]
					if v == 1:
						pen3.setColor(QColor(0,200,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
					if v == 2:
						pen3.setColor(QColor(0,150,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
					if v == 3:
						pen3.setColor(QColor(0,100,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
					if v == 4:
						pen3.setColor(QColor(0,50,0))
						painter3.setPen(pen3)
						painter3.drawPoint(j,i)
			del pen3
			del painter3
			
			self.imageLabel_R2.setPixmap(QPixmap.fromImage(pic3))
	
	
		
	# From here, most of the functions are event handler or slots		
	def spinChange(self):
		self.slider.setValue(self.spinBox.value())
		# self.t = self.spinBox.value()
		# self.loadImages()
		# self.refreshImages()
	
	def sliderChange(self):
		self.spinBox.setValue(self.slider.value())
		self.t = self.slider.value()
		self.loadImages()
		self.refreshImages()
		self.refreshImages2()
		self.refreshImages3()
		
	def keyPressEvent(self, e):
		if (e.key()>=Qt.Key_0 and e.key()<=Qt.Key_9):
			num = e.key() - 0x30
			if num == 0:
				self.Display_Flags['CH0'] = not self.Display_Flags['CH0']
			if num == 1:
				self.Display_Flags['CH1'] = not self.Display_Flags['CH1']
			if num == 2:
				self.Display_Flags['CH2'] = not self.Display_Flags['CH2']
			if num == 3:
				self.Display_Flags['CH3'] = not self.Display_Flags['CH3']
			if num == 4:
				self.Display_Flags['CH1_label'] = not self.Display_Flags['CH1_label']
			if num == 5:
				self.Display_Flags['CH2_label'] = not self.Display_Flags['CH2_label']
		self.refreshImages()
			
	
	def playButtonEvent(self):
		self.loadAllImages()

		if self.t == self.t_span:
			self.t = 1
		
		self.timer.start(800)
	
	def tick_timer(self):
		self.t = (self.t + 1) % self.t_span
		if self.t == 0:
			self.t = self.t_span
		self.spinBox.setValue(self.t)
	
	def pauseButtonEvent(self):
		self.timer.stop()
		
	def stopButtonEvent(self):
		self.timer.stop()
		self.t = 1
		self.spinBox.setValue(self.t)
		
	def starButtonEvent(self):
		
		print "please go to Nanowell for feature!"
		# self.load_well_data()
		
		# if len(self.monoWell)>0:
			# self.monoWell.pop()
		
		# self.monoWell.append(TIMING_Feature_Board(self.path, self.BID, self.row, self.col, self.E, self.T, 1, self.t_span))

		
	def load_well_data(self):
		print "loading cell Features..."

		path = self.path
		B = self.BID
		Well = self.Well_ID

		self.E = {}
		self.T = {}

		path = path + "features/2_Cell_Pool/" + "B" + str(B).zfill(3) + "No" + str(Well)

		for j in range(1,5):
			fname = path + "E" + str(j) + ".txt"
			if os.path.isfile(fname):
				f = open(fname)
				temp = f.readlines()
				feat = []
				for i in range(0,5):
					x = temp[i].split()
					x = [x[i] for i in range(0,0+self.t_span)]
					x = [float(x[i]) for i in range(0,self.t_span)]
					#x = [k if k!=-1000 else -1 for k in x]
					feat.append(x)
				self.E["E"+str(j)] = feat
			else:
				print "No cell E" + str(j)


			fname = path + "T" + str(j) + ".txt"
			if os.path.isfile(fname):
				f = open(fname)
				temp = f.readlines()
				feat = []
				for i in range(0,6):
					x = temp[i].split()
					x = [x[i] for i in range(0,0+self.t_span)]
					x = [float(x[i]) for i in range(0,self.t_span)]
					#x = [k if k!=-1000 else -1 for k in x]
					feat.append(x)
				self.T["T"+str(j)] = feat
			else:
				print "No cell T" + str(j)

		print "Loading Done!"
	
	def quick_seg_fix_func(self):
		self.loadAllImages()
		#self.CH1_label_dict_edit = copy.deepcopy(self.CH1_label_dict)
		#self.CH2_label_dict_edit = copy.deepcopy(self.CH2_label_dict)
		
		self.ReSeG1 = Quick_Seg_Fix()		
		self.ReSeG1.show()
		self.connect(self.ReSeG1,SIGNAL('ReSeG_Effector_Channel'),self.ReSeG_slot)
		self.connect(self.ReSeG1,SIGNAL('ReSeG_Target_Channel'),self.ReSeG_slot)
		
	def ReSeG_slot(self,CH,K,frames):
	
		if CH == 'E':
			for index in frames:
				if index > 0 and index <= self.t_span:
					i = str(index)
					temp = self.CH1_label_dict_edit[i]
					img = self.convert_bin_map(temp)
					
					img_label = self.spectral_clustering_func(img, K)
					self.CH1_label_dict_edit[i] = img_label
			CH1_label_temp = []
			for ii in range(1,self.t_span+1):
				CH1_label_temp.append(self.CH1_label_dict_edit[str(ii)])
			Tracker1 = TIMING_Cell_Tracker(CH1_label_temp, self.t_span)
			Tracker1.get_track()
			CH1_label_temp = Tracker1.write_track_img()
			for ii in range(1, self.t_span+1):
				self.CH1_label_dict_edit[str(ii)] = CH1_label_temp[ii-1]
			
		if CH == 'T':
			for index in frames:
				if index > 0 and index <= self.t_span:
					i = str(index)
					temp = self.CH2_label_dict_edit[i]
					img = self.convert_bin_map(temp)
					
					img_label = self.spectral_clustering_func(img, K)
					self.CH2_label_dict_edit[i] = img_label
			CH2_label_temp = []
			for ii in range(1,self.t_span+1):
				CH2_label_temp.append(self.CH2_label_dict_edit[str(ii)])
			Tracker2 = TIMING_Cell_Tracker(CH2_label_temp, self.t_span)
			Tracker2.get_track()
			CH2_label_temp = Tracker2.write_track_img()
			for ii in range(1, self.t_span+1):
				self.CH2_label_dict_edit[str(ii)] = CH2_label_temp[ii-1]
			
		#self.refreshImages3()
	
	def convert_bin_map(self,img):
		
		temp = np.zeros(img.shape)
		Width = 281
		Height = 281
		for i in range(0,Height):
			for j in range(0,Width):
				if img[i][j] != 0:
					temp[i][j] = 1
					
		return temp
		
	def spectral_clustering_func(self, img, K):
		
		mask = img.astype(bool)
		
		img_f = img.astype(float)
		img_f += 1 + 0.2 * np.random.randn(*img.shape)
		
		graph = image.img_to_graph(img_f, mask=mask)
		
		labels = spectral_clustering(graph, n_clusters=K, eigen_solver='arpack')
		
		label_im = -np.ones(mask.shape)
		label_im[mask] = labels
		
		Width = 281
		Height = 281
		for i in range(0,Height):
			for j in range(0,Width):
				label_im[i][j] += 1
		
		return label_im.astype(np.uint16)
		
	def quick_track_fix_func(self):
		self.loadAllImages()
		
		self.Switch1 = Quick_Tracker_Fix()		
		self.Switch1.show()
		self.connect(self.Switch1,SIGNAL('SWITCH_EFFECTORS'),self.quick_switch_slot)
		self.connect(self.Switch1,SIGNAL('SWITCH_TARGETS'),self.quick_switch_slot)
	
	def quick_switch_slot(self,CH,p1,p2,frames):
		if CH == 'E':
			for index in frames:
				if index > 0 and index <= self.t_span:
					i = str(index)
					temp = self.CH1_label_dict_edit[i]
					new_label = copy.deepcopy(temp)
					
					for i in range(0,281):
						for j in range(0,281):
							if new_label[i][j] == p1:
								temp[i][j] = p2
							if new_label[i][j] == p2:
								temp[i][j] = p1
					
					self.CH1_label_dict_edit[i] = temp

		if CH == 'T':
			for index in frames:
				if index > 0 and index <= self.t_span:
					i = str(index)
					temp = self.CH2_label_dict_edit[i]
					new_label = copy.deepcopy(temp)

					for i in range(0,281):
						for j in range(0,281):
							if new_label[i][j] == p1:
								temp[i][j] = p2
							if new_label[i][j] == p2:
								temp[i][j] = p1
					
					self.CH2_label_dict_edit[i] = temp
		
		
	def manual_edit_func(self):
		print "under construction ...."
		
	def save_edit_func(self):
		# write updated images
		CH = 1
		for t in range(1, self.t_span+1):
			fname = self.path + "B" + str(self.BID).zfill(3) +"/label_img/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg_t"+str(t)+".tif"
			io.imsave(fname, self.CH1_label_dict_edit[str(t)])
		CH = 2
		for t in range(1, self.t_span+1):
			fname = self.path + "B" + str(self.BID).zfill(3) +"/label_img/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg_t"+str(t)+".tif"
			io.imsave(fname, self.CH2_label_dict_edit[str(t)])

		# delete feature txt files
		fnames = os.listdir(self.path+'features/2_Cell_Pool/')
		for fname in fnames:
			if fname.startswith("B" + str(self.BID).zfill(3) + "No" + str(self.Well_ID)):
				command = 'del '+ self.path+'features/2_Cell_Pool/' + fname
				os.system(command)
		
		# write new features
		CH1_label_temp = []
		for ii in range(1,self.t_span+1):
			CH1_label_temp.append(self.CH1_label_dict_edit[str(ii)])
		CH2_label_temp = []
		for ii in range(1,self.t_span+1):
			CH2_label_temp.append(self.CH2_label_dict_edit[str(ii)])
		generate_cell_pool(CH1_label_temp, CH2_label_temp, self.path, "B" + str(self.BID).zfill(3), self.Well_ID, self.t_span)
		
		
	def mixing_mode_change_func(self):
		temp = self.R2_combo1.currentText()
		
		if temp == 'MIX_ORG':
			self.mixing_mode_flag = 0
		
		if temp == 'MIX_EDIT':
			self.mixing_mode_flag = 1
			
		self.refreshImages()
		
	def original_label_flag_func(self):
		temp = self.R2_combo2.currentText()
		
		if temp == 'CH1_Label_IMG':
			self.label_image_2_flag = 0
		
		if temp == 'CH2_Label_IMG':
			self.label_image_2_flag = 1
			
		self.refreshImages2()
		
	def edited_label_flag_func(self):
		temp = self.R2_combo3.currentText()
		
		if temp == 'CH1_Label_IMG':
			self.label_image_3_flag = 0
		
		if temp == 'CH2_Label_IMG':
			self.label_image_3_flag = 1
			
		self.refreshImages3()

	
def main():
	app = QApplication(sys.argv)
	path = "C:\\Users\\Hengyang\\Desktop\\TIMING 1.0\\Dataset\\20160211_GR_01_CARTAR_M\\"
	BID = 1
	row = 3
	col = 1
	t = 1
	t_span = 72
	cube = TIMING_ReEditBox(path, BID, row, col, t, t_span)
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()
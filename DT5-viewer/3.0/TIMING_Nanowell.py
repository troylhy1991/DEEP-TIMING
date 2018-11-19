import sys,os

import SimpleITK as sitk
import numpy as np

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from TIMING_Feature_Board import *
from TIMING_ReEditBox import *
from TIMING_DT_Sampler import *

helper_path = "./helper/"
sys.path.append(os.path.abspath(helper_path))
import TIMING_QImageConverter as QC


class Nanowell_Tag():
	def __init__(self):
		self.dataset = 'Dataset ID'
		self.BID = 1
		self.R = 1
		self.C = 1
		self.E_Num = 0
		self.T_Num = 0
		self.tSeek1 = 0
		self.TimInt = 5
		self.DInt = 0
		self.EDInt = 0



class TIMING_Nanowell(QFrame):
	def __init__(self, dataPath, BID, Well_ID, t, t_span, tag):
		super(TIMING_Nanowell,self).__init__()

		self.path = dataPath
		self.BID = BID
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

		self.CH0 = []
		self.CH1 = []
		self.CH2 = []
		self.CH3 = []
		self.CH1_label = []
		self.CH2_label = []
		self.CH1_box = []
		self.CH2_box = []


		self.CH0_dict = {}
		self.CH1_dict = {}
		self.CH2_dict = {}
		self.CH3_dict = {}
		self.CH1_label_dict = {}
		self.CH2_label_dict = {}
		self.CH1_box_dict = {}
		self.CH2_box_dict = {}
		self.CH1_box_dict_edited = {}
		self.CH2_box_dict_edited = {}

		self.monoWell = []


		self.feature_loaded = 0    # indicating whether the feat data is loaded
		self.Display_Flags = {'CH0': True, 'CH1': True, 'CH2': True, 'CH3': False, 'CH1_label': False, 'CH2_label': False, 'CH1_box': True, 'CH2_box': True }
		self.timer = QTimer()
		self.timer.timeout.connect(self.tick_timer)

		self.Width = 281
		self.Height = 281


		self.imageLabel = QLabel()
		self.scrollArea = QScrollArea()
		self.slider = QSlider(Qt.Horizontal)
		self.spinBox = QSpinBox()
		self.playButton = QPushButton()
		self.pauseButton = QPushButton()
		self.stopButton = QPushButton()
		self.communityButton = QPushButton()
		self.editButton = QPushButton()
		self.starButton = QPushButton()
		self.sampleButton = QPushButton()
		self.progress = QProgressBar()



		self.loadBoxes()
		#except:
		#	print "Error1!"

		try:
			self.loadImages()
		except:
			print "Error2!"

		try:
			self.setupUI()
		except:
			print "Error3!"

		try:
			self.refreshImages()
		except Exception:
			print "Error4!"

	def setupUI(self):
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

		if self.Display_Flags['CH1_box'] == True:
			for box in self.CH1_box:
				x = box[1]
				y = box[2]
				w = box[3]
				h = box[4]
				painter.drawRect(x,y,w,h)


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


		if self.Display_Flags['CH2_box'] == True:
			for box in self.CH2_box:
				x = box[1]
				y = box[2]
				w = box[3]
				h = box[4]
				painter.drawRect(x,y,w,h)

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

		self.editButton.setIcon(QIcon("../edit.png"))
		self.editButton.clicked.connect(self.editButtonEvent)


		self.playButton.setIcon(QIcon("../play.png"))
		self.playButton.clicked.connect(self.playButtonEvent)

		self.pauseButton.setIcon(QIcon("../pause.png"))
		self.pauseButton.clicked.connect(self.pauseButtonEvent)

		self.stopButton.setIcon(QIcon("../stop.png"))
		self.stopButton.clicked.connect(self.stopButtonEvent)

		self.sampleButton.setIcon(QIcon("../scissors.png"))
		self.sampleButton.clicked.connect(self.sampleButtonEvent)


		hLabel = QLabel("t")
		hLabel.setDisabled(True)

		GridLayout = QGridLayout()
		HBoxLayout_top1 = QHBoxLayout()
		HBoxLayout_top2 = QHBoxLayout()
		HBoxLayout_bottom = QHBoxLayout()

		HBoxLayout_top1.addWidget(self.progress)
		HBoxLayout_top2.addWidget(self.playButton)
		HBoxLayout_top2.addWidget(self.pauseButton)
		HBoxLayout_top2.addWidget(self.stopButton)
		HBoxLayout_top2.addWidget(self.editButton)
		HBoxLayout_top2.addWidget(self.starButton)
		HBoxLayout_top2.addWidget(self.sampleButton)


		HBoxLayout_bottom.addWidget(self.spinBox)
		HBoxLayout_bottom.addWidget(hLabel)
		HBoxLayout_bottom.addWidget(self.slider)


		# Nanowell Information Display
		pad = "       "

		Info_1A = QLabel("Dataset ID       :")
		Info_1B = QLabel(self.Tag.dataset)
		H1 = QHBoxLayout()
		H1.addWidget(Info_1A)
		H1.addWidget(Info_1B)

		Info_2A = QLabel("Block ID           :")
		Info_2B = QLabel(pad + str(self.Tag.BID))
		H2 = QHBoxLayout()
		H2.addWidget(Info_2A)
		H2.addWidget(Info_2B)

		Info_3A = QLabel("Row                :")
		Info_3B = QLabel(pad + str(self.Tag.R))
		H3 = QHBoxLayout()
		H3.addWidget(Info_3A)
		H3.addWidget(Info_3B)

		Info_4A = QLabel("Column           :")
		Info_4B = QLabel(pad + str(self.Tag.C))
		H4 = QHBoxLayout()
		H4.addWidget(Info_4A)
		H4.addWidget(Info_4B)

		Info_5A = QLabel("# of Effectors :")
		Info_5B = QLabel(pad + str(self.Tag.E_Num))
		H5 = QHBoxLayout()
		H5.addWidget(Info_5A)
		H5.addWidget(Info_5B)

		Info_6A = QLabel("# of Targets   :")
		Info_6B = QLabel(pad + str(self.Tag.T_Num))
		H6 = QHBoxLayout()
		H6.addWidget(Info_6A)
		H6.addWidget(Info_6B)

		V1 = QVBoxLayout()
		V1.addLayout(H1)
		V1.addLayout(H2)
		V1.addLayout(H3)
		V1.addLayout(H4)
		V1.addLayout(H5)
		V1.addLayout(H6)

		GridLayout.addLayout(V1,0,0)
		GridLayout.addLayout(HBoxLayout_top1,1,0)
		GridLayout.addLayout(HBoxLayout_top2,2,0)
		GridLayout.addWidget(self.scrollArea,3,0)
		GridLayout.addLayout(HBoxLayout_bottom,4,0)
		self.setLayout(GridLayout)
		self.setWindowTitle("DEEP-TIMING Nanowell")
		self.show()


	def getImagePath(self, CH):
		path = self.path + "B" + str(self.BID).zfill(3) + "/images/crops_8bit_s/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"_t"+str(self.t)+".tif"
		#print path
		return path

	def getBGImagePath(self,CH):
		path = self.path + "B" + str(self.BID).zfill(3) + "/crops_8bit_s/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg_t"+str(self.t)+".tif"
		#print path
		return path

	def getLabelImagePath(self, CH):
		path = self.path + "B" + str(self.BID).zfill(3) +"/label_img/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg/imgNo"+str(self.Well_ID)+"CH"+str(CH)+"bg_t"+str(self.t)+".tif"
		return path

	def bBoxParser(self, path, cell_type):
		if os.path.isfile(path):
			f = open(path)
			lines = f.readlines()
			f.close()
		else:
			lines = []

		bbox_info = []
		for line in lines:
			temp = []
			temp_line = line.rstrip().split('\t')
			temp.append(int(float(temp_line[0])))
			temp.append(float(temp_line[1]))
			temp.append(float(temp_line[2]))
			temp.append(float(temp_line[3]))
			temp.append(float(temp_line[4]))
			temp.append(float(temp_line[5])) ### box_info read and write consistency
			temp.append(float(temp_line[6]))
			if float(temp_line[5]) == cell_type:
				#if temp[6] > 0.8:
				bbox_info.append(temp)
		return bbox_info

	def getBoxPath(self, cell_type):
		if cell_type == 1:
			path = self.path + "B" + str(self.BID).zfill(3) +"/labels/TRACK/EZ/FRCNN-Fast/imgNo"+str(self.Well_ID) + "/label_E_t"+str(self.t).zfill(3)+".txt"
			#print(path)
			if os.path.isfile(path):
				return path
			else:
				# path = self.path + "B" + str(self.BID).zfill(3) +"/label_FRCNN/imgNo"+str(self.Well_ID) + "_new_EZ/imgNo"+str(self.Well_ID) + "E_t"+str(self.t)+".txt"
				return "_"

		if cell_type == 2:
			path = self.path + "B" + str(self.BID).zfill(3) +"/labels/TRACK/EZ/FRCNN-Fast/imgNo"+str(self.Well_ID) + "/label_T_t"+str(self.t).zfill(3)+".txt"
			#print(path)

			if os.path.isfile(path):
				return path
			else:
				# path = self.path + "B" + str(self.BID).zfill(3) +"/label_FRCNN/imgNo"+str(self.Well_ID) + "_new_EZ/imgNo"+str(self.Well_ID) + "T_t"+str(self.t)+".txt"
				return "_"

	def loadBoxes(self):

		if str(self.t) in self.CH1_box_dict_edited.keys():
			self.CH1_box = self.CH1_box_dict_edited[str(self.t)]
			#print('ckpt1')
		else:
			if os.path.isfile(self.getBoxPath(1)):
				self.CH1_box_dict[str(self.t)] = self.bBoxParser(self.getBoxPath(1),1)
				#print('ckpt1')
			else:
				self.CH1_box_dict[str(self.t)] = []
				#print('ckpt2')
			self.CH1_box_dict_edited[str(self.t)] = self.CH1_box_dict[str(self.t)]
			self.CH1_box = self.CH1_box_dict[str(self.t)]

		if str(self.t) in self.CH2_box_dict_edited.keys():
			self.CH2_box = self.CH2_box_dict_edited[str(self.t)]
		else:
			if os.path.isfile(self.getBoxPath(2)):
				self.CH2_box_dict[str(self.t)] = self.bBoxParser(self.getBoxPath(2), 2)
				#print('ckpt3')
			else:
				self.CH2_box_dict[str(self.t)] = []
				#print('ckpt4')
			self.CH2_box_dict_edited[str(self.t)] = self.CH2_box_dict[str(self.t)]
			self.CH2_box = self.CH2_box_dict[str(self.t)]


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
			if os.path.isfile(self.getImagePath(1)):
				self.CH1_dict[str(self.t)] = QImage(self.getImagePath(1))
				# print(self.getImagePath(1))
			else:
				# print(self.getImagePath(1) + " error .....")
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH1_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH1 = self.CH1_dict[str(self.t)]

		if str(self.t) in self.CH2_dict.keys():
			self.CH2 = self.CH2_dict[str(self.t)]
		else:
			if os.path.isfile(self.getImagePath(2)):
				self.CH2_dict[str(self.t)] = QImage(self.getImagePath(2))
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


	def loadAllImages(self):
		counts = len(self.CH0_dict)
		self.progress.setValue(counts)
		t_temp =self.t
		for t in range(1,self.t_span+1):
			self.t = t
			self.loadImages()
			self.loadBoxes()
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


		################# Paint the basic Images
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

		################## Paint the Boundaries
		if self.Display_Flags['CH0'] == True:
			pen = QPen(Qt.white)
		else:
			pen = QPen(Qt.cyan)
		painter.setPen(pen)
		painter.setFont(QFont('Decorative', 10))
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

		if self.Display_Flags['CH1_box'] == True:
			for box in self.CH1_box:
				x = box[1]
				y = box[2]
				w = box[3]
				h = box[4]
				painter.drawRect(x,y,w,h)
				text = "E." + str(box[0])
				painter.drawText(x,y,text)


		if self.Display_Flags['CH0'] == True:
			pen = QPen(Qt.yellow)
		else:
			pen.setColor(Qt.magenta)
		painter.setPen(pen)
		painter.setFont(QFont('Decorative', 10))
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


		if self.Display_Flags['CH2_box'] == True:
			for box in self.CH2_box:
				x = box[1]
				y = box[2]
				w = box[3]
				h = box[4]
				painter.drawRect(x,y,w,h)
				text = "T." + str(box[0])
				painter.drawText(x,y,text)

			# draw an alignment mouse click point
				# painter.drawEllipse(self.begin_x, self.begin_y, 2, 2)
				# painter.drawEllipse(self.end_x, self.end_y, 2, 2)

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
		#pen.setColor(Qt.red)
		#painter.setPen(pen)
		#painter.setBrush(Qt.red)
		#painter.drawEllipse(25,230,10,10)

		#pen.setColor(Qt.green)
		#painter.setPen(pen)
		#painter.setBrush(Qt.green)
		#painter.drawEllipse(25,250,10,10)

		#pen.setColor(Qt.white)
		#painter.setPen(pen)
		#font = QFont()
		#font.setFamily('Lucida')
		#font.setFixedPitch(True)
		#font.setPointSize(10)
		#font.setBold(True)
		#painter.setFont(font)

		#painter.drawText(45,240,'Effector')
		#painter.drawText(45,260,'Target')

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
		self.loadBoxes()
		self.refreshImages()

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
			if num == 7:
				self.Display_Flags['CH1_box'] = not self.Display_Flags['CH1_box']
			if num == 8:
				self.Display_Flags['CH2_box'] = not self.Display_Flags['CH2_box']
		self.refreshImages()


	def playButtonEvent(self):
		self.loadAllImages()

		if self.t == self.t_span:
			self.t = 1

		self.timer.start(500)

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

		if self.feature_loaded == 0:
			self.load_well_data()

		if len(self.monoWell)>0:
			self.monoWell.pop()

		self.monoWell.append(TIMING_Feature_Board(self.path, self.BID, self.Well_ID, self.E, self.T, self.Tag, 1, self.t_span))

	def sampleButtonEvent(self):

		if self.feature_loaded == 0:
			self.load_well_data()

		self.sampler = TIMING_DT_Sampler(self.path, self.BID, self.Well_ID, self.t_span, self.Tag, self.E, self.T)

	def editButtonEvent(self):
		#print("...")
		self.ReEdit = TIMING_ReEditBox(self.path, self.BID, self.Well_ID, 1, self.t_span, self.Tag)


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

def main():
	app = QApplication(sys.argv)
	path = "/uhpc/roysam/hlu8/TIMING/TIMING_II/TIMING2_Benchmark_Datasets/20160211_GR_01_CARTAR_M/OUT_test2/"
	BID = 1
	Well_ID = 9
	t = 1
	t_span = 72
	tag = Nanowell_Tag()
	cube = TIMING_Nanowell(path, BID, Well_ID, t, t_span, tag)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from TIMING_labelImageQT import *


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


class sliderWindow(QFrame):

	def __init__(self, dataPath, BID, Well_ID, t_span, E, T, tag):

		super(sliderWindow,self).__init__()
		self.t0 = 1
		self.t_prior = 1
		self.t_post = 2

		self.E = E
		self.T = T
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

		self.win1 = LabelImageQT1(dataPath, BID, Well_ID, self.E, self.T, self.t_prior, t_span, self.Tag)
		self.win2 = LabelImageQT1(dataPath, BID, Well_ID, self.E, self.T, self.t0, t_span, self.Tag)
		self.win3 = LabelImageQT1(dataPath, BID, Well_ID, self.E, self.T, self.t_post, t_span, self.Tag)



		self.initUI()
		self.setObjectName("myObject")
		self.setStyleSheet("#myObject {border: 5px solid white}")
		self.show()

	def initUI(self):

		self.spinBox = QSpinBox()
		self.spinBox.setRange(1,self.t_span)
		self.spinBox.setValue(1)
		self.spinBox.valueChanged.connect(self.spinChange)


		self.slider = QSlider(Qt.Horizontal)
		self.slider.setRange(1,self.t_span)
		self.slider.setValue(1)
		self.slider.valueChanged.connect(self.sliderChange)

		HBox1 = QHBoxLayout()
		HBox1.addWidget(self.win1)
		HBox1.addWidget(self.win2)
		HBox1.addWidget(self.win3)

		HBox2 = QHBoxLayout()
		HBox2.addWidget(self.spinBox)
		HBox2.addWidget(self.slider)

		VBox = QVBoxLayout()
		VBox.addLayout(HBox1)
		VBox.addLayout(HBox2)

		self.setLayout(VBox)

	def spinChange(self):
		self.slider.setValue(self.spinBox.value())


	def sliderChange(self):
		self.spinBox.setValue(self.slider.value())
		self.t0 = self.slider.value()

		if self.t0 ==1:
			self.t_prior = 1
		else:
			self.t_prior = self.t0 - 1

		if self.t0 == self.t_span:
			self.t_post = self.t_span
		else:
			self.t_post = self.t0 + 1

		self.refreshImages()

	def refreshImages(self):

		self.win1.spinBox.setValue(self.t_prior)
		self.win2.spinBox.setValue(self.t0)
		self.win3.spinBox.setValue(self.t_post)


def main():
	app = QApplication(sys.argv)
	path = "..\\Temp\\20150827_MM_01_Z\\"
	BID = 3
	row = 1
	col = 3
	t = 1
	t_span = 80
	SW = sliderWindow(path, BID, row, col, t_span)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

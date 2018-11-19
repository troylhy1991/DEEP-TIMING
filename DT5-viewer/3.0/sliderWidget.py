import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from LabelImageQt import *


class Dataset_Tag():
	'''
	A Dataset Tag will be created anytime a dataset is loaded
	'''
	def __init__(self):
		self.path = ''
		self.dataset = 'Dataset ID'
		self.blocks = 30
		self.block_list = []
		self.frames = 72

class Nanowell_Tag():
	'''
	A Nanowell Tag instance is created anytime a nanowell is clicked.
	And the Nanowell Tag will be passed to the slider widget
	'''
	def __init__(self):
		self.BID = 1
		self.Nanowell_ID = 1
		self.E_num = 0
		self.T_num = 0


class sliderWidget(QFrame):

	#def __init__(self, dataPath, BID, Well_ID, t_span, E, T, tag):
	def __init__(self, dataset_tag, nanowell_tag):

		super(sliderWidget,self).__init__()
		self.t0 = 1
		self.t_prior = 1
		self.t_post = 2

		self.dataset_tag = dataset_tag
		self.nanowell_tag = nanowell_tag

		self.E = nanowell_tag.E_num
		self.T = nanowell_tag.T_num
		self.t_span = self.dataset_tag.frames


		self.win1 = LabelImageQT1(dataset_tag, nanowell_tag, self.t_prior)
		self.win2 = LabelImageQT1(dataset_tag, nanowell_tag, self.t0)
		self.win3 = LabelImageQT1(dataset_tag, nanowell_tag, self.t_post)

		self.connect(self.win1, SIGNAL("CLICK_DRAG_SWAP"), self.sync_swap_slot)
		self.connect(self.win2, SIGNAL("CLICK_DRAG_SWAP"), self.sync_swap_slot)
		self.connect(self.win3, SIGNAL("CLICK_DRAG_SWAP"), self.sync_swap_slot)



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

		self.saveButton = QPushButton("save")
		self.saveButton.clicked.connect(self.save_edited_track_slot)
		self.discardButton = QPushButton("discard")
		self.discardButton.clicked.connect(self.discard_nanowell_slot)

		HBox1 = QHBoxLayout()
		HBox1.addWidget(self.win1)
		HBox1.addWidget(self.win2)
		HBox1.addWidget(self.win3)

		HBox2 = QHBoxLayout()
		HBox2.addWidget(self.spinBox)
		HBox2.addWidget(self.slider)
		HBox2.addWidget(self.saveButton)
		HBox2.addWidget(self.discardButton)

		VBox = QVBoxLayout()
		VBox.addLayout(HBox1)
		VBox.addLayout(HBox2)

		self.setLayout(VBox)


	def save_edited_track_slot(self):
		print("save the edited track ... ")

		# # Make the folder for current edited nanowell
		# folder_name = self.dataset_tag.path + "B" + str(self.nanowell_tag.BID).zfill(3) +"/label_FRCNN/imgNo"+str(self.nanowell_tag.Nanowell_ID) + '_GT/'
		# os.system('mkdir ' + folder_name)
		#
		# print('E Number: ', self.nanowell_tag.E_num, 'T Number: ', self.nanowell_tag.T_num)
		#
		# # Write boxes to txt files based on new cell ID
		# for t in range(1, self.t_span+1):
		# 	# write the E box
		# 		fname = folder_name + "/imgNo"+str(self.nanowell_tag.Nanowell_ID) + "E_t"+str(t)+".txt"
		# 		if self.nanowell_tag.E_num > 0:
		# 			f = open(fname, 'w')
		# 			for line in self.win1.CH1_box_dict_edited[str(t)]:
		# 				line = [str(k) for k in line]
		# 				line = '\t'.join(line) + '\n'
		# 				f.writelines(line)
		# 			f.close()
		# 	# write the T box
		# 		fname = folder_name + "/imgNo"+str(self.nanowell_tag.Nanowell_ID) + "T_t"+str(t)+".txt"
		# 		if self.nanowell_tag.T_num > 0:
		# 			f = open(fname, 'w')
		# 			for line in self.win1.CH2_box_dict_edited[str(t)]:
		# 				line = [str(k) for k in line]
		# 				line = '\t'.join(line) + '\n'
		# 				f.writelines(line)
		# 			f.close()

		# Emit Signal and update table value
		self.emit(SIGNAL("SAVE_EDITED_NANOWELL"))
		# Save the table value

	def discard_nanowell_slot(self):
		print("Discard current nanowell ...")
		# discard current nanowell
		self.emit(SIGNAL("DISCARD_NANOWELL"))

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

	def sync_swap_slot(self, mode, t, updated_item):
		# update the items in three nanowell windows
		if mode == 'E':
			self.win1.CH1_box_dict_edited[str(t)] = updated_item
			self.win2.CH1_box_dict_edited[str(t)] = updated_item
			self.win3.CH1_box_dict_edited[str(t)] = updated_item

		if mode == 'T':
			self.win1.CH2_box_dict_edited[str(t)] = updated_item
			self.win2.CH2_box_dict_edited[str(t)] = updated_item
			self.win3.CH2_box_dict_edited[str(t)] = updated_item

		# update the view
		if self.win1.t == t:
			self.win1.loadBoxes()
			self.win1.refreshImages()

		if self.win2.t == t:
			self.win2.loadBoxes()
			self.win2.refreshImages()

		if self.win3.t == t:
			self.win3.loadBoxes()
			self.win3.refreshImages()



def main():
	app = QApplication(sys.argv)

	nanowell_tag1 = Nanowell_Tag()

	dataset_tag1 = Dataset_Tag()

	SW = sliderWidget(dataset_tag1, nanowell_tag1)
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

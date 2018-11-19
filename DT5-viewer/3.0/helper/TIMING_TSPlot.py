import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



import matplotlib.pyplot as plt
import numpy as np

import matplotlib.cbook as cbook

from copy import deepcopy





class TSPlot(QFrame):
	def __init__(self, E, T, cell_flag, feat_flag, tSeek1, DInt, EDInt, t_span = 80, t = 1):
		super(TSPlot,self).__init__()
		self.E = E
		self.T = T
		self.E_norm = deepcopy(E)
		self.T_norm = deepcopy(T)
		self.t = t
		self.t_span = t_span
		self.tSeek1 = tSeek1
		self.DInt = DInt
		self.EDInt = EDInt


		self.cell_flag = cell_flag
		self.feat_flag = feat_flag

		#self.normalize_data()
		self.create_main_frame()

	def normalize_data(self):
		E_num = len(self.E.keys())
		T_num = len(self.T.keys())
		#only the speed and Death Marker needs to be normalized

		#First, Normalize E
		#The speed
		Max_speed_E = 0
		Max_DM_E = 0
		for i in range(1,E_num+1):
			if max(self.E['E'+str(i)][3])>Max_speed_E:
				Max_speed_E = max(self.E['E'+str(i)][3])

			if max(self.E['E'+str(i)][4])>Max_DM_E:
				Max_DM_E = max(self.E['E'+str(i)][4])

		for i in range(1,E_num+1):
			for t in range(0,self.t_span):
				self.E_norm['E'+str(i)][3][t] = self.E['E'+str(i)][3][t]/(Max_speed_E+0.001)
				self.E_norm['E'+str(i)][4][t] = self.E['E'+str(i)][4][t]/(Max_DM_E+0.001)

		#First, Normalize T
		#The speed
		Max_speed_T = 0
		Max_DM_T = 0
		for i in range(1,T_num+1):
			if max(self.T['T'+str(i)][3])>Max_speed_T:
				Max_speed_T = max(self.T['T'+str(i)][3])

			if max(self.T['T'+str(i)][4])>Max_DM_T:
				Max_DM_T = max(self.T['T'+str(i)][4])

		for i in range(1,T_num+1):
			for t in range(0,self.t_span):
				self.T_norm['T'+str(i)][3][t] = self.T['T'+str(i)][3][t]/(Max_speed_T+0.001)
				self.T_norm['T'+str(i)][4][t] = self.T['T'+str(i)][4][t]/(Max_DM_T+0.001)


	def create_main_frame(self):
		self.main_frame = QWidget()


		self.refresh()


		self.Box = QHBoxLayout()
		self.Box.addWidget(self.main_frame)
		self.setLayout(self.Box)
		self.setFixedSize(800,500)
		self.setObjectName("myObject3")
		self.setStyleSheet("#myObject3 {border: 5px solid white}")
		self.show()

	def refresh(self):

		Thresh = 0

		tSeek1 = self.tSeek1
		mini = 0
		maxi = 200

		self.fig = plt.figure(figsize=(8,5))

		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self.main_frame)

		ax = self.fig.add_subplot(1, 1, 1)

		cell_index = self.cell_flag.index(1)
		feat_index = self.feat_flag.index(1)

		if cell_index == 0:
			cell_key = 'E1'
			plot_title = 'Effector Cell 1 Feature Time Series'
			Thresh = self.EDInt
			try:
				feat_data = self.E[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell E1 or No given features"

		if cell_index == 1:
			cell_key = 'E2'
			plot_title = 'Effector Cell 2 Feature Time Series'
			Thresh = self.EDInt
			try:
				feat_data = self.E[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell E2 or No given features"


		if cell_index == 2:
			cell_key = 'E3'
			plot_title = 'Effector Cell 3 Feature Time Series'
			Thresh = self.EDInt
			try:
				feat_data = self.E[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell E3 or No given features"

		if cell_index == 3:
			cell_key = 'E4'
			plot_title = 'Effector Cell 4 Feature Time Series'
			Thresh = self.EDInt
			try:
				feat_data = self.E[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell E4 or No given features"


		if cell_index == 4:
			cell_key = 'T1'
			plot_title = 'Target Cell 1 Feature Time Series'
			Thresh = self.DInt
			try:
				feat_data = self.T[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell T1 or No given features"

		if cell_index == 5:
			cell_key = 'T2'
			plot_title = 'Target Cell 2 Feature Time Series'
			Thresh = self.DInt
			try:
				feat_data = self.T[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell T2 or No given features"


		if cell_index == 6:
			cell_key = 'T3'
			plot_title = 'Target Cell 3 Feature Time Series'
			Thresh = self.DInt
			try:
				feat_data = self.T[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell T3 or No given features"

		if cell_index == 7:
			cell_key = 'T4'
			plot_title = 'Target Cell 4 Feature Time Series'
			Thresh = self.DInt
			try:
				feat_data = self.T[cell_key][feat_index]
				mini = min(feat_data)
				maxi = max(feat_data)
			except:
				print "No cell T4 or No given features"

		if feat_index == 0:
			y_label = 'Position X'

		if feat_index == 1:
			y_label = 'Position Y'

		if feat_index == 2:
			y_label = 'Aspect Ratio'

		if feat_index == 3:
			y_label = 'Speed'

		if feat_index == 4:
			y_label = 'Death Marker'

		if feat_index == 5:
			y_label = 'Contact Ratio'


		try:
			plt.plot(feat_data)
			plt.plot(feat_data,'ro')

			# plot contact line
			if tSeek1>0 and tSeek1<self.t_span:
				plt.plot((tSeek1,tSeek1),(int(mini*0.95),int(maxi*1.05)),'r-')

			# plot deathmarker threshold
			if feat_index == 4:
				plt.plot((0,80),(Thresh,Thresh),'r-')

			plt.xlabel('Time')
			plt.ylabel(y_label)
			plt.title(plot_title)
		except:
			print "Can't Plot Time Series Left!"

	def update_main_frame(self):

		plt.close(self.fig)

		self.Box.removeWidget(self.main_frame)
		self.main_frame.deleteLater()
		self.main_frame = None

		self.main_frame = QWidget()

		self.refresh()

		self.Box.addWidget(self.main_frame)

		self.show()

def main():
	app = QApplication(sys.argv)
	radar = TSPlot()
	app.exec_()

if __name__ == '__main__':
	main()

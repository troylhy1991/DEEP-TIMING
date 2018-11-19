"""
Example of creating a radar chart (a.k.a. a spider or star chart) [1]_.

Although this example allows a frame of either 'circle' or 'polygon', polygon
frames don't have proper gridlines (the lines are circles instead of polygons).
It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
matplotlib.axis to the desired number of vertices, but the orientation of the
polygon is not aligned with the radial axes.

.. [1] http://en.wikipedia.org/wiki/Radar_chart
"""
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from copy import deepcopy

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def example_data():

    data1 = [
        ['Acpect Ratio', 'Speed', 'Death Marker', 'CR'],
        ('Effectors',[
            [0.00, 0.06, 0.01, 1.00],
            [0.05, 0.10, 1.00, 0.00]]),
        ('Targets',[
            [0.00, 0.05, 0.00, 0.05],
            [0.08, 0.94, 0.04, 0.02],
            [0.79, 0.10, 0.00, 0.05],
            [0.79, 0.10, 0.00, 0.05]])
    ]
    return data1

	
class radarMap(QFrame):
	def __init__(self, E, T, t_span = 80, t = 1):
		super(radarMap,self).__init__()
		self.E = E
		self.T = T
		
		self.E_norm = deepcopy(E)
		self.T_norm = deepcopy(T)
		self.t = t
		self.t_span = t_span
		
		self.normalize_data()
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
				
	def pick_data(self,t):
		
		Effector_List =[]
		E_num = len(self.E.keys())
		
		for i in range(1,E_num+1):
			feat = self.E_norm['E'+str(i)]
			temp = [feat[2][t-1], feat[3][t-1], feat[4][t-1], 0.00]
			Effector_List.append(temp)
		if E_num < 4:
			for i in range(1,4-E_num+1):
				temp = [0.00, 0.00, 0.00, 0.00]
				Effector_List.append(temp)
		
		Target_List =[]
		T_num = len(self.T.keys())
		
		for i in range(1,T_num+1):
			feat = self.T_norm['T'+str(i)]
			temp = [feat[2][t-1], feat[3][t-1], feat[4][t-1], feat[5][t-1]]
			Target_List.append(temp)
			
		if T_num < 4:
			for i in range(1,4-T_num+1):
				temp = [0.00, 0.00, 0.00, 0.00]
				Target_List.append(temp)
		
		data1 = [
			['Aspect Ratio', 'Speed', 'Death Marker', 'CR'],
			('Effectors',Effector_List),
			('Targets',Target_List)
		]
		return data1


		
		
	def create_main_frame(self):
		self.main_frame = QWidget()
		
		self.refresh(1)
		
		self.Box = QHBoxLayout()
		self.Box.addWidget(self.main_frame)
		self.setLayout(self.Box)
		self.setFixedSize(650,450)
		self.setObjectName("myObject2")
		self.setStyleSheet("#myObject2 {border: 5px solid white}")
		self.show()
		
	def refresh(self, t):
		
		# print "refresh radarmap " + str(t)
		N = 4
		theta = radar_factory(N, frame='circle')

		data = self.pick_data(t)
		spoke_labels = data.pop(0)

		self.fig = plt.figure()
		self.fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.95, bottom=0.05)

		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self.main_frame)
		
		
		colors = ['r', 'g', 'm', 'y', 'b']
		# Plot the four cases from the example data on separate axes
		for n, (title, case_data) in enumerate(data):
			ax = self.fig.add_subplot(1, 2, n + 1, projection='radar')
			plt.rgrids([0.2, 0.4, 0.6, 0.8])
			ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
						 horizontalalignment='center', verticalalignment='center')
			for d, color in zip(case_data, colors):
				ax.plot(theta, d, color=color)
				ax.fill(theta, d, facecolor=color, alpha=0.25)
			ax.set_varlabels(spoke_labels)

		# add legend relative to top-left plot
		plt.subplot(1, 2, 1)
		labels = ('Cell 1', 'Cell 2', 'Cell 3', 'Cell 4')
		legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
		plt.setp(legend.get_texts(), fontsize='small')

		plt.figtext(0.5, 0.965, 'Feature Snapshots Panel', ha='center', color='black', weight='bold', size='large')

		#self.setCentralWidget(self.main_frame)
		#plt.show()
		
	def update_main_frame(self,t):
		
		plt.close(self.fig)
		self.Box.removeWidget(self.main_frame)
		self.main_frame.deleteLater()
		self.main_frame = None
		
		self.main_frame = QWidget()
		
		self.refresh(t)
		
		self.Box.addWidget(self.main_frame)

		self.show()
def main():
	app = QApplication(sys.argv)
	radar = radarMap()
	app.exec_()
	
if __name__ == '__main__':
	main()

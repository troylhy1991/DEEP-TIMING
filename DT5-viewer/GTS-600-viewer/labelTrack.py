import sys,os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from tableWidget import *
from sliderWidget import *


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
		self.DATASET = 1
		self.GROUP = 1
        self.GLOBAL_SEQ = 1
		self.SEQ = 1
		self.FRAMES = 1
		self.E_num = 0
		self.T_num = 0

class labelTrack(QMainWindow):
    def __init__(self):
        '''
        The main window of labelTrack application.
        '''
        super(labelTrack, self).__init__()

        self.dataset_tag = Dataset_Tag()
        self.nanowell_tag = Nanowell_Tag()

        # File Menu
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        load_action = QAction('&Load', self)
        load_action.triggered.connect(self.load_func)

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_func)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(load_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)


        # About Menu
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.about_func)

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(about_action)

        # create the sub-modules
        self.tableWidget = tableWidget(self.dataset_tag)
        self.sliderWidget = sliderWidget(self.dataset_tag, self.nanowell_tag)

        # establish the connections
        self.connect(self.tableWidget, SIGNAL("Nanowell_Table_Selection"), self.nanowell_click_slot)
        self.connect(self.sliderWidget, SIGNAL("SAVE_EDITED_NANOWELL"), self.saveEditedNanowell)
        self.connect(self.sliderWidget, SIGNAL("DISCARD_NANOWELL"), self.discardNanowell)


        VBox = QVBoxLayout()
        VBox.addWidget(self.tableWidget)
        VBox.addWidget(self.sliderWidget)
        #self.setLayout(VBox)

        LayoutWidget = QWidget()
        LayoutWidget.setLayout(VBox)

        # Main Window Show
        self.setCentralWidget(LayoutWidget)
        self.setWindowTitle('labelTrack of TIMING Project')
        self.show()

    def load_func(self):
        self.dataset_tag.path = str(QFileDialog.getExistingDirectory(self,"Select Directory"))
        self.dataset_tag.path = self.dataset_tag.path + "/"

        folders = os.listdir(self.dataset_tag.path)
        for folder in folders:
            if 'B' in folder:
                self.dataset_tag.block_list.append(folder)

        self.tableWidget.Tag = self.dataset_tag
        self.tableWidget.get_table_data()


    def save_func(self):
        # table_fname = self.dataset_tag.path + '/features/Track_Annotation_Logs.txt'
        #
        # f = open(table_fname, 'w')
        #
        # for line in self.tableWidget.Table_Data:
        #     line = [str(i) for i in line]
        #     temp = '\t'.join(line) + '\n'
        #     f.writelines(temp)
        #
        # f.close()
        print("No saving enabled ...")

    def about_func(self):
        QMessageBox.information(self,"About","Version: labelTrack 4 TIMING \n Author: Hengyang Lu \n Email: hlu9@uh.edu \n Copy Rights Reserved.")

    def nanowell_click_slot(self, tag, nano_tag):
        '''
        The slider window of nanowell will be updated based on the click
        '''
        self.sliderWidget.nanowell_tag = nano_tag
        self.sliderWidget.t_span = int(nano_tag.FRAMES)
        self.sliderWidget.spinBox.setRange(1, int(nano_tag.FRAMES))

        self.sliderWidget.win1.nanowell_tag = nano_tag
        self.sliderWidget.win2.nanowell_tag = nano_tag
        self.sliderWidget.win3.nanowell_tag = nano_tag

        self.sliderWidget.win1.refresh_legacy()
        self.sliderWidget.win2.refresh_legacy()
        self.sliderWidget.win3.refresh_legacy()


        self.sliderWidget.slider.setValue(1)
    def saveEditedNanowell(self):
        row = self.tableWidget.object_selected
        column = 6
        model = self.tableWidget.table.model()
        index = model.index(row,column)
        model.arraydata[index.row()][index.column()] = 1
        self.tableWidget.table.setModel(model)

        # save the edited table
        self.tableWidget.Table_Data = model.arrayData()
        self.save_func()

    def discardNanowell(self):
        row = self.tableWidget.object_selected
        column = 6
        model = self.tableWidget.table.model()
        index = model.index(row,column)
        model.arraydata[index.row()][index.column()] = -1
        self.tableWidget.table.setModel(model)


def main():
    App = QApplication(sys.argv)
    labelTrack1 = labelTrack()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()

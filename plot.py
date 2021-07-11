import sys
import time

import numpy as np

from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure
from matplotlib import pyplot as plt


from PyQt5 import QtCore, QtGui, QtWidgets

from plot_ui import Ui_MainWindow



class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self._main = QtWidgets.QWidget()
        # self.setCentralWidget(self._main)
        # ui = Ui_MainWindow()
        self.setupUi(self)
        layout = QtWidgets.QVBoxLayout(self.frame_plot)

        self.static_canvas = FigureCanvas(Figure(figsize=(7,8)))
        layout.addWidget(self.static_canvas)
        self.addToolBar(NavigationToolbar(self.static_canvas, self))
        self.gridLayout_scroll = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.status_label = QtWidgets.QLabel("", self)
        self.statusBar().addPermanentWidget(self.status_label)
        self.file = ""
        self.all_data = {}
        self.checkboxes = []

        # n = 3
        # for i in range(n):
        #     ax = self.static_canvas.figure.add_subplot(n,1,i+1)
        #     t = np.linspace(0, 10, 501)
        #     ax.plot(t, np.tan(t), ".")
        # dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        # layout.addWidget(dynamic_canvas)
        # self.addToolBar(QtCore.Qt.BottomToolBarArea,
        #                 NavigationToolbar(dynamic_canvas, self))

        # self._static_ax = static_canvas.figure.add_subplot()
        # t = np.linspace(0, 10, 501)
        # self._static_ax.plot(t, np.tan(t), ".")

        # self.ax_2 = static_canvas.figure.add_subplot()
        # t = np.linspace(0, 10, 501)
        # self._static_ax.plot(t, np.sin(t), ".")

        # self._dynamic_ax = dynamic_canvas.figure.subplots()
        # t = np.linspace(0, 10, 101)
        # # Set up a Line2D.
        # self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))
        # self._timer = dynamic_canvas.new_timer(50)
        # self._timer.add_callback(self._update_canvas)
        # self._timer.start()

    # def _update_canvas(self):
    #     t = np.linspace(0, 10, 101)
    #     # Shift the sinusoid as a function of time.
    #     self._line.set_data(t, np.sin(t + time.time()))
    #     self._line.figure.canvas.draw()

    def plot_2d_one(self, value):
        print("plot 2d one")
        # plt.clf()
        self.static_canvas.figure.clf()
        ax = self.static_canvas.figure.add_subplot(1,1,1)
        data_to_plot = []
        for box in self.checkboxes:
            if box.checkState():
                data_type = box.text()
                data_to_plot.append(data_type)
                print("plot: ", data_type, "size: ", len(self.all_data[data_type][0]))
                process_data = self.all_data[data_type]
                if process_data[0][0] > 1e6:
                    for i in range(len(process_data[0])):
                        process_data[0][i] = float(process_data[0][i])/1e6
                data_num = len(process_data)
                for i in range(1, data_num):
                    ax.plot(process_data[0], process_data[i], label=data_type+"_"+str(i))
        ax.legend()
        self.static_canvas.draw()


    def plot_2d_multi(self, value):
        self.static_canvas.figure.clf()
        # ax = self.static_canvas.figure.add_subplot(1,1,1)
        data_to_plot = []
        for box in self.checkboxes:
            if box.checkState():
                data_type = box.text()
                data_to_plot.append(data_type)
        ax_num = len(data_to_plot)
        ax_row = int(min(3, ax_num))
        ax_column = int((ax_num-1)/ax_row + 1)
        ax_idx = 0
        for data_type in data_to_plot:
            if data_type in self.all_data:
                print("plot: ", data_type, "size: ", len(self.all_data[data_type][0]))
                ax_idx += 1
                ax = self.static_canvas.figure.add_subplot(ax_row, ax_column, ax_idx)
                process_data = self.all_data[data_type]
                if process_data[0][0] > 1e6:
                    for i in range(len(process_data[0])):
                        process_data[0][i] = float(process_data[0][i])/1e6
                data_num = len(process_data)
                for i in range(1, data_num):
                    ax.plot(process_data[0], process_data[i], label=data_type+"_"+str(i))
                ax.legend()
        # ax.legend()
        self.static_canvas.draw()

    def plot_3d(self, value):
        print("plot 3d")

    def reset(self, value):
        print("reset")
        for i in range(len(self.checkboxes)):
            self.checkboxes[i].setCheckState(False)
        self.static_canvas.figure.clf()
        self.static_canvas.draw()

    def readData(self):
        file_path = self.file
        omit_lines = 0
        with open(file_path) as f:
            while omit_lines:
                f.readline()
                omit_lines -= 1

            for per_line in f.readlines():
                sta_idx = per_line.find(']')
                if sta_idx!=-1:
                    per_line = per_line[sta_idx+2:]
                else:
                    continue
                try:
                    data_type, datas = per_line.split(':')
                except:
                    print("read line error, pass")
                    continue
                datas = datas.split()
                data_len = len(datas)
                if data_type in self.all_data:
                    for i in range(data_len):
                        self.all_data[data_type][i].append(float(datas[i]))
                else:
                    self.all_data[data_type] = []
                    for i in range(data_len):
                        self.all_data[data_type].append([float(datas[i])])

    def insertCheckbox(self):
        # frame_handle = self.gridLayout_scroll.widget()
        # self.gridLayout_scroll.removeWidget(frame_handle)
        # self.gridLayout_3.setObjectName("gridLayout_3")
        for i in range(self.gridLayout_scroll.count()):
            self.gridLayout_scroll.itemAt(i).widget().deleteLater()
        frame_plot_data = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        # self.frame_plot_data.setFrameShape(QtWidgets.QFrame.StyledPanel)
        box_num = 0
        for key in self.all_data:
            # print(key)
            check_box = QtWidgets.QCheckBox(frame_plot_data)
            # check_box.text
            check_box.setText(key)
            box_length = check_box.fontMetrics().width(key) + 20
            box_length = min(box_length, 200)
            check_box.setGeometry(0, 30*box_num, box_length, 25)
            self.checkboxes.append(check_box)
            box_num += 1
        # self.checkBox = QtWidgets.QCheckBox(frame_plot_data)
        # self.checkBox.setGeometry(QtCore.QRect(50, 50, 92, 23))
        # self.checkBox.setObjectName("checkBox")

        # self.checkBox_2 = QtWidgets.QCheckBox(frame_plot_data)
        # self.checkBox_2.setGeometry(QtCore.QRect(60, 120, 92, 23))
        # self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_scroll.addWidget(frame_plot_data, 0, 0, 1, 1)
        self.show_data_scrollArea.setWidget(self.scrollAreaWidgetContents)


    def openFile(self, value):
        self.file, type_f = QtWidgets.QFileDialog.getOpenFileName(self, "choose log file", "/home/chao/px4_ros/glogs/", "All Files (*);;log Files (*.csv)")
        print("open file: ", self.file)
        self.reset(1)
        self.all_data.clear()
        self.checkboxes.clear()
        self.readData()
        self.insertCheckbox()
        self.status_label.setText(self.file)



if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()

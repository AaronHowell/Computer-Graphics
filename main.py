import math
import sys

import numpy as np
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QApplication

from cor import CartesianCoordinateSystem
from line import lineD
from mainwindow import Ui_MainWindow


class MainWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.lineDialog=lineD()
        self.setupUi(self)
        self.initUI()
        self.scene=None
        self.lineDialog.infoSignal.connect(self.DDAline)

    def initUI(self):
        self.ButtonConnect()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.viewport().installEventFilter(self)
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.coordinateSystem = CartesianCoordinateSystem(self.scene)

    def eventFilter(self, obj, event):
        if obj is self.graphicsView.viewport() and event.type()==QEvent.Type.Wheel:
            zoom_in_factor = 1.1
            zoom_out_factor = 1 / zoom_in_factor
            if event.angleDelta().y() > 0:
                self.graphicsView.scale(zoom_in_factor, zoom_in_factor)
            else:
                self.graphicsView.scale(zoom_out_factor, zoom_out_factor)
            return True
        return super().eventFilter(obj, event)
    def ButtonConnect(self):
        self.clean.clicked.connect(self.ButtonSet)
        self.dda.clicked.connect(self.ButtonSet)
        self.bres.clicked.connect(self.ButtonSet)

    def ButtonSet(self):
        btn = self.sender()
        btnName = btn.objectName()
        if btnName=="clean":
            self.clearScene()
        elif btnName=='dda':
            self.lineDialog.infoSignal.disconnect()
            self.lineDialog.infoSignal.connect(self.DDAline)
            self.lineDialog.show()

        elif btnName=='bres':
            self.lineDialog.infoSignal.disconnect()
            self.lineDialog.infoSignal.connect(self.Bresenham)
            self.lineDialog.show()

    def DDAline(self,lineInfo:list):
        x1=lineInfo[0]
        y1 = lineInfo[1]
        x2 = lineInfo[2]
        y2 = lineInfo[3]

        self.coordinateSystem.drawLine(x1,y1,x2,y2, QPen(Qt.red))
        k=(y1-y2)/(x1-x2)
        #取下整数，看和哪个最接近
        if np.abs(k)<=1:
            y=y1
            for x in range(x1,x2+1):
                self.coordinateSystem.drawPoint(x,math.floor(y+0.5),QPen(Qt.red))
                y+=k
        else:
            x=x1
            for y in range(y1,y2+1):
                self.coordinateSystem.drawPoint(math.floor(x+0.5), y, QPen(Qt.red))
                x+=1/k

    def Bresenham(self,lineInfo:list):
        x1=lineInfo[0]
        y1 = lineInfo[1]
        x2 = lineInfo[2]
        y2 = lineInfo[3]
        self.coordinateSystem.drawLine(x1,y1,x2,y2, QPen(Qt.red))
        k = (y1 - y2) / (x1 - x2)
        if np.abs(k)<=1:
            y=y1
            e=-0.5
            for x in range(x1,x2+1):
                self.coordinateSystem.drawPoint(x,y,QPen(Qt.red))
                e+=k
                if e>=0:
                    y+=1
                    e-=1
        else:
            x = x1
            e = -0.5
            for y in range(y1, y2 + 1):
                self.coordinateSystem.drawPoint(x, y, QPen(Qt.red))
                e += 1/k
                if e >= 0:
                    x += 1
                    e -= 1




    def clearScene(self):
        self.coordinateSystem.clearScene()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
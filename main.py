import math
import sys

import numpy as np
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QApplication

from circleDialog import circleDialog
from cor import CartesianCoordinateSystem
from ellipticDialog import ellipticDialog
from line import lineD
from mainwindow import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.lineDialog = lineD()
        self.circleDialog = circleDialog()
        self.ellipseDialog = ellipticDialog()
        self.ellipseDialog.ellipseinfoSignal.connect(self.MidPointEllipse)
        self.circleDialog.circleinfoSignal.connect(self.MidPointCircle)
        self.setupUi(self)
        self.initUI()
        self.scene = None
        self.lineDialog.infoSignal.connect(self.DDAline)




    def initUI(self):
        self.ButtonConnect()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.viewport().installEventFilter(self)
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
        self.coordinateSystem = CartesianCoordinateSystem(self.scene)

    def MidPointEllipse(self, ellipseInfor: list):

        a = ellipseInfor[0]
        x0 = ellipseInfor[1]
        y0 = ellipseInfor[2]
        b = ellipseInfor[3]
        self.coordinateSystem.drawEllipse(x0, y0, a, b, QPen(Qt.green))
        x=int(a+1/2)
        y=0
        taa=a*a
        t2aa=2*taa
        t4aa=a*t2aa

        tbb=b*b
        t2bb=2*tbb
        t4bb=2*t2bb
        t2abb=a*t2bb
        t2bbx=t2bb*x
        tx=x

        d1=t2bbx*(x-1)+tbb/2+t2aa*(1-tbb)
        while t2bb*tx>t2aa*y:
            self.FourSymmetry(x,y,QPen(Qt.green),x0,y0)
            if d1<0:
                y+=1
                d1=d1+t4aa*y+t2aa
                tx=x-1
            else:
                x-=1
                y+=1
                d1=d1-t4bb*x+t4aa*y+t2aa
                tx=x

        d2=t2bb*(x*x+1)-t4bb*x+t2aa*(y*y+y-tbb)+taa/2
        while x>=0:
            self.FourSymmetry(x,y,QPen(Qt.green),x0,y0)
            if d2<0:
                x-=1
                y+=1
                d2=d2+t4aa*y-t4bb*x+t2bb
            else:
                x-=1
                d2=d2-t4bb*x+t2bb

    def BresenhamCircle(self, circleInfo: list):
        r = circleInfo[0]
        x0 = circleInfo[1]
        y0 = circleInfo[2]
        self.coordinateSystem.drawCircle(x0,y0,r,QPen(Qt.blue))
        delta=2-2*r
        x=0
        y=r
        while y >= 0:
            self.FourSymmetry(x,y,QPen(Qt.blue),x0,y0)

            if delta < 0:
                delta1 = 2 * (delta + y) - 1  # 取H点
                if delta1 <= 0:
                    direction = 1
                else:
                    direction = 2  # 取D点
            elif delta > 0:
                delta2 = 2 * (delta - x) - 1  # 取D点
                if delta2 < 0:
                    direction = 2
                else:
                    direction = 3  # 取V点
            else:
                direction = 2

            if direction == 1:
                x += 1
                delta += 2 * x + 1
            elif direction == 2:
                x += 1
                y -= 1
                delta += 2 * (x - y + 1)
            elif direction == 3:
                y -= 1
                delta += -2 * y + 1

    def MidPointCircle(self, circleInfo: list):
        r = circleInfo[0]
        x = circleInfo[1]
        y = circleInfo[2]
        self.coordinateSystem.drawCircle(x, y, r, QPen(Qt.blue))
        i = 0
        j = r
        d = 1.25 - r
        self.EightSymmetry(i, j, QPen(Qt.blue), x, y)
        while i <= j:
            if d < 0:
                d += 2 * i + 3
            else:
                d += 2 * (i - j) + 5
                j -= 1
            i += 1
            self.EightSymmetry(i, j, QPen(Qt.blue), x, y)

    def EightSymmetry(self, i, j, pen:QPen, x, y):
        self.coordinateSystem.drawPoint(i+x,j+y,pen)
        self.coordinateSystem.drawPoint(-i+x, j+y, pen)
        self.coordinateSystem.drawPoint(i+x, -j+y, pen)
        self.coordinateSystem.drawPoint(-i+x, -j+y, pen)
        self.coordinateSystem.drawPoint(j+x,i+y,pen)
        self.coordinateSystem.drawPoint(-j+x, i+y, pen)
        self.coordinateSystem.drawPoint(j+x, -i+y, pen)
        self.coordinateSystem.drawPoint(-j+x, -i+y, pen)

    def FourSymmetry(self,i,j,pen:QPen,x,y):
        self.coordinateSystem.drawPoint(i+x,j+y,pen)
        self.coordinateSystem.drawPoint(-i+x, j+y, pen)
        self.coordinateSystem.drawPoint(i+x, -j+y, pen)
        self.coordinateSystem.drawPoint(-i+x, -j+y, pen)


    def ButtonSet(self):
        btn = self.sender()
        btnName = btn.objectName()
        if btnName == "clean":
            self.clearScene()
        elif btnName == 'dda':
            self.lineDialog.infoSignal.disconnect()
            self.lineDialog.infoSignal.connect(self.DDAline)
            self.lineDialog.show()
        elif btnName == 'bres':
            self.lineDialog.infoSignal.disconnect()
            self.lineDialog.infoSignal.connect(self.Bresenham)
            self.lineDialog.show()
        elif btnName == 'mpc':
            """中点画圆"""
            self.circleDialog.circleinfoSignal.disconnect()
            self.circleDialog.circleinfoSignal.connect(self.MidPointCircle)
            self.circleDialog.show()
            pass
        elif btnName == 'brc':
            """Bresenham画圆"""
            self.circleDialog.circleinfoSignal.disconnect()
            self.circleDialog.circleinfoSignal.connect(self.BresenhamCircle)
            self.circleDialog.show()
            pass
        elif btnName == 'meli':
            """中点椭圆"""
            self.ellipseDialog.show()
            pass

    def DDAline(self, lineInfo: list):
        x1 = lineInfo[0]
        y1 = lineInfo[1]
        x2 = lineInfo[2]
        y2 = lineInfo[3]

        self.coordinateSystem.drawLine(x1, y1, x2, y2, QPen(Qt.red))
        k = (y1 - y2) / (x1 - x2)
        # 取下整数，看和哪个最接近
        if np.abs(k) <= 1:
            y = y1
            for x in range(x1, x2 + 1):
                self.coordinateSystem.drawPoint(x, math.floor(y + 0.5), QPen(Qt.red))
                y += k
        else:
            x = x1
            for y in range(y1, y2 + 1):
                self.coordinateSystem.drawPoint(math.floor(x + 0.5), y, QPen(Qt.red))
                x += 1 / k

    def Bresenham(self, lineInfo: list):
        x1 = lineInfo[0]
        y1 = lineInfo[1]
        x2 = lineInfo[2]
        y2 = lineInfo[3]
        self.coordinateSystem.drawLine(x1, y1, x2, y2, QPen(Qt.red))
        k = (y1 - y2) / (x1 - x2)
        if np.abs(k) <= 1:
            y = y1
            e = -0.5
            for x in range(x1, x2 + 1):
                self.coordinateSystem.drawPoint(x, y, QPen(Qt.red))
                e += k
                if e >= 0:
                    y += 1
                    e -= 1
        else:
            x = x1
            e = -0.5
            for y in range(y1, y2 + 1):
                self.coordinateSystem.drawPoint(x, y, QPen(Qt.red))
                e += 1 / k
                if e >= 0:
                    x += 1
                    e -= 1

    def clearScene(self):
        self.coordinateSystem.clearScene()

    def eventFilter(self, obj, event):
        if obj is self.graphicsView.viewport() and event.type() == QEvent.Type.Wheel:
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
        self.brc.clicked.connect(self.ButtonSet)
        self.mpc.clicked.connect(self.ButtonSet)
        self.meli.clicked.connect(self.ButtonSet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

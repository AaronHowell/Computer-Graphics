import math
import random
import sys
from queue import Queue

import numpy as np
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QApplication

from Polygon import PolygonDialog
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
        self.polygonDialog = PolygonDialog()
        self.lineDialog2 = lineD()
        self.lineDialog2.infoSignal.connect(self.Cohen_Sutherland)
        self.polygonDialog.PolyinfoSignal.connect(self.func1)
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

    def Cohen_Sutherland(self, lineInfo: list):
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8

        left_x=-10
        left_y=10
        width=20
        height=20
        self.coordinateSystem.drawRectangle(left_x, left_y, width, height,QPen(Qt.blue))
        XL=left_x
        XR=left_x+width
        YB=left_y-height
        YT=left_y
        x1 = lineInfo[0]
        y1 = lineInfo[1]
        x2 = lineInfo[2]
        y2 = lineInfo[3]
        self.coordinateSystem.drawLine(lineInfo[0],lineInfo[1],lineInfo[2],lineInfo[3],QPen(Qt.red))
        code1=self.CaculateRegionCode(x1,y1,XL,XR,YB,YT)
        code2=self.CaculateRegionCode(x2,y2,XL,XR,YB,YT)

        while code1 != 0 or code2 != 0:
            if code1 & code2 != 0:
                return

            code = code1 if code1 != 0 else code2

            if LEFT & code:
                x = XL
                y = y1 + (y2 - y1) * (XL - x1) / (x2 - x1)
            elif RIGHT & code:
                x = XR
                y = y1 + (y2 - y1) * (XR - x1) / (x2 - x1)
            elif BOTTOM & code:
                y = YB
                x = x1 + (x2 - x1) * (YB - y1) / (y2 - y1)
            elif TOP & code:
                y = YT
                x = x1 + (x2 - x1) * (YT - y1) / (y2 - y1)

            if code == code1:
                x1 = x
                y1 = y
                code1 = self.CaculateRegionCode(x1, y1, XL, XR, YB, YT)
            else:
                x2 = x
                y2 = y
                code2 = self.CaculateRegionCode(x2, y2, XL, XR, YB, YT)

        self.DDAline([int(x1),int(y1),int(x2),int(y2)])
    def CaculateRegionCode(self,x, y, XL, XR, YB, YT):
        LEFT = 1
        RIGHT = 2
        BOTTOM = 4
        TOP = 8
        code = 0
        if x < XL:
            code |= LEFT
        if x > XR:
            code |= RIGHT
        if y < YB:
            code |= BOTTOM
        if y > YT:
            code |= TOP
        return code
    def point_in_polygon(self, x, y, polygon):
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def func1(self, list_x, list_y):
        for i in range(len(list_x) - 1):
            self.DDAline([list_x[i], list_y[i], list_x[i + 1], list_y[i + 1]])
        self.DDAline([list_x[0], list_y[0], list_x[-1], list_y[-1]])
        polygon_point = [(x, y) for x, y in zip(list_x, list_y)]
        max_x = max(list_x)
        min_x = min(list_x)
        min_y = min(list_y)
        max_y = max(list_y)
        while True:
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            if self.point_in_polygon(x, y, polygon_point):
                break
        seed_queue = Queue()
        seed_queue.put((x, y))
        while not seed_queue.empty():
            x, y = seed_queue.get()
            self.coordinateSystem.drawPoint(x, y, QPen(Qt.red))
            x1 = x
            while True:
                x1 -= 1
                if self.point_in_polygon(x1, y, polygon_point):
                    self.coordinateSystem.drawPoint(x1, y, QPen(Qt.red))
                else:
                    break
            x1 = x
            while True:
                x1 += 1
                if self.point_in_polygon(x1, y, polygon_point):
                    self.coordinateSystem.drawPoint(x1, y, QPen(Qt.red))
                else:
                    break
            if y >= min_y + 1:
                for x in range(min_x, max_x):
                    if self.point_in_polygon(x, y - 1, polygon_point):
                        seed_queue.put((x, y - 1))
                        break
        seed_queue.put((x, y))
        while not seed_queue.empty():
            x, y = seed_queue.get()
            self.coordinateSystem.drawPoint(x, y, QPen(Qt.red))
            x1 = x
            while True:
                x1 -= 1
                if self.point_in_polygon(x1, y, polygon_point):
                    self.coordinateSystem.drawPoint(x1, y, QPen(Qt.red))
                else:
                    if x1 < min_x:
                        break
            x1 = x
            while True:
                x1 += 1
                if self.point_in_polygon(x1, y, polygon_point):
                    self.coordinateSystem.drawPoint(x1, y, QPen(Qt.red))
                else:
                    if x1 > max_x:
                        break
            if y <= max_y - 1:
                for x in range(min_x, max_x):
                    if self.point_in_polygon(x, y + 1, polygon_point):
                        seed_queue.put((x, y + 1))
                        print((x, y + 1))
                        break

    def MidPointEllipse(self, ellipseInfor: list):
        a = ellipseInfor[0]
        x0 = ellipseInfor[1]
        y0 = ellipseInfor[2]
        b = ellipseInfor[3]
        self.coordinateSystem.drawEllipse(x0, y0, a, b, QPen(Qt.green))
        x = int(a + 1 / 2)
        y = 0
        taa = a * a
        t2aa = 2 * taa
        t4aa = a * t2aa
        tbb = b * b
        t2bb = 2 * tbb
        t4bb = 2 * t2bb
        t2bbx = t2bb * x
        tx = x
        d1 = t2bbx * (x - 1) + tbb / 2 + t2aa * (1 - tbb)  # 下半区域
        while t2bb * tx > t2aa * y:
            self.FourSymmetry(x, y, QPen(Qt.green), x0, y0)
            if d1 < 0:
                y += 1
                d1 = d1 + t4aa * y + t2aa
                tx = x - 1  # 从左往右生成点
            else:
                x -= 1
                y += 1
                d1 = d1 - t4bb * x + t4aa * y + t2aa
                tx = x

        d2 = t2bb * (x * x + 1) - t4bb * x + t2aa * (y * y + y - tbb) + taa / 2  # 上半区域
        while x >= 0:
            self.FourSymmetry(x, y, QPen(Qt.green), x0, y0)
            if d2 < 0:
                x -= 1
                y += 1
                d2 = d2 + t4aa * y - t4bb * x + t2bb
            else:
                x -= 1
                d2 = d2 - t4bb * x + t2bb

    def BresenhamCircle(self, circleInfo: list):
        r = circleInfo[0]
        x0 = circleInfo[1]
        y0 = circleInfo[2]
        self.coordinateSystem.drawCircle(x0, y0, r, QPen(Qt.blue))
        delta = 2 - 2 * r
        x = 0
        y = r
        while y >= 0:
            self.FourSymmetry(x, y, QPen(Qt.blue), x0, y0)

            if delta < 0:
                delta1 = 2 * (delta + y) - 1  # HD
                if delta1 <= 0:
                    direction = 1  # 取H点
                else:
                    direction = 2  # 取D点
            elif delta > 0:
                delta2 = 2 * (delta - x) - 1  # DV
                if delta2 < 0:
                    direction = 2  # 取D点
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
                d += 2 * i + 3  # 取靠外的一个像素，也就是右一
            else:
                d += 2 * (i - j) + 5  # 取靠内的一个像素，也就是右下
                j -= 1
            i += 1
            self.EightSymmetry(i, j, QPen(Qt.blue), x, y)

    def EightSymmetry(self, i, j, pen: QPen, x, y):
        self.coordinateSystem.drawPoint(i + x, j + y, pen)
        self.coordinateSystem.drawPoint(-i + x, j + y, pen)
        self.coordinateSystem.drawPoint(i + x, -j + y, pen)
        self.coordinateSystem.drawPoint(-i + x, -j + y, pen)
        self.coordinateSystem.drawPoint(j + x, i + y, pen)
        self.coordinateSystem.drawPoint(-j + x, i + y, pen)
        self.coordinateSystem.drawPoint(j + x, -i + y, pen)
        self.coordinateSystem.drawPoint(-j + x, -i + y, pen)

    def FourSymmetry(self, i, j, pen: QPen, x, y):
        self.coordinateSystem.drawPoint(i + x, j + y, pen)
        self.coordinateSystem.drawPoint(-i + x, j + y, pen)
        self.coordinateSystem.drawPoint(i + x, -j + y, pen)
        self.coordinateSystem.drawPoint(-i + x, -j + y, pen)

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
        elif btnName == 'ex3_1':
            '''多边形扫描转换'''
            self.polygonDialog.show()
            pass
        elif btnName == 'ex4':

            self.lineDialog2.show()
            pass

    def DDAline(self, lineInfo: list):
        x1 = lineInfo[0]
        y1 = lineInfo[1]
        x2 = lineInfo[2]
        y2 = lineInfo[3]

        self.coordinateSystem.drawLine(x1, y1, x2, y2, QPen(Qt.red))
        if x1 - x2 == 0:
            k = 111111
        else:
            k = (y1 - y2) / (x1 - x2)
        # 取下整数，看和哪个最接近
        if np.abs(k) <= 1:
            t2 = max(x1, x2)
            t1 = min(x1, x2)
            if t1 == x1:
                y = y1
            else:
                y = y2
            for x in range(t1, t2 + 1):
                self.coordinateSystem.drawPoint(x, math.floor(y + 0.5), QPen(Qt.red))
                y += k
        else:
            t2 = max(y1, y2)
            t1 = min(y1, y2)
            if t1 == y1:
                x = x1
            else:
                x = x2
            for y in range(t1, t2 + 1):
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
        self.ex3_1.clicked.connect(self.ButtonSet)
        self.ex4.clicked.connect(self.ButtonSet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QPainterPath
from PyQt5.QtWidgets import (QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem)


class CartesianCoordinateSystem:

    def __init__(self, scene):
        self.scene = scene
        self.unit = 20
        self.drawCoordinateSystem()

    def drawCoordinateSystem(self):
        # 创建用于坐标轴的QPen（实线黑色）
        axis_pen = QPen(Qt.black)
        axis_pen.setStyle(Qt.SolidLine)
        # 绘制坐标轴
        self.scene.addLine(-1000, 0, 1000, 0, axis_pen)
        self.scene.addLine(0, -1000, 0, 1000, axis_pen)
        # 绘制刻度
        for i in range(-1000, 1001, self.unit):
            if i != 0:
                self.scene.addLine(i, -5, i, 5, axis_pen)
                self.scene.addLine(-5, i, 5, i, axis_pen)
        # 绘制虚线网格
        grid_pen = QPen(QColor(192, 192, 192))  # 浅灰色
        grid_pen.setStyle(Qt.DashLine)
        for i in range(-1000, 1001, self.unit):
            if i != 0:
                self.scene.addLine(-1000, i, 1000, i, grid_pen)
                self.scene.addLine(i, -1000, i, 1000, grid_pen)

    def clearScene(self):
        for item in self.scene.items():
            self.scene.removeItem(item)
        self.drawCoordinateSystem()

    def drawPoint(self, x, y, pen):
        x = x * self.unit
        y = y * self.unit

        path = QPainterPath()
        path.addEllipse(x - 5, -y - 5, 10, 10)
        point_item = self.scene.addPath(path, pen)
        return point_item

    def drawRectangle(self, x, y, width, height, pen, filled=False):
        x = x * self.unit
        y = y * self.unit
        width = width * self.unit
        height = height * self.unit
        rect_item = QGraphicsRectItem(x, -y, width, height)
        rect_item.setPen(pen)
        if filled:
            rect_item.setBrush(pen.color())
        self.scene.addItem(rect_item)
        return rect_item

    def drawCircle(self, x, y, radius, pen, filled=False):
        circle_item = QGraphicsEllipseItem((x - radius)*self.unit , -(y + radius)*self.unit,
                                           2 * radius*self.unit , 2 * radius*self.unit)
        circle_item.setPen(pen)
        if filled:
            circle_item.setBrush(pen.color())
        self.scene.addItem(circle_item)
        return circle_item

    def drawLine(self, x1, y1, x2, y2, pen):
        line_item = QGraphicsLineItem(x1 * self.unit, -y1 * self.unit, x2 * self.unit, -y2 * self.unit)
        line_item.setPen(pen)
        self.scene.addItem(line_item)
        return line_item

    def drawEllipse(self,x,y,a,b,pen):
        ellipse_item = QGraphicsEllipseItem((x - a)*self.unit , -(y + b)*self.unit,
                                           2 * a*self.unit , 2 * b*self.unit)
        ellipse_item.setPen(pen)

        self.scene.addItem(ellipse_item)
        return ellipse_item
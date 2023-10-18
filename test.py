import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen

class MyView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setSceneRect(-200, -200, 400, 400)

        self.setDragMode(QGraphicsView.ScrollHandDrag)


    def wheelEvent(self, event):
        # 实现滚轮放大缩小功能
        zoom_in_factor = 1.1
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        view = MyView()
        self.setCentralWidget(view)

        red_ellipse = QGraphicsEllipseItem(-50, -50, 100, 100)
        red_ellipse.setPen(QPen(Qt.red))
        view.scene().addItem(red_ellipse)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

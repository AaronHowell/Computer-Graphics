# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 536)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.clean = QPushButton(self.centralwidget)
        self.clean.setObjectName(u"clean")

        self.verticalLayout.addWidget(self.clean)

        self.dda = QPushButton(self.centralwidget)
        self.dda.setObjectName(u"dda")

        self.verticalLayout.addWidget(self.dda)

        self.bres = QPushButton(self.centralwidget)
        self.bres.setObjectName(u"bres")

        self.verticalLayout.addWidget(self.bres)

        self.mpc = QPushButton(self.centralwidget)
        self.mpc.setObjectName(u"mpc")

        self.verticalLayout.addWidget(self.mpc)

        self.brc = QPushButton(self.centralwidget)
        self.brc.setObjectName(u"brc")

        self.verticalLayout.addWidget(self.brc)

        self.meli = QPushButton(self.centralwidget)
        self.meli.setObjectName(u"meli")

        self.verticalLayout.addWidget(self.meli)

        self.ex3_1 = QPushButton(self.centralwidget)
        self.ex3_1.setObjectName(u"ex3_1")

        self.verticalLayout.addWidget(self.ex3_1)

        self.ex4 = QPushButton(self.centralwidget)
        self.ex4.setObjectName(u"ex4")

        self.verticalLayout.addWidget(self.ex4)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout.addWidget(self.graphicsView)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8ba1\u7b97\u673a\u56fe\u5f62\u5b66-CQU", None))
        self.clean.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u5168\u90e8", None))
        self.dda.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u7ebfDDA", None))
        self.bres.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u7ebfBresenham", None))
        self.mpc.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u70b9\u753b\u5706", None))
        self.brc.setText(QCoreApplication.translate("MainWindow", u"\u5706Bresenham", None))
        self.meli.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u70b9\u692d\u5706", None))
        self.ex3_1.setText(QCoreApplication.translate("MainWindow", u"\u79cd\u5b50\u6cd5", None))
        self.ex4.setText(QCoreApplication.translate("MainWindow", u"Cohen_Sutherland", None))
    # retranslateUi


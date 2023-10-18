from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from lineDialog import Ui_Dialog


class lineD(Ui_Dialog,QDialog):
    infoSignal = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.numRegex=QRegExp(r"-?\d*")
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.emitlineInfo)
        self.SetRegex()

    def emitlineInfo(self):
        try:
            self.infoSignal.emit([int(self.lineEdit.text()),int(self.lineEdit_2.text()),
                    int(self.lineEdit_3.text()),int(self.lineEdit_4.text())])
        except Exception as e:
            QMessageBox.warning(self,'Error',f'{str(e)}')

    def SetRegex(self):
        validator = QRegExpValidator(self.numRegex)
        self.lineEdit.setValidator(validator)
        self.lineEdit_2.setValidator(validator)
        self.lineEdit_3.setValidator(validator)
        self.lineEdit_4.setValidator(validator)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = lineD()
    dialog.exec_()
    sys.exit(app.exec_())
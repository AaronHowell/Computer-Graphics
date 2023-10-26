from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from Polygondialog import Ui_Dialog


class PolygonDialog(Ui_Dialog, QDialog):
    PolyinfoSignal = pyqtSignal(list,list)

    def __init__(self):
        super().__init__()
        self.numRegex = QRegExp(r"^-?\d+(,-?\d+)*$")
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.emitlineInfo)
        self.SetRegex()

    def emitlineInfo(self):
        try:
            input_list_x = self.lineEdit.text().split(',')
            input_list_x =[int(x) for x in input_list_x]
            input_list_y = self.lineEdit_2.text().split(',')
            input_list_y = [int(x) for x in input_list_y]
            if len(input_list_x)==len(input_list_y):
                self.PolyinfoSignal.emit(input_list_x,input_list_y)
            else:
                QMessageBox.warning(self, 'Error', f'Mismatched x and y coordinates')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'{str(e)}')

    def SetRegex(self):
        validator = QRegExpValidator(self.numRegex)
        self.lineEdit.setValidator(validator)
        self.lineEdit_2.setValidator(validator)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = PolygonDialog()
    dialog.exec_()
    sys.exit(app.exec_())

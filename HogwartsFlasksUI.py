from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox, \
    QRadioButton, QFrame


class HogCtrlWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hogwarts Flasks Control")
        # Top switch
        lblModeInfo = QLabel("Режим: автоматический из гуглотаблицы или ручной ввод")
        self.rbtnSheet = QRadioButton("Из гуглотаблицы")
        rbtnManual = QRadioButton("Ручной ввод")
        rbtnManual.setChecked(True)
        lt_Mode = QVBoxLayout()
        lt_Mode.addWidget(lblModeInfo)
        lt_Mode.addWidget(self.rbtnSheet)
        lt_Mode.addWidget(rbtnManual)

        # Global layout
        lt_main = QVBoxLayout()
        lt_main.addLayout(lt_Mode)
        self.setLayout(lt_main)
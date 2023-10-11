from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox, \
    QRadioButton, QFrame, QGroupBox, QCheckBox, QSpacerItem, QSizePolicy


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)

class HogCtrlWindow(QtWidgets.QWidget):
    def OnModeChange(self):
        if self.rbtnSheet.isChecked():
            if not self.cbSheetPollEn.isEnabled():
                self.cbSheetPollEn.setChecked(False)
                self.cbSheetPollEn.setEnabled(True)
                self.gbManual.setEnabled(False)
        else:
            self.cbSheetPollEn.setChecked(False)
            self.cbSheetPollEn.setEnabled(False)
            self.gbManual.setEnabled(True)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hogwarts Flasks Control")

        # Top switch
        gb1 = QGroupBox("Режим")
        self.rbtnSheet = QRadioButton("Автоматический из гуглотаблицы")
        self.rbtnSheet.clicked.connect(self.OnModeChange)
        rbtnManual = QRadioButton("Ручной ввод")
        rbtnManual.setChecked(True)
        rbtnManual.clicked.connect(self.OnModeChange)
        lt_Mode = QVBoxLayout()
        lt_Mode.addWidget(self.rbtnSheet)
        lt_Mode.addWidget(rbtnManual)
        gb1.setLayout(lt_Mode)

        # Googlesheet settings
        gb2 = QGroupBox("Настройки гуглотаблицы")
        lblUrl = QLabel("URL таблицы:")
        self.edSheetUrl = QLineEdit("https://docs.google.com/spreadsheets/d/15dcdgj4wC7PxBiPrd3yXb1rx570sCtQEPsK_vzpmmoA/edit?usp=sharing")
        self.cbSheetPollEn = QCheckBox("Включить опрос")
        self.cbSheetPollEn.setChecked(False)
        self.cbSheetPollEn.setEnabled(False)
        lt_gsheet = QGridLayout()
        lt_gsheet.addWidget(lblUrl, 0, 0)
        lt_gsheet.addWidget(self.edSheetUrl, 0, 1)
        lt_gsheet.addWidget(self.cbSheetPollEn, 1, 0)
        gb2.setLayout(lt_gsheet)

        # Manual values
        self.gbManual = QGroupBox("Ручной ввод баллов")
        self.edGrif = QLineEdit("0")
        self.edGrif.setMaximumSize(54, 20)
        self.edSlyze = QLineEdit("0")
        self.edSlyze.setMaximumSize(54, 20)
        self.edRave = QLineEdit("0")
        self.edRave.setMaximumSize(54, 20)
        self.edHuff = QLineEdit("0")
        self.edHuff.setMaximumSize(54, 20)
        self.btnApply = QPushButton("Применить")
        lt_Manual = QGridLayout()
        lt_Manual.addWidget(QLabel('Введите нужные значения и нажмите "Применить"'), 0, 0, 1, 4)
        lt_Manual.addWidget(QLabel("Гриффиндор"), 1, 0)
        lt_Manual.addWidget(QLabel("Слизерин"), 1, 1)
        lt_Manual.addWidget(QLabel("Рэйвенкло"), 1, 2)
        lt_Manual.addWidget(QLabel("Хаффлпафф"), 1, 3)
        lt_Manual.addWidget(self.edGrif, 2, 0)
        lt_Manual.addWidget(self.edSlyze, 2, 1)
        lt_Manual.addWidget(self.edRave, 2, 2)
        lt_Manual.addWidget(self.edHuff, 2, 3)
        lt_Manual.addWidget(self.btnApply, 3, 0, 1, 4)
        self.gbManual.setLayout(lt_Manual)

        # Current values
        gb4 = QGroupBox("Текущие значения баллов")
        self.lblGrif = QLabel("0")
        self.lblSlyze = QLabel("0")
        self.lblRave = QLabel("0")
        self.lblHuff = QLabel("0")
        lt_CurVal = QGridLayout()
        lt_CurVal.addWidget(QLabel("Гриффиндор"), 0, 0)
        lt_CurVal.addWidget(QLabel("Слизерин"), 0, 1)
        lt_CurVal.addWidget(QLabel("Рэйвенкло"), 0, 2)
        lt_CurVal.addWidget(QLabel("Хаффлпафф"), 0, 3)
        lt_CurVal.addWidget(self.lblGrif, 1, 0)
        lt_CurVal.addWidget(self.lblSlyze, 1, 1)
        lt_CurVal.addWidget(self.lblRave, 1, 2)
        lt_CurVal.addWidget(self.lblHuff, 1, 3)
        gb4.setLayout(lt_CurVal)

        # Global layout
        lt_main = QVBoxLayout()
        lt_main.addWidget(gb1)
        lt_main.addWidget(gb2)
        lt_main.addWidget(self.gbManual)
        lt_main.addWidget(gb4)
        self.setLayout(lt_main)

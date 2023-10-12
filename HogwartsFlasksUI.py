from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox, \
    QRadioButton, QFrame, QGroupBox, QCheckBox, QSpacerItem, QSizePolicy
from CmdUart import CmdUart


Uart = CmdUart()

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

def TryConvert(txt: str):
    try:
        if txt.isnumeric():
            v = int(txt)
            return v
    except ValueError:
        pass
    return None

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

    def SendPoints(self, pg, ps, pr, ph):
        for i in range(0, 3):
            rpl = Uart.send_cmd_and_get_reply("set {0} {1} {2} {3}".format(pg, ps, pr, ph))
            print(rpl)
            if "ok" in rpl.lower():
                self.lblSta.setText("Ok")
                self.lblGrif.setText(str(pg))
                self.lblSlyze.setText(str(ps))
                self.lblRave.setText(str(pr))
                self.lblHuff.setText(str(ph))
                return True
        self.lblSta.setText("Sending fail")
        return False

    def OnApply(self):
        try:
            pg = int(self.edGrif.text())
            ps = int(self.edSlyze.text())
            pr = int(self.edRave.text())
            ph = int(self.edHuff.text())
        except ValueError:
            return
        self.SendPoints(pg, ps, pr, ph)

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
        # self.edSheetUrl = QLineEdit("https://docs.google.com/spreadsheets/d/15dcdgj4wC7PxBiPrd3yXb1rx570sCtQEPsK_vzpmmoA/edit?usp=sharing")
        self.edSheetUrl = QLineEdit("https://docs.google.com/spreadsheets/d/1VP880oA1ZxCTcJISrknymbvjjjLUlh9lBMdLnXp3d3Y/edit?usp=sharing")
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
        self.btnApply.clicked.connect(self.OnApply)
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

        # Bottom status line
        self.lblSta = QLabel()

        # Global layout
        lt_main = QVBoxLayout()
        lt_main.addWidget(gb1)
        lt_main.addWidget(gb2)
        lt_main.addWidget(self.gbManual)
        lt_main.addWidget(gb4)
        lt_main.addWidget(self.lblSta)

        self.setLayout(lt_main)

        if Uart.find_port():
            self.lblSta.setText("Device found at " + Uart.ser.port)
        else:
            print("Device not found")
            QMessageBox.critical(self, "Not Found", "Device not found")

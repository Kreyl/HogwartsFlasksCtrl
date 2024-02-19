from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QMessageBox, \
    QRadioButton, QFrame, QGroupBox, QCheckBox
from PyQt5.QtGui import QIntValidator
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
        if self.rbtnServer.isChecked():
            if not self.cbServerPollEn.isEnabled():
                self.cbServerPollEn.setChecked(False)
                self.cbServerPollEn.setEnabled(True)
                self.gbManual.setEnabled(False)
        else:
            self.cbServerPollEn.setChecked(False)
            self.cbServerPollEn.setEnabled(False)
            self.gbManual.setEnabled(True)

    def SendPoints(self, pg, ps, pr, ph):
        # Try several times
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

    def GetPoints(self):
        return int(self.lblGrif.text()), int(self.lblSlyze.text()), int(self.lblRave.text()), int(self.lblHuff.text())

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
        self.rbtnServer = QRadioButton("Автоматический с сервера")
        self.rbtnServer.clicked.connect(self.OnModeChange)
        rbtnManual = QRadioButton("Ручной ввод")
        rbtnManual.setChecked(True)
        rbtnManual.clicked.connect(self.OnModeChange)
        lt_Mode = QVBoxLayout()
        lt_Mode.addWidget(self.rbtnServer)
        lt_Mode.addWidget(rbtnManual)
        gb1.setLayout(lt_Mode)

        # ==== Remote settings ====
        gb2 = QGroupBox("Настройки сервера")
        lblUrl = QLabel("URL:")
        self.edServerUrl = QLineEdit("http://158.160.52.182:8050/get-scores")
        # Request period
        lblReqPeriod = QLabel("Период опроса:")
        self.edReqPeriod = QLineEdit("11")
        self.edReqPeriod.setValidator(QIntValidator(1, 999, self))
        lblSeconds = QLabel("с")
        # Request timeout
        lblReqTimeout = QLabel("Request Timeout:")
        self.edReqTimeout = QLineEdit("9")
        self.edReqTimeout.setValidator(QIntValidator(1, 999, self))
        lblReqTimeoutSeconds = QLabel("s")
        # Poll enable
        self.cbServerPollEn = QCheckBox("Включить опрос")
        self.cbServerPollEn.setChecked(False)
        self.cbServerPollEn.setEnabled(False)
        lt_gsheet = QGridLayout()
        # Url
        lt_gsheet.addWidget(lblUrl, 0, 0, 1, 1)
        lt_gsheet.addWidget(self.edServerUrl, 0, 1, 1, 2)
        # Period
        lt_gsheet.addWidget(lblReqPeriod, 1, 0)
        lt_gsheet.addWidget(self.edReqPeriod, 1, 1)
        lt_gsheet.addWidget(lblSeconds, 1, 2)
        # Timeout
        lt_gsheet.addWidget(lblReqTimeout, 2, 0)
        lt_gsheet.addWidget(self.edReqTimeout, 2, 1)
        lt_gsheet.addWidget(lblReqTimeoutSeconds, 2, 2)
        # Switch
        lt_gsheet.addWidget(self.cbServerPollEn, 3, 0, 1, 2)
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

        # Try to connect
        if Uart.find_port():
            self.lblSta.setText("Device found at " + Uart.ser.port)
        else:
            self.lblSta.setText("Device not found")
            print("Device not found")
            # QMessageBox.critical(self, "Not Found", "Device not found")

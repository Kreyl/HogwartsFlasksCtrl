import time
from GSheetReader import GSheetRdr
from PyQt5 import QtWidgets
from HogwartsFlasksUI import HogCtrlWindow
import threading

GRdr = GSheetRdr()


def thd_auto_func(win: HogCtrlWindow):
    was_en = False
    points_grif = -100000
    points_slyze = -100000
    points_rave = -100000
    points_huff = -100000
    while True:
        time.sleep(5) # No more than 60 read requests per user per minute
        if win.cbSheetPollEn.isChecked():
            if not was_en:
                was_en = True
                GRdr.url = win.edSheetUrl.text()
                GRdr.Connect()
            pg = GRdr.GetCellInt('A2')
            if pg is None:
                continue
            ps = GRdr.GetCellInt('B2')
            if ps is None:
                continue
            pr = GRdr.GetCellInt('C2')
            if pr is None:
                continue
            ph = GRdr.GetCellInt('D2')
            if ph is None:
                continue
            # Check if changed
            if pg == points_grif and ps == points_slyze and pr == points_rave and ph == points_huff:
                continue
            points_grif = pg
            points_slyze = ps
            points_rave = pr
            points_huff = ph
            print(points_grif, points_slyze, points_rave, points_huff)
            win.lblGrif.setText(str(points_grif))
            win.lblSlyze.setText(str(points_slyze))
            win.lblRave.setText(str(points_rave))
            win.lblHuff.setText(str(points_huff))

def main():
    app = QtWidgets.QApplication([])
    window = HogCtrlWindow()
    window.show()
    threading.Thread(target=thd_auto_func, args=(window, )).start()

    # if uart.find_port():
    #     window.lblSta.setText("Device found at " + uart.ser.port)
    # else:
    #     print("Device not found")
    #     QMessageBox.critical(window, "Not Found", "Device not found")
    #     return

    app.exec()


if __name__ == "__main__":
    main()
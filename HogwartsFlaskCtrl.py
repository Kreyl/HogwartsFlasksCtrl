import time
from GSheetReader import GSheetRdr
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
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
            # pg = GRdr.GetCellInt('A2')
            # ps = GRdr.GetCellInt('B2')
            # pr = GRdr.GetCellInt('C2')
            # ph = GRdr.GetCellInt('D2')
            pg = GRdr.GetCellInt('G14')
            ps = GRdr.GetCellInt('G15')
            pr = GRdr.GetCellInt('G17')
            ph = GRdr.GetCellInt('G16')
            if pg is None or ps is None or pr is None or ph is None:
                continue
            # Check if changed
            if pg == points_grif and ps == points_slyze and pr == points_rave and ph == points_huff:
                continue
            points_grif = pg
            points_slyze = ps
            points_rave = pr
            points_huff = ph
            print(points_grif, points_slyze, points_rave, points_huff)
            win.SendPoints(pg, ps, pr, ph)

def main():
    app = QtWidgets.QApplication([])
    window = HogCtrlWindow()
    window.show()
    threading.Thread(target=thd_auto_func, args=(window, )).start()

    app.exec()


if __name__ == "__main__":
    main()
import time
from GSheetReader import GSheetRdr
from PyQt5 import QtWidgets
from HogwartsFlasksUI import HogCtrlWindow

# GRdr = GSheetRdr()
# GRdr.url = "https://docs.google.com/spreadsheets/d/15dcdgj4wC7PxBiPrd3yXb1rx570sCtQEPsK_vzpmmoA/edit?usp=sharing"

# points_grif = -100000
# points_slyze = -100000
# points_rave = -100000
# points_huff = -100000


# def TryConvert(txt: str):
#     try:
#         if txt.isnumeric():
#             v = int(txt)
#             if 0 <= v <= 255:
#                 return v
#     except ValueError:
#         pass
#     return None


# GRdr.Connect()

# while True:
#     time.sleep(1)
#     pg = GRdr.GetCellInt('A2')
#     if pg is None:
#         continue
#     ps = GRdr.GetCellInt('B2')
#     if ps is None:
#         continue
#     pr = GRdr.GetCellInt('C2')
#     if pr is None:
#         continue
#     ph = GRdr.GetCellInt('D2')
#     if ph is None:
#         continue
#
#     # Check if changed
#     if pg == points_grif and ps == points_slyze and pr == points_rave and ph == points_huff:
#         continue
#
#     points_grif = pg
#     points_slyze = ps
#     points_rave = pr
#     points_huff = ph
#
#     print(points_grif, points_slyze, points_rave, points_huff)


def main():
    app = QtWidgets.QApplication([])
    window = HogCtrlWindow()
    window.show()

    # if uart.find_port():
    #     window.lblSta.setText("Device found at " + uart.ser.port)
    # else:
    #     print("Device not found")
    #     QMessageBox.critical(window, "Not Found", "Device not found")
    #     return

    app.exec()


if __name__ == "__main__":
    main()
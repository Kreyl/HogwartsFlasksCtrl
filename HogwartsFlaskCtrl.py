import json
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from HogwartsFlasksUI import HogCtrlWindow
import threading
import requests

PointsMinValue = -999
PointsMaxValue = 9999


def thd_auto_func(win: HogCtrlWindow):
    was_active = False
    while True:
        if win.cbServerPollEn.isChecked():
            period = int(win.edReqPeriod.text())
            if period < 1:
                period = 1
            # Do not sleep after enabling
            if was_active:
                print(f"Sleeping {period} s.")
                time.sleep(period)
                # Check again: may be unchecked when sleeping
                if not win.cbServerPollEn.isChecked():
                    continue
            else:
                was_active = True

            # Send request
            print("Requesting...")
            rtimeout = int(win.edReqTimeout.text())
            if rtimeout < 1:
                rtimeout = 1
            try:
                response = requests.get(win.edServerUrl.text(), timeout=rtimeout)
                # response = requests.get(win.edServerUrl.text(), timeout=9)
            except Exception as e:
                win.lblSta.setText("Request failed")
                print("Request exception: {0} {1!r}".format(type(e).__name__, e.args))
                pass
                continue
            # Request succeded somehow
            if response.status_code == 200:
                try:
                    jsonstr = response.json()
                    print(jsonstr)
                    win.lblSta.setText(jsonstr)
                    jpoints = json.loads(jsonstr)
                    srvg = int(jpoints["Grif"])
                    srvs = int(jpoints["Slyze"])
                    srvr = int(jpoints["Rave"])
                    srvh = int(jpoints["Huff"])
                    # Get current values and check if changed
                    currg, currs, currr, currh = win.GetPoints()
                    if currg == srvg and currs == srvs and currr == srvr and currh == srvh:
                        print("Not changed.")
                    else:
                        # print(points_grif, points_slyze, points_rave, points_huff)
                        win.SendPoints(srvg, srvs, srvr, srvh)
                except ValueError:
                    print("Error parsing json")
                    pass
            else:  # if response.status_code == 200
                win.lblSta.setText("Error getting data: {}".format(response.status_code))
        else:  # if win.cbServerPollEn.isChecked()
            was_active = False
            time.sleep(1)


def main():
    app = QtWidgets.QApplication([])
    window = HogCtrlWindow()
    window.show()
    threading.Thread(target=thd_auto_func, args=(window,)).start()

    app.exec()


if __name__ == "__main__":
    main()

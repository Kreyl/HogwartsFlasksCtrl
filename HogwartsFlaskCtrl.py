import json
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from HogwartsFlasksUI import HogCtrlWindow
import threading
import requests

PointsMinValue = -999
PointsMaxValue = 9999


def ThdAutoFunc(win: HogCtrlWindow):
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
                srv_response = requests.get(win.edServerUrl.text(), timeout=rtimeout)
            except Exception as e:
                win.lblSta.setText("Request failed")
                print("Request exception: {0} {1!r}".format(type(e).__name__, e.args))
                pass
                continue
            # Request succeded somehow
            if srv_response.status_code == 200:
                try:
                    jsonstr = srv_response.json()
                    print(jsonstr)
                    win.lblSta.setText(jsonstr)
                    jpoints = json.loads(jsonstr)
                    srvg = int(jpoints["Grif"])
                    srvs = int(jpoints["Slyze"])
                    srvr = int(jpoints["Rave"])
                    srvh = int(jpoints["Huff"])
                    jshow_points = jpoints.get("ShowPoints")
                    srv_show_points = 1
                    if jshow_points is not None:
                        srv_show_points = 0 if int(jshow_points) == 0 else 1
                    # Get current values and check if changed
                    currg, currs, currr, currh = win.GetPoints()
                    win_show_points = 1 if win.points_are_shown else 0
                    if (currg == srvg and currs == srvs and currr == srvr and currh == srvh and
                            win_show_points == srv_show_points):
                        print("Not changed.")
                    else:
                        # print(points_grif, points_slyze, points_rave, points_huff)
                        win.SendPoints(srvg, srvs, srvr, srvh, srv_show_points)
                except ValueError:
                    print("Error parsing json")
                    pass
            else:  # if response.status_code == 200
                win.lblSta.setText("Error getting data: {}".format(srv_response.status_code))
        else:  # if win.cbServerPollEn.isChecked()
            was_active = False
            time.sleep(1)


def main():
    app = QtWidgets.QApplication([])
    window = HogCtrlWindow()
    window.show()
    threading.Thread(target=ThdAutoFunc, args=(window,)).start()

    app.exec()


if __name__ == "__main__":
    main()

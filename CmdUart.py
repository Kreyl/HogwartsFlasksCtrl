import time

import serial
import serial.tools.list_ports
from typing import Optional, List


def GetComportsList() -> List[str]:
    """
    scans COM ports and returns their list
    :return: list of available COM ports
    """
    return [comport.device for comport in serial.tools.list_ports.comports()]


class CmdUart:
    ser = serial.Serial()

    def __init__(self):
        self.ser.baudrate = 115200
        self.ser.write_timeout = 0.2
        self.ser.timeout = 1

    def SendCmdAndGetReply(self, cmd: str):
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            cmd += "\r\n"
            bcmd: bytes = bytes(cmd, encoding='cp1251')
            self.ser.write(bcmd)
            self.ser.flush()
            # Get answer
            while True:
                reply: str = self.ser.readline().decode('cp1251').strip()
                if reply:
                    return reply
                else:
                    return ""
        except (OSError, serial.SerialException):
            return ""

    def SendCmdAndGetReplyStartingWith(self, cmd: str, rpl_start: str, timeout_s):
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            cmd += "\r\n"
            bcmd: bytes = bytes(cmd, encoding='cp1251')
            self.ser.write(bcmd)
            self.ser.flush()
            # Get answer
            rpl_list = []
            time_start = time.time()
            while time.time() - time_start < timeout_s:
                reply: str = self.ser.readline().decode('cp1251').strip()
                rpl_list.append(reply)
                if reply.lower().startswith(rpl_start.lower()):
                    break
            return rpl_list
        except (OSError, serial.SerialException):
            return []

    def SendCmdAndGetOk(self, cmd: str, try_cnt=1):
        while try_cnt:
            try_cnt -= 1
            answer: str = self.SendCmdAndGetReply(cmd)
            # print("{0} {1}".format(cmd, answer))
            if answer.lower().strip() == 'ok':
                return True
        return False

    def CheckPort(self, port_name: str):
        # print([comport.device for comport in serial.tools.list_ports.comports()])
        if port_name:
            try:
                self.ser.port = port_name
                self.ser.open()
                if self.SendCmdAndGetOk('Ping', 2):
                    print("Device found at {0}".format(port_name))
                    return True
                self.ser.close()
            except (OSError, serial.SerialException):
                pass
        return False

    def FindPort(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if self.CheckPort(port.device):
                return True
        return False

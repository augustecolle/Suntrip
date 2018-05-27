import socket
import time
import sys
import select


class connection():

    def __init__(self, ip_, port_):
        self.socket = socket.socket()
        # self.socket.setblocking(0)  # for timeout
        self.dir_ip = ip_
        self.port = port_
        self.timeout = 2.           # in seconds

    def connect(self):
        try:
            self.socket.connect((self.dir_ip, self.port))
            return True
        except:
            print(sys.exc_info())
            print("Could not connect")
            return False

    def send_command(self, command):
        try:
            self.socket.sendall(command.encode())
            return True
        except:
            print(sys.exc_info())
            print("Failed to send command")
            return False

    def read_answer(self):
        try:
            ready = select.select([self.socket], [], [], self.timeout)
            if ready[0]:
                res = self.socket.recv(100)
                return res.decode().strip()
            else:
                print("Timeout")
                return False
        except:
            print(sys.exc_info())
            print("Failed to receive answer")
            return False


class multimeter():

    def __init__(self, ipaddr, port):
        self.sc = connection(ipaddr, port)
        self.sc.connect()
        self.sc.send_command("SYST:REM\n")
        time.sleep(1.0)

    def getVoltage(self, range):
        self.sc.send_command("MEAS:VOLT:DC? "+str(range)+"\n")
        volts = self.sc.read_answer()
        if volts is not "":
            return float(volts)
        else:
            volts = self.sc.read_answer()
            if volts is not "":
                return float(volts)
            else:
                return False

    def getCurrent(self, range):
        self.sc.send_command("MEAS:CURR:DC? "+str(range)+"\n")
        amps = self.sc.read_answer()
        if amps is not "":
            return float(amps)
        else:
            amps = self.sc.read_answer()
            if amps is not "":
                return float(amps)
            else:
                return False

import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from window import *
import datetime
import serial.tools.list_ports
from settings import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)

        self.returnVal = {}

        self.ui.actionSettings.triggered.connect(self.config)
        self.ui.pushButton.clicked.connect(self.go)
        self.ui.pushButton_2.clicked.connect(self.stop)

    def config(self):
        self.dialog = SettingsDialog()
        response = self.dialog.exec_()
        if(response):
            self.ui.pushButton.setEnabled(True)
            self.returnVal = self.dialog.get_data()

    def go(self):
        self.th = MyThread(self.returnVal)
        self.th.sig.connect(self.data)
        self.th.start()
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(True)

    def stop(self):
        self.th.exit()
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(False)


    def data(self, tmp):
        temperature = (tmp.split('_'))[0] + '°C'
        humidity = ((tmp.split('_'))[1])[0:5] + '%'
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.textEdit.append(f"{date_time}\n{temperature}\n")
        self.ui.textEdit_2.append(f"{date_time}\n{humidity}\n")
        self.ui.textEdit_3.setPlainText(f"{date_time}\nTemperature:{temperature}\nHumidity:{humidity}")


class MyThread(QThread):
    sig = pyqtSignal(str)
    def __init__(self, com_data):
        super().__init__()
        self.com_port = com_data['com_port']
        self.baud_rate = com_data['baud_rate']
        self.data_bits = com_data['data_bits']
        self.serialInst = serial.Serial()
    
    def run(self):
        self.serialInst.baudrate = self.baud_rate
        self.serialInst.port = self.com_port
        self.serialInst.data_bit = self.data_bits
        self.serialInst.open()

        while True:
            if self.serialInst.in_waiting:
                packet = self.serialInst.readline()
                self.sig.emit(packet.decode('utf').rstrip('\n'))

    def exit(self):
        self.terminate()
        if self.serialInst.is_open:
            self.serialInst.close()
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

from dialog import *
from PyQt5.QtWidgets import QDialog
import serial


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.pushButton.clicked.connect(self.accept)
        ports = serial.tools.list_ports.comports()
        for i in ports:
            self.dialog.comboBox.addItem(str(i.device))
        self.returnVal = {}


    def get_data(self):
        self.returnVal['com_port'] = self.dialog.comboBox.currentText()
        self.returnVal['baud_rate'] = int(self.dialog.comboBox_2.currentText())

        tmp = self.dialog.comboBox_3.currentText()
        if(tmp == '5'):
            self.returnVal['data_bits'] = serial.FIVEBITS
        if(tmp == '6'):
            self.returnVal['data_bits'] = serial.SIXBITS
        if(tmp == '7'):
            self.returnVal['data_bits'] = serial.SEVENBITS
        if(tmp == '8'):
            self.returnVal['data_bits'] = serial.EIGHTBITS

        return self.returnVal   
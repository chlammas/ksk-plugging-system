from handlers.excel_handler import load_ksk
from handlers.image_hanler import generate_ksk_images
import os


import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setStyleSheet(
            "background-color: #074143;color:#d2e9e3;font-size:18px")
        self.grid = QGridLayout()
        gb1 = self.createSecondGroup("traitement de donnees")

        button1 = QPushButton(gb1)
        button1.setText("Browse")
        button1.move(560, 45)
        button1.clicked.connect(self.browsefiles)
        button1.setStyleSheet("background-color :#2c3532;")
        # b0a295;
        button2 = QPushButton(gb1)
        button2.setText("Generate")
        button2.move(670, 45)
        button2.clicked.connect(self.generate_data)
        button2.setStyleSheet("background-color :#2c3532;")
        self.textbox = QLineEdit(gb1)
        self.textbox.setGeometry(200, 45, 350, 30)
        self.textbox.setStyleSheet(
            "background-color :#2c3532;border :1px solid #d2e9e3")

        self.grid.addWidget(gb1, 0, 0, 2, 5)
        gb2 = self.createExampleGroup("Plugs")
        self.grid.addWidget(gb2, 3, 4, 9, 1)
        self.setLayout(self.grid)
        # button2 = QPushButton(gb")
        # button2.move(670, 45)
        self.setWindowTitle("PyQt5 Group Box")
        self.showMaximized()

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv, *.xlsx)')
        self.textbox.setText(fname[0])
        return fname[0]

    def generate_data(self):
        ksk_path = self.textbox.text()
        ksk_data = load_ksk(ksk_path,
                            "input/data/wire_list.xlsx", 1)
        generate_ksk_images(*ksk_data)
        gb3 = self.createExampleGroup("connectors")
        self.grid.addWidget(gb3, 3, 0, 9, 4)

    def createExampleGroup(self, name=""):
        groupBox = QGroupBox(name)
        # groupBox.setGeometry(QRect(*size))
        vbox = QGridLayout()
        position = [(0, 0), (0, 1), (1, 0), (1, 1)]
        images = []
        if name == "Plugs":
            images.append("input/images/bc.png")
        else:
            for img_name in os.listdir('output'):
                images.append('output/' + img_name)

        for index in range(len(images)):
            row, column = position[index-1]
            vbox.addWidget(self.createSecondGroup(
                "", images[index-1]), row, column)
            # vbox.addWidget(radio2)
            # vbox.addWidget(radio3)
            groupBox.setLayout(vbox)

        return groupBox

    def createSecondGroup(self, name="", image=""):
        groupBox = QGroupBox(name)
        groupBox.setGeometry(QRect(660, 100, 120, 321))
        if image != "":
            # creating label
            label = QLabel(groupBox)
            # loading image
            pixmap1 = QPixmap(image)
            # adding image to label
            label.setPixmap(pixmap1)
            label.setScaledContents(True)
            label.resize(540, 250)

        #groupBox.setStyleSheet("background: url(" + image + ") no-repeat;")
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())

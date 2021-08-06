import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from handlers.excel_handler import load_ksk_list
from handlers.ouput_handler import get_ksk, search_for_ksk, dump_ksk_object
from second_app import SecondWindow


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.main_grid = QGridLayout()

        file_selection_gb = self.createChildGroup("Files selection")
        # file_selection_gb.setStyleSheet('border:2px solid #b2384f;color:#b2384f')
        self.ksk_WCC_btn = QPushButton(file_selection_gb)
        self.ksk_WCC_btn.setText("Browse")
        self.ksk_WCC_btn.setEnabled(False)
        self.ksk_WCC_btn.move(430, 160)
        self.ksk_WCC_btn.clicked.connect(self.browseWCC)
        self.ksk_WCC_btn.setStyleSheet("background-color :#fbeec1;color:black")
        
        label= QLabel(file_selection_gb)
            # loading image
        pixmap1 = QPixmap('input/images/im.png')   
        # adding image to label
        label.setPixmap(pixmap1)
        # print(pixmap1.size())
        label.setScaledContents(True)
        label.setGeometry(200, 30, 140, 100)

        ksk_file_btn = QPushButton(file_selection_gb)
        ksk_file_btn.setText("Browse")
        ksk_file_btn.move(430, 270)
        ksk_file_btn.clicked.connect(self.browsefile)
        ksk_file_btn.setStyleSheet("background-color :#fbeec1;color:black")

        generate_btn = QPushButton(file_selection_gb)
        generate_btn.setText("Generate")
        # generate_btn.move()(100, 210,300,120)
        generate_btn.setGeometry(140, 320,200,40)
        generate_btn.clicked.connect(self.generate_data)
        generate_btn.setStyleSheet("background-color :#1b3320;color:#fbeec1")

        figure_generate_btn = QPushButton(file_selection_gb)
        figure_generate_btn.setText("Connect as an operator")
        # figure_generate_btn.move()(100, 210,300,120)
        figure_generate_btn.setGeometry(350, 400,200,60)
        figure_generate_btn.clicked.connect(self.generate_data)
        figure_generate_btn.setStyleSheet("background-color :#bd986b;color:black")
        self.WCC_path_box = QLineEdit(file_selection_gb)
        self.WCC_path_box.setText("input/data/wire_list.xlsx")
        self.WCC_path_box.setReadOnly(True)
        self.WCC_path_box.setGeometry(60, 160, 350, 30)
        self.WCC_path_box.setStyleSheet(
            "background-color :#fbeec1;border :1px solid #d2e9e3;color:black;font-size:16px")
        # self.layout = QHBoxLayout(file_selection_gb)
        self.unlock_box = QCheckBox(file_selection_gb)
        self.unlock_box.setText('I want change wcc file')
        self.unlock_box.setGeometry(120, 190, 350, 30)
        self.unlock_box.setStyleSheet("font-size:18px")
        # self.unlock_box.setChecked(True)
        self.unlock_box.stateChanged.connect(self.change_editline_state)

        label1 = QLabel(file_selection_gb)
        label2 = QLabel(file_selection_gb)
        label1.setGeometry(60, 130, 350, 30)
        label1.setText('Select wire list file :')
        label1.setStyleSheet("color:black;font-size:18px")
        label2.setGeometry(60, 240, 350, 30)
        label2.setText('Select ksk file :')
        label2.setStyleSheet("color:black;font-size:18px")
       
        self.ksk_path_box = QLineEdit(file_selection_gb)
        self.ksk_path_box.setGeometry(60, 270, 350, 30)
        self.ksk_path_box.setStyleSheet(
            "background-color :#fbeec1;border :1px solid #d2e9e3;color:black;font-size:16px")

        self.main_grid.addWidget(file_selection_gb, 0, 0, 2, 5)

        

        self.setWindowTitle("Plugging System")
        self.setStyleSheet(
            "background-color: #659ebc;color:black;font-size:18px")
            #074143
        self.setLayout(self.main_grid)
        # self.showMaximized()

    def browsefile(self):
        """ Get a file path and put it in a textbox """
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv, *.xlsx)')
        self.ksk_path_box.setText(fname[0])

    def browseWCC(self):
        """ Get a file path and put it in a textbox """
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv, *.xlsx)')
        self.WCC_path_box.setText(fname[0])
    def initUI(self):
        self.setWindowTitle('Centering')
        self.resize(600, 500)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def change_editline_state(self):
    
        self.WCC_path_box.setReadOnly(not self.WCC_path_box.isReadOnly())
        self.ksk_WCC_btn.setEnabled(not self.ksk_WCC_btn.isEnabled())

    def generate_data(self):
        """load KSK's data from a file into an object then pickle it"""
        Wcc_path=self.WCC_path_box.text()
        ksk_path = self.ksk_path_box.text()
        all_ksk = load_ksk_list(ksk_path,Wcc_path)
        dump_ksk_object(all_ksk)
        self.wm = SecondWindow()
        self.wm.show()


    def createChildGroup(self, name="", image=""):
        groupBox = QGroupBox(name)
        groupBox.setGeometry(QRect(660, 100, 120, 321))
        if image != "":
            label = QLabel(groupBox)
            pixmap1 = QPixmap(image)
            label.setPixmap(pixmap1)
            label.setScaledContents(True)
            label.resize(540, 250)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = MainWindow()
    clock.show()
    sys.exit(app.exec_())
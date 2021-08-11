import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from handlers.excel_handler import load_KSK_list
from handlers.ouput_handler import get_KSK, search_for_KSK, dump_KSK_object
from second_app import SecondWindow


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

        file_selection_gb = self.createChildGroup("Files selection")

        label = QLabel(file_selection_gb)
        pixmap1 = QPixmap('input/images/im.png')
        label.setPixmap(pixmap1)
        label.setScaledContents(True)
        label.setGeometry(200, 30, 140, 100)

        WCC_box_label = QLabel(file_selection_gb)
        WCC_box_label.setGeometry(60, 130, 350, 30)
        WCC_box_label.setText('Select wire list file :')
        WCC_box_label.setStyleSheet("color:black;font-size:18px")

        self.WCC_path_box = QLineEdit(file_selection_gb)
        self.WCC_path_box.setText("input/data/wire_list.xlsx")
        self.WCC_path_box.setReadOnly(True)
        self.WCC_path_box.setGeometry(60, 160, 350, 30)
        self.WCC_path_box.setStyleSheet(
            "background-color :#fbeec1;border :1px solid #d2e9e3;color:black;font-size:16px")

        self.WCC_btn = QPushButton(file_selection_gb)
        self.WCC_btn.setText("Browse")
        self.WCC_btn.setEnabled(False)
        self.WCC_btn.move(430, 160)
        self.WCC_btn.clicked.connect(
            lambda: self.browsefile(self.WCC_path_box))
        self.WCC_btn.setStyleSheet("background-color :#fbeec1;color:black")

        self.unlock_box = QCheckBox(file_selection_gb)
        self.unlock_box.setText('I want change wcc file')
        self.unlock_box.setGeometry(120, 190, 350, 30)
        self.unlock_box.setStyleSheet("font-size:18px")
        self.unlock_box.stateChanged.connect(self.change_WCC_box_state)

        KSK_box_label = QLabel(file_selection_gb)
        KSK_box_label.setGeometry(60, 240, 350, 30)
        KSK_box_label.setText('Select KSK file :')
        KSK_box_label.setStyleSheet("color:black;font-size:18px")

        self.KSK_path_box = QLineEdit(file_selection_gb)
        self.KSK_path_box.setGeometry(60, 270, 350, 30)
        self.KSK_path_box.setStyleSheet(
            "background-color :#fbeec1;border :1px solid #d2e9e3;color:black;font-size:16px")

        KSK_file_btn = QPushButton(file_selection_gb)
        KSK_file_btn.setText("Browse")
        KSK_file_btn.move(430, 270)
        KSK_file_btn.clicked.connect(
            lambda: self.browsefile(self.KSK_path_box))
        KSK_file_btn.setStyleSheet("background-color :#fbeec1;color:black")

        generate_btn = QPushButton(file_selection_gb)
        generate_btn.setText("Generate")
        generate_btn.setGeometry(140, 320, 200, 40)
        generate_btn.clicked.connect(self.generate_data)
        generate_btn.setStyleSheet("background-color :#1b3320;color:#fbeec1")

        figure_generate_btn = QPushButton(file_selection_gb)
        figure_generate_btn.setText("Connect as an operator")
        figure_generate_btn.setGeometry(350, 400, 200, 60)
        figure_generate_btn.clicked.connect(self.show_operator_window)
        figure_generate_btn.setStyleSheet(
            "background-color :#bd986b;color:black")

        self.main_grid.addWidget(file_selection_gb, 0, 0, 2, 5)

    def browsefile(self, textbox):
        """ Get a file path and put it in a textbox """
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv, *.xlsx)')
        textbox.setText(fname[0])

    def initUI(self):
        self.setWindowTitle("Plugging System")
        self.setStyleSheet(
            "background-color: #659ebc;color:black;font-size:18px")
        self.main_grid = QGridLayout()
        self.setLayout(self.main_grid)
        self.resize(600, 500)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def change_WCC_box_state(self):
        self.WCC_path_box.setReadOnly(not self.WCC_path_box.isReadOnly())
        self.WCC_btn.setEnabled(not self.WCC_btn.isEnabled())

    def generate_data(self):
        """load KSK's data from a file into an object then pickle it"""
        Wcc_path = self.WCC_path_box.text()
        KSK_path = self.KSK_path_box.text()
        try:
            all_KSK = load_KSK_list(KSK_path, Wcc_path)
        except ValueError as err:
            QMessageBox.critical(self, "Excel file ", str(err))
        except:
            QMessageBox.critical(self, "Excel file ", 'Something wrong')
        else:
            dump_KSK_object(all_KSK)
            self.KSK_path_box.clear()
            msg = QMessageBox()
            msg.information(self, "Data Generated ",
                            'Data Generated successfuly')

    def show_operator_window(self):
        self.wm = SecondWindow(True)
        self.wm.show()
        self.close()

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

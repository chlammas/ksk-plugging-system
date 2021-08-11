import os
import sys
from typing import Text
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from handlers.excel_handler import load_ksk_list
from handlers.ouput_handler import get_ksk, search_for_ksk


class SecondWindow(QWidget):
    def __init__(self, from_admin=False):
        super(SecondWindow, self).__init__()

        self.main_grid = QGridLayout()
        output_gb = self.createChildGroup("KSK LIST")
        self.main_grid.addWidget(output_gb, 0, 0, 9, 1)

        self.label = QLabel(output_gb)
        self.label.setGeometry(QRect(450, 20, 400, 400))
        self.label.setMinimumSize(QSize(600, 600))
        self.label.setMaximumSize(QSize(600, 600))
        self.label.setObjectName("lb1")

        # Loading the GIF
        self.movie = QMovie("input/images/gif.gif")
        self.label.setMovie(self.movie)
        self.startAnimation()

    # Start Animation

        self.search_box = QLineEdit(output_gb)
        self.search_box.setStyleSheet(
            "background-color :#fbeec1;color:#1b3320;border :1px solid grey")
        self.search_box.setPlaceholderText('Enter your search :')

        self.search_box.setGeometry(10, 30, 240, 30)

        self.list_widget = QListWidget(output_gb)
        self.list_widget.setGeometry(10, 70, 240, 600)
        self.list_widget.setStyleSheet(
            "background-color :#fbeec1;color:#1b3320")
        self.fill_ksk_list_widget()

        self.search_box.textChanged.connect(self.fill_ksk_list_widget)
        self.list_widget.itemClicked.connect(self.show_ksk_images)

        self.setWindowTitle("Plugging System")
        self.setStyleSheet(
            "background-color:#659ebc ;color:#fbeec1;font-size:18px")
        if from_admin:
            back_btn = QPushButton(output_gb)
            back_btn.setGeometry(30, 630, 200, 40)
            back_btn.setStyleSheet("background-color :#bd986b;color:black")
            back_btn.setText('Back')
            self.list_widget.setGeometry(10, 70, 240, 550)
            back_btn.clicked.connect(self.show_admin_window)

        self.setLayout(self.main_grid)
        self.showMaximized()

    def show_admin_window(self):
        from app import MainWindow
        self.wm = MainWindow()
        self.wm.show()
        self.close()

    def show_ksk_images(self, index: int = None):
        """Show up image of each connector of a ksk"""
        ksk_name = ""
        if type(index) == int and 0 <= index < self.list_widget.count():
            ksk_name = self.list_widget.item(index).text()
            self.list_widget.selectedItems().clear()
            self.list_widget.setCurrentRow(index)

        else:
            ksk_name = self.list_widget.selectedItems()[0].text()

        # self.list_widget.selectedItems()[0].setBackground(QColor(244,224,194))
        get_ksk(ksk_name)
        connectors_gb = self.createParentGroup("Connectors")
        self.main_grid.addWidget(connectors_gb, 0, 2, 9, 4)

        next_btn = QPushButton(connectors_gb)
        next_btn.setGeometry(980, 290, 70, 40)
        MyIcon2 = QPixmap('input/images/next.png')
        next_btn.setIcon(QIcon(MyIcon2))
        next_btn.setIconSize(QSize(100, 40))
        # next_btn.setText("next")
        next_btn.setToolTip('next')
        next_btn.setStyleSheet("background-color :#fbeec1;color:#fbeec1")
        next_btn.clicked.connect(lambda: self.show_ksk_images(
            self.list_widget.selectedIndexes()[0].row() + 1))
        # generate_btn.clicked.connect(next_ksk(ksk_name))
        # generate_btn.setStyleSheet("background-color :#1b3320;color:#fbeec1")
        previous_btn = QPushButton(connectors_gb)
        # previous_btn.setText("previous")
        previous_btn.setGeometry(20, 290, 70, 40)
        MyIcon = QPixmap('input/images/previous.png')
        previous_btn.setIcon(QIcon(MyIcon))
        previous_btn.setIconSize(QSize(100, 40))
        previous_btn.setToolTip('Previous')

        previous_btn.setStyleSheet("background-color :#fbeec1;color:#fbeec1")
        previous_btn.clicked.connect(lambda: self.show_ksk_images(
            self.list_widget.selectedIndexes()[0].row() - 1))

    def startAnimation(self):
        self.movie.start()

    def fill_ksk_list_widget(self):
        """Fill up the ksk list widget by ksk names"""
        self.list_widget.clear()
        search_query = self.search_box.text()
        ksk_names = search_for_ksk(search_query)
        for ksk_name in ksk_names:
            QListWidgetItem(ksk_name, self.list_widget)

    def createParentGroup(self, name=""):
        groupBox = QGroupBox(name)
        g_layout = QGridLayout()
        position = [(0, 0), (0, 1), (1, 0), (1, 1)]
        images = []
        for ksk_name in os.listdir('output'):
            ksk_path = f'output/{ksk_name}'
            for index, img_name in enumerate(os.listdir(ksk_path)):
                images.append(f'{ksk_path}/{img_name}')
                row, column = position[index]
                child_box = self.createChildGroup(
                    "", images[index-1])
                child_box.setStyleSheet('border:none')
                g_layout.addWidget(child_box, row, column)
                groupBox.setLayout(g_layout)

        return groupBox

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
    clock = SecondWindow()
    clock.show()
    sys.exit(app.exec_())

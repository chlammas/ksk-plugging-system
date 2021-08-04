import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from handlers.excel_handler import load_ksk_list
from handlers.ouput_handler import get_ksk, search_for_ksk, dump_ksk_object


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.main_grid = QGridLayout()

        file_selection_gb = self.createChildGroup("Files selection")

        ksk_file_btn = QPushButton(file_selection_gb)
        ksk_file_btn.setText("Browse")
        ksk_file_btn.move(560, 45)
        ksk_file_btn.clicked.connect(self.browsefile)
        ksk_file_btn.setStyleSheet("background-color :#2c3532;")

        generate_btn = QPushButton(file_selection_gb)
        generate_btn.setText("Generate")
        generate_btn.move(670, 45)
        generate_btn.clicked.connect(self.generate_data)
        generate_btn.setStyleSheet("background-color :#2c3532;")

        self.ksk_path_box = QLineEdit(file_selection_gb)
        self.ksk_path_box.setGeometry(200, 45, 350, 30)
        self.ksk_path_box.setStyleSheet(
            "background-color :#2c3532;border :1px solid #d2e9e3")

        self.main_grid.addWidget(file_selection_gb, 0, 0, 2, 5)

        output_gb = self.createChildGroup("Output")
        self.main_grid.addWidget(output_gb, 3, 4, 9, 1)

        self.search_box = QLineEdit(output_gb)
        self.search_box.setStyleSheet(
            "background-color :#2c3532;border :1px solid #d2e9e3")
        self.search_box.setGeometry(10, 30, 240, 30)

        self.list_widget = QListWidget(output_gb)
        self.list_widget.setGeometry(10, 70, 240, 460)
        self.fill_ksk_list_widget()

        self.search_box.textChanged.connect(self.fill_ksk_list_widget)
        self.list_widget.itemClicked.connect(self.show_ksk_images)

        self.setWindowTitle("Plugging System")
        self.setStyleSheet(
            "background-color: #074143;color:#d2e9e3;font-size:18px")
        self.setLayout(self.main_grid)
        self.showMaximized()

    def browsefile(self):
        """ Get a file path and put it in a textbox """
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Excel (*.csv, *.xlsx)')
        self.ksk_path_box.setText(fname[0])

    def generate_data(self):
        """load KSK's data from a file into an object then pickle it"""
        ksk_path = self.ksk_path_box.text()
        all_ksk = load_ksk_list(ksk_path,
                                "input/data/wire_list.xlsx")
        dump_ksk_object(all_ksk)

    def show_ksk_images(self):
        """Show up image of each connector of a ksk"""
        ksk_name = self.list_widget.selectedItems()[0].text()
        get_ksk(ksk_name)
        connectors_gb = self.createParentGroup("Connectors")
        self.main_grid.addWidget(connectors_gb, 3, 0, 9, 4)

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
                g_layout.addWidget(self.createChildGroup(
                "", images[index-1]), row, column)
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
    clock = MainWindow()
    clock.show()
    sys.exit(app.exec_())

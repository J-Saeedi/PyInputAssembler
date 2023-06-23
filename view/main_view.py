import sys
from resource.ui_window import Ui_MainWindow
from PyQt5.QtCore import QFileInfo, QSettings, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QApplication, QMainWindow,\
    QFormLayout, QLineEdit, QTabWidget, QWidget, QAction,\
    QFileDialog, QTableWidgetItem, QCheckBox, QGridLayout, QHBoxLayout


class MainWindow(QMainWindow, Ui_MainWindow):
    settings = QSettings("gui.ini", QSettings.IniFormat)

    def __init__(self, application, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.app = application
        self.connect_signals()

    def connect_signals(self):
        self.actionSaveSettings.triggered.connect(self.save)
        self.actionLoadSettings.triggered.connect(self.restore)
        self.pushButton_openCode.clicked.connect(self.open_code_dialog)
        self.pushButton_openExcel.clicked.connect(self.open_excel_dialog)
        self.pushButton_updateScan.clicked.connect(self.app.scan_variables)
        self.pushButton_generate.clicked.connect(self.app.generate_inputs)
        self.pushButton_export.clicked.connect(self.save_excel_dialog)
        # self.pushButton_updateScan.clicked.connect(clear_table)

    def restore(self):
        finfo = QFileInfo(self.settings.fileName())

        if finfo.exists() and finfo.isFile():
            for w in self.app.qapp.allWidgets():
                mo = w.metaObject()
                if w.objectName() != "":
                    for i in range(mo.propertyCount()):
                        name = mo.property(i).name()
                        val = self.settings.value(
                            "{}/{}".format(w.objectName(), name), w.property(name))
                        w.setProperty(name, val)

    def save(self):
        for w in self.app.qapp.allWidgets():
            mo = w.metaObject()
            if w.objectName() != "":
                for i in range(mo.propertyCount()):
                    name = mo.property(i).name()
                    self.settings.setValue(
                        "{}/{}".format(w.objectName(), name), w.property(name))

    def open_code_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Your Code", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.lineEdit_codeAddress.setText(fileName)
            self.app.codeAddress = fileName
            print(fileName)

    def open_excel_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Your Excel Reference Inputs", "", "Microsoft Excel Files (*.xlsx)", options=options)
        if fileName:
            self.lineEdit_excelAddress.setText(fileName)
            self.app.excelAddress = fileName
            print(fileName)  # DELME

    def save_excel_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save Your Excel Reference Inputs", "CaseStudy", "Microsoft Excel Files (*.xlsx)", options=options)
        if fileName:
            self.app.export_generated_inputs(fileName)
            print(fileName)  # DELME

    def clear_table(self):
        self.tableWidget.setRowCount(0)

    def append_new_row(self, header="boob", variable="boob-var"):
        rowCount = self.tableWidget.rowCount()
        header_item = QTableWidgetItem(header)
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setVerticalHeaderItem(rowCount, header_item)

        item = QTableWidgetItem(variable)
        self.tableWidget.setItem(rowCount, 1, item)

        container1 = QWidget()
        box = QGridLayout(container1)
        container1.checkbox = QCheckBox()
        box.setAlignment(Qt.AlignCenter)
        box.addWidget(container1.checkbox)
        self.tableWidget.setCellWidget(rowCount, 0, container1)

        container2 = QWidget()
        box = QHBoxLayout(container2)
        container2.lineEdit_from = QLineEdit()
        container2.lineEdit_to = QLineEdit()
        container2.lineEdit_from.setPlaceholderText("from cell:")
        container2.lineEdit_to.setPlaceholderText("to cell:")
        box.addWidget(container2.lineEdit_from)
        box.addWidget(container2.lineEdit_to)
        self.tableWidget.setCellWidget(rowCount, 2, container2)

        self.tableWidget.resizeRowsToContents()

import sys
import openpyxl
from PyQt5.QtWidgets import QApplication
from view.main_view import MainWindow
from model.code_manipulator import CodeManipulator
from model.variable_combiner import Combiner


class Utility:
    def scan_variables():
        try:
            Application.codeAddress = r"example.py"  # DELME
            variables_list = CodeManipulator.scan_variables(
                Application.codeAddress)
            if variables_list:
                Application.view.clear_table()
            for this in variables_list:
                name, var = this
                Application.view.append_new_row(header=name, variable=var)

        except FileNotFoundError:
            print(
                f"file not found at this address:\n{CodeManipulator.codeAddress}")

    def generate_inputs():
        table_obj = Application.view.tableWidget
        avail_vars = Combiner.find_avaliable_variables(table_obj)

        excel_fileName = Application.excelAddress
        avail_values = Combiner.load_variables_values(
            avail_vars, excel_fileName)
        result = Combiner.combine(avail_values)
        preview = "\n".join(list(map(lambda x: f"input{x}", result)))
        Application.view.plainTextEdit.setPlainText(preview)
        print(result)  # DELME
        Application.generated_inputs = result
        Application.generated_inputs_labels = list(avail_values.keys())
        Application.view.pushButton_export.setEnabled(True)

    def export_generated_inputs(fileName):
        if not (Application.generate_inputs):
            return -1
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.cell(row=1, column=1, value="CaseStudyName")
        for i, label in enumerate(Application.generated_inputs_labels, start=2):
            worksheet.cell(row=1, column=i, value=label)

        for i, value_list in enumerate(Application.generated_inputs, start=2):
            worksheet.cell(row=i, column=1, value="Case"+str(i-1).zfill(8))
            for j, value in enumerate(value_list, start=2):
                worksheet.cell(row=i, column=j, value=value)
        workbook.save(fileName)


class Application(Utility):
    qapp = None
    view = None
    generated_inputs = None
    generated_inputs_labels = None

    @classmethod
    def init_ui(cls):
        cls.qapp = QApplication(sys.argv)
        cls.view = MainWindow(cls)

    def normal_run():
        Application.init_ui()
        Application.view.show()
        sys.exit(Application.qapp.exec())

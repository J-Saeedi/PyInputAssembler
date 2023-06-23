import openpyxl
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
from itertools import product


class Combiner:

    def find_avaliable_variables(table_obj):
        result = []
        rowCount = table_obj.rowCount()
        for row in range(rowCount):
            is_checked = table_obj.cellWidget(row, 0).checkbox.isChecked()
            var_name = table_obj.item(row, 1).text()
            from_cell = table_obj.cellWidget(row, 2).lineEdit_from.text()
            to_cell = table_obj.cellWidget(row, 2).lineEdit_to.text()
            # print(is_checked, var_name, from_cell, to_cell)
            if is_checked:
                result.append((var_name, from_cell, to_cell))
        return result

    def get_col_row_number(string_code):
        xy = coordinate_from_string(string_code)  # returns ('A',4)
        col = column_index_from_string(xy[0])  # returns 1
        row = xy[1]
        return row, col

    def load_variables_values(var_list, excel_fileName):
        results = {}
        try:
            workbook = openpyxl.load_workbook(excel_fileName)
            worksheet = workbook.active
            for var in var_list:
                data_in_range = []
                if (var[1] == "-") or (var[2] == "-"):
                    results[var[0]] = data_in_range
                    continue
                min_row, min_col = Combiner.get_col_row_number(var[1])
                max_row, max_col = Combiner.get_col_row_number(var[2])

                # Read the values from cells
                for row in worksheet.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col, values_only=True):
                    for cell in row:
                        data_in_range.append(cell)
                results[var[0]] = data_in_range

        except FileNotFoundError:
            print("File Not Found")

        return results

    def combine(variables_values):
        values = list(variables_values.values())
        good_values = list(filter(lambda x: x != [], values))
        return list(product(*good_values))

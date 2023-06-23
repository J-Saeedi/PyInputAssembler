import re


class CodeManipulator:
    codeAddress = None
    # scan_re_key = r"\s*(.+?)\s*=\s*\\?\s*.+#\s*\@\@(.+)\@\@"
    scan_re_key = r"\s*(.+?)\s*=\s*\\?\s*(\S+)\s*#\s*\@\@(.+)\@\@"

    @classmethod
    def scan_variables(cls):
        if not cls.codeAddress:
            raise FileNotFoundError
        with open(cls.codeAddress) as f:
            code_text = str(f.read())
        result = re.findall(cls.scan_re_key, code_text)
        result = list(map(lambda x: (x[0], x[2]), result))
        # print(result)
        return result

    @classmethod
    def generate_case(cls, name, data):
        template_code = ""
        with open(cls.codeAddress) as f:
            template_code = str(f.read())
        new_code = template_code
        for variable in data:
            old_part = r"\@\@(.+)\@\@"
            new_part = r"\@\@(" + str(variable) + r")\@\@"
            key = cls.scan_re_key.replace(old_part, new_part)
            if data[variable]:
                new_value = r"\n\1 = " + str(data[variable]) + r" # @@\3@@"
            else:
                new_value = r"\n\1 = r'" + str(name) + r"' # @@\3@@"
            print([new_value])
            new_code = re.sub(key, new_value, new_code)

        with open(f"{name}.py", "w") as f:
            f.write(new_code)

    def generate_launcher(fileName, cores):
        template = """import multiprocessing
import os
from glob import glob
import runpy
# Define a function to run a Python file


def run_file(filename):
    # Execute the Python file using the execfile() function
    with open(filename) as infile:
        runpy.run_path(filename)


if __name__ == '__main__':
    # Define a list of Python files to run
    files = list(glob("Case*.py"))

    # Specify the maximum number of worker processes to use
    max_processes = 2

    # Call the freeze_support() function on Windows
    if os.name == 'nt':
        multiprocessing.freeze_support()

    # Create a process pool with the specified number of worker processes
    pool = multiprocessing.Pool(processes=max_processes)

    # Run each Python file in a separate process
    pool.map(run_file, files)

    # Close the process pool
    pool.close()
    pool.join()

"""
        code = template.replace("max_processes = 2",
                                f"max_processes = {cores}")
        with open(fileName, 'w') as f:
            f.write(code)
